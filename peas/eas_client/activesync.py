from twisted.internet import reactor, protocol, defer
from twisted.internet.ssl import ClientContextFactory
from twisted.python.failure import Failure
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from xml.dom.minidom import getDOMImplementation
import base64, urlparse, StringIO, uuid, sys
from urllib import urlencode
from dewbxml import wbxmlparser, wbxmlreader, wbxmldocument, wbxmlelement, wbxmlstring
from activesync_producers import WBXMLProducer, FolderSyncProducer, SyncProducer, ProvisionProducer, ItemOperationsProducer

version = "1.0"

class DataReader(wbxmlreader):
    def __init__(self, data):
        self._wbxmlreader__bytes = StringIO.StringIO(data)

def convert_wbelem_to_dict(wbe):
    if isinstance(wbe, wbxmlelement):
        out_dict = {}
        k = wbe.name
        if len(wbe.children) == 1:
            v = convert_wbelem_to_dict(wbe.children[0])
        else:
            name_dupe = False
            child_names = []
            for child in wbe.children:
                if isinstance(child, wbxmlelement):
                    if child.name in child_names:
                        name_dupe = True
                        break
                    child_names.append(child.name)
            if not name_dupe:
                v = {}
                for child in wbe.children:
                    v.update(convert_wbelem_to_dict(child))
            else:
                v = []
                for child in wbe.children:
                    v.append(convert_wbelem_to_dict(child))
        out_dict[k] = v
    else:
        return str(wbe).strip()
    return out_dict


class WBXMLHandler(protocol.Protocol):
    def __init__(self, deferred, verbose=False):
        self.deferred = deferred
        self.d = ''
        self.verbose = verbose
    def dataReceived(self, data):
        self.d += data
    def connectionLost(self, reason):
        if self.verbose: print "FINISHED LOADING"#, self.d.encode("hex")
        if not len(self.d):
            # this is valid from sync command
            self.deferred.callback(None)
            return
        wb = wbxmlparser()
        doc = wb.parse(DataReader(self.d))
        res_dict = convert_wbelem_to_dict(doc.root)
        if self.verbose: print "Result:",res_dict
        if "Status" in res_dict.values()[0]:
            err_status = int(res_dict.values()[0]["Status"])
            if err_status != 1:
                # application-layer error
                self.deferred.errback("ActiveSync error %d"%err_status)
                return
        self.deferred.callback(res_dict)


class WebClientContextFactory(ClientContextFactory):
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)

class ActiveSync(object):
    def __init__(self, domain, username, pw, server, use_ssl, policy_key=0, server_version="14.0", device_type="iPhone", device_id=None, verbose=False):
        self.use_ssl = use_ssl
        self.domain = domain
        self.username = username
        self.password = pw
        self.server = server
        self.device_id = device_id
        if not self.device_id:
            self.device_id = str(uuid.uuid4()).replace("-","")[:32]
        self.server_version = server_version
        self.device_type = device_type
        self.policy_key = policy_key
        self.folder_data = {}
        self.verbose = verbose
        self.collection_data = {}
        clientContext = WebClientContextFactory()
        self.agent = Agent(reactor, clientContext)
        self.operation_queue = defer.DeferredQueue()
        self.queue_deferred = self.operation_queue.get()
        self.queue_deferred.addCallback(self.queue_full)

    # Response processing

    def activesync_error(self, err):
        if self.verbose: print "ERROR",err
        return Failure(exc_value=err, exc_type="ActiveSync")
    def options_response(self, resp):
        if resp.code != 200:
            return self.activesync_error("Response code %d"%resp.code)
        supported_commands = resp.headers.getRawHeaders("ms-asprotocolcommands")
        return supported_commands

    def wbxml_response(self, response):
        if response.code != 200:
            return self.activesync_error("Response code %d"%response.code)
        d = defer.Deferred()
        response.deliverBody(WBXMLHandler(d, self.verbose))
        return d

    def process_fetch(self, resp):
        if isinstance(resp["ItemOperations"]["Response"], list): # multifetch
            return resp["ItemOperations"]["Response"]
        else:
            return resp["ItemOperations"]["Response"]["Fetch"]

    def process_sync(self, resp, collection_id):
        if not resp:
            return self.collection_data[collection_id]["data"]
            
        sync_key = resp["Sync"]["Collections"]["Collection"]["SyncKey"]
        collection_id = resp["Sync"]["Collections"]["Collection"]["CollectionId"]
        
        assert collection_id != None
        if collection_id not in self.collection_data: # initial sync
            self.collection_data[collection_id] = {"key":sync_key}
            return self.sync(collection_id, sync_key)
        else:
            self.collection_data[collection_id]["key"] = sync_key
            if "data" not in self.collection_data[collection_id]:
                self.collection_data[collection_id]["data"] = {}
            if "Commands" in resp["Sync"]["Collections"]["Collection"]:

                commands = resp["Sync"]["Collections"]["Collection"]["Commands"]
                if isinstance(commands, dict):

                    for command, cmdinfo in commands.iteritems():
                        if self.verbose:
                            print "PROCESS COMMAND:", command, cmdinfo
                        if command == 'Add':
                            server_id = cmdinfo['ServerId']
                            self.collection_data[collection_id]['data'][server_id] = cmdinfo

                else:
                    # This seems to assume "commands" is a list but it was a dict when tested.
                    for command in resp["Sync"]["Collections"]["Collection"]["Commands"]:
                        if self.verbose:
                            print "PROCESS COMMAND",command
                            print "all commands:", resp["Sync"]["Collections"]["Collection"]["Commands"]
                        if "Add" in command:
                            try:
                                server_id = command["Add"]["ServerId"]
                            except:
                                print "ERROR: Unexpected add format:",command["Add"]
                                continue
                            self.collection_data[collection_id]["data"][server_id] = command["Add"]
        
        if "MoreAvailable" in resp["Sync"]["Collections"]["Collection"]:
            if self.verbose: print "MORE AVAILABLE, syncing again"
            return self.sync(collection_id, sync_key)

        return self.collection_data[collection_id]["data"]

    def process_folder_sync(self, resp):
        if "folders" not in self.folder_data:
            self.folder_data["folders"] = {}
        self.folder_data["key"] = resp["FolderSync"]["SyncKey"]
        for change in resp["FolderSync"]["Changes"]:
            if "Add" in change:
                server_id = change["Add"]["ServerId"]
                self.folder_data["folders"][server_id] = change["Add"]
        return self.folder_data["folders"]

    def acknowledge_result(self, policyKey):
        if self.verbose: print "FINAL POLICY KEY",policyKey
        self.policy_key = policyKey
        return True
    def process_policy_key(self, resp):
        try:
            policyKey = resp["Provision"]["Policies"]["Policy"]["PolicyKey"]
        except:
            raise Exception("ActiveSync","Retrieving policy key failed",sys.exc_info()[0])
        return policyKey


    # Request helpers

    def get_url(self):
        scheme = "http"
        if self.use_ssl:
            scheme = "https"
        return "%s://%s/Microsoft-Server-ActiveSync"%(scheme, self.server)
    def add_parameters(self, url, params):
        ps = list(urlparse.urlparse(url))
        ps[4] = urlencode(params)
        return urlparse.urlunparse(ps)
    def authorization_header(self):
        return "Basic "+base64.b64encode("%s\%s:%s"%(self.domain.lower(),self.username.lower(),self.password))

    # Request queueing

    def queue_full(self, next_request):
        if self.verbose: print "Queue full",next_request
        method = next_request[0]
        retd = next_request[-1]
        args = next_request[1:-2]
        kwargs = next_request[-2]
        d = method(*args, **kwargs)
        d.addCallback(self.request_finished, retd)
        d.addErrback(self.request_failed, retd)

    def request_finished(self, obj, return_deferred):
        if self.verbose: print "Request finished, resetting queue",obj,return_deferred
        self.queue_deferred = self.operation_queue.get()
        self.queue_deferred.addCallback(self.queue_full)
        return_deferred.callback(obj)

    def request_failed(self, failure, return_deferred):
        if self.verbose: print "Request failed, resetting queue",failure,return_deferred
        self.queue_deferred = self.operation_queue.get()
        self.queue_deferred.addCallback(self.queue_full)
        return_deferred.errback(failure)

    def add_operation(self, *operation_method_and_args, **kwargs):
        if self.verbose: print "Add operation",operation_method_and_args
        ret_d = defer.Deferred()
        self.operation_queue.put(operation_method_and_args+(kwargs,ret_d,))
        return ret_d

    # Supported Requests

    def get_options(self):
        if self.verbose: print "Options, get URL:",self.get_url(),"Authorization",self.authorization_header()
        d = self.agent.request(
            'OPTIONS',
            self.get_url(),
            Headers({'User-Agent': ['python-EAS-Client %s'%version], 'Authorization': [self.authorization_header()]}),
            None)
        d.addCallback(self.options_response)
        d.addErrback(self.activesync_error)
        return d

    def acknowledge(self, policyKey):
        self.policy_key = policyKey
        prov_url = self.add_parameters(self.get_url(), {"Cmd":"Provision", "User":self.username, "DeviceId":self.device_id, "DeviceType":self.device_type})
        d = self.agent.request(
            'POST',
            prov_url,
            Headers({'User-Agent': ['python-EAS-Client %s'%version], 
                        'Authorization': [self.authorization_header()],
                        'MS-ASProtocolVersion': [self.server_version],
                        'X-MS-PolicyKey': [str(self.policy_key)],
                        'Content-Type': ["application/vnd.ms-sync.wbxml"]}),
            ProvisionProducer(policyKey, verbose=self.verbose))
        d.addCallback(self.wbxml_response)
        d.addCallback(self.process_policy_key)
        d.addCallback(self.acknowledge_result)
        d.addErrback(self.activesync_error)
        return d    

    def provision(self):
        prov_url = self.add_parameters(self.get_url(), {"Cmd":"Provision", "User":self.username, "DeviceId":self.device_id, "DeviceType":self.device_type})
        d = self.agent.request(
            'POST',
            prov_url,
            Headers({'User-Agent': ['python-EAS-Client %s'%version], 
                        'Authorization': [self.authorization_header()],
                        'MS-ASProtocolVersion': [self.server_version],
                        'X-MS-PolicyKey': [str(self.policy_key)],
                        'Content-Type': ["application/vnd.ms-sync.wbxml"]}),
            ProvisionProducer(verbose=self.verbose))
        d.addCallback(self.wbxml_response)
        d.addCallback(self.process_policy_key)
        d.addCallback(self.acknowledge)
        d.addErrback(self.activesync_error)
        return d    

    def folder_sync(self, sync_key=0):
        if sync_key == 0 and "key" in self.folder_data:
            sync_key = self.folder_data["key"]
        sync_url = self.add_parameters(self.get_url(), {"Cmd":"FolderSync", "User":self.username, "DeviceId":self.device_id, "DeviceType":self.device_type})
        d = self.agent.request(
            'POST',
            sync_url,
            Headers({'User-Agent': ['python-EAS-Client %s'%version], 
                        'Authorization': [self.authorization_header()],
                        'MS-ASProtocolVersion': [self.server_version],
                        'X-MS-PolicyKey': [str(self.policy_key)],
                        'Content-Type': ["application/vnd.ms-sync.wbxml"]}),
            FolderSyncProducer(sync_key, verbose=self.verbose))
        d.addCallback(self.wbxml_response)
        d.addCallback(self.process_folder_sync)
        d.addErrback(self.activesync_error)
        return d

    def sync(self, collectionId, sync_key=0, get_body=False):
        if sync_key == 0 and collectionId in self.collection_data:
            sync_key = self.collection_data[collectionId]["key"]

        sync_url = self.add_parameters(self.get_url(), {"Cmd":"Sync", "User":self.username, "DeviceId":self.device_id, "DeviceType":self.device_type})
        d = self.agent.request(
            'POST',
            sync_url,
            Headers({'User-Agent': ['python-EAS-Client %s'%version], 
                        'Authorization': [self.authorization_header()],
                        'MS-ASProtocolVersion': [self.server_version],
                        'X-MS-PolicyKey': [str(self.policy_key)],
                        'Content-Type': ["application/vnd.ms-sync.wbxml"]}),
            SyncProducer(collectionId, sync_key, get_body, verbose=self.verbose))
        d.addCallback(self.wbxml_response)
        d.addCallback(self.process_sync, collectionId)
        d.addErrback(self.activesync_error)
        return d

    def fetch(self, collectionId, serverId, fetchType, mimeSupport=0):
        fetch_url = self.add_parameters(self.get_url(), {"Cmd":"ItemOperations", "User":self.username, "DeviceId":self.device_id, "DeviceType":self.device_type})
        d = self.agent.request(
            'POST',
            fetch_url,
            Headers({'User-Agent': ['python-EAS-Client %s'%version], 
                        'Authorization': [self.authorization_header()],
                        'MS-ASProtocolVersion': [self.server_version],
                        'X-MS-PolicyKey': [str(self.policy_key)],
                        'Content-Type': ["application/vnd.ms-sync.wbxml"]}),
            ItemOperationsProducer("Fetch", collectionId, serverId, fetchType, mimeSupport, store="Mailbox", verbose=self.verbose))
        d.addCallback(self.wbxml_response)
        d.addCallback(self.process_fetch)
        d.addErrback(self.activesync_error)
        return d

    def fetch_link(self, linkId):
        fetch_url = self.add_parameters(self.get_url(), {"Cmd":"ItemOperations", "User":self.username, "DeviceId":self.device_id, "DeviceType":self.device_type})
        d = self.agent.request(
            'POST',
            fetch_url,
            Headers({'User-Agent': ['python-EAS-Client %s'%version], 
                        'Authorization': [self.authorization_header()],
                        'MS-ASProtocolVersion': [self.server_version],
                        'X-MS-PolicyKey': [str(self.policy_key)],
                        'Content-Type': ["application/vnd.ms-sync.wbxml"]}),
            ItemOperationsProducer("Fetch", None, linkId, None, None, store="DocumentLibrary", verbose=self.verbose))
        d.addCallback(self.wbxml_response)
        d.addCallback(self.process_fetch)
        d.addErrback(self.activesync_error)
        return d
