from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer
from zope.interface import implements
from dewbxml import wbxmlparser, wbxmlreader, wbxmldocument, wbxmlelement, wbxmlstring
import struct

class WBXMLProducer(object):
	implements(IBodyProducer)
	def __init__(self, wbdoc, verbose=False):
		self.verbose=verbose
		self.wb = wbdoc
		self.body = str(self.wb.tobytes())
		self.length = len(self.body)
	def startProducing(self, consumer):
		#if self.verbose: print "Producing",self.body.encode("hex"), self.wb
		consumer.write(self.body)
		return succeed(None)
	def pauseProducing(self): pass
	def stopProducing(self): pass

def convert_array_to_children(in_elem, in_val):
	if isinstance(in_val, list):
		for v in in_val:
			if len(v) > 2:
				add_elem = wbxmlelement(v[0], page_num=v[2])
			else:
				add_elem = wbxmlelement(v[0], page_num=in_elem.page_num)
			in_elem.addchild(add_elem)
			convert_array_to_children(add_elem, v[1])
	elif isinstance(in_val, dict):
		print "FOUND OPAQUE THING",in_val
		in_elem.addchild(wbxmlstring(struct.pack(in_val["fmt"],in_val["val"]), opaque=True))
		print "OPAQUE PRODUCED",in_elem
	elif in_val != None:
		in_elem.addchild(wbxmlstring(in_val))

def convert_dict_to_wbxml(indict, default_page_num=None):
	wb = wbxmldocument()
	wb.encoding = "utf-8"
	wb.version = "1.3"
	wb.schema = "activesync"
	assert len(indict) == 1 # must be only one root element
	#print "Root",indict.keys()[0]
	if default_page_num != None:
		root = wbxmlelement(indict.keys()[0], page_num=default_page_num)
	else:
		root = wbxmlelement(indict.keys()[0])
	wb.addchild(root)
	convert_array_to_children(root, indict.values()[0])
	return wb
		
class FolderSyncProducer(WBXMLProducer):
	def __init__(self, sync_key, verbose=False):
		wb = convert_dict_to_wbxml({
			"FolderSync": [
				("SyncKey", str(sync_key))
			]
		}, default_page_num=7);
		return WBXMLProducer.__init__(self, wb, verbose=verbose)



class ItemOperationsProducer(WBXMLProducer):
	def __init__(self, opname, collection_id, server_id, fetch_type, mimeSupport, store="Mailbox", verbose=False):
		server_ids = []
		if isinstance(server_id, list):
			server_ids.extend(server_id)
		else:
			server_ids.append(server_id)
		wbdict = {
			"ItemOperations": []
		}
		for sid in server_ids:
			if store == "Mailbox":
				wbdict["ItemOperations"].append((opname, [
					("Store", str(store)),
					("CollectionId", str(collection_id), 0),
					("ServerId", str(sid), 0),
					("Options",[
						("MIMESupport", str(mimeSupport), 0),
						("BodyPreference", [
							("Type", str(fetch_type)),
							("TruncationSize", str(512))
						], 17)
					]),
				]))
			else:
				wbdict["ItemOperations"].append((opname, [
					("Store", str(store)),
					("LinkId", str(sid), 19),
					("Options",[]),
				]))				
		wb = convert_dict_to_wbxml(wbdict, default_page_num=20)
		return WBXMLProducer.__init__(self, wb, verbose=verbose)

class SyncProducer(WBXMLProducer):
	def __init__(self, collection_id, sync_key, get_body, verbose=False):
		wbdict = {
			"Sync": [
				("Collections", [
					("Collection", [
						("SyncKey", str(sync_key)),
						("CollectionId", str(collection_id)),
						("DeletesAsMoves", "1"),
					])
				])
			]
		}
		if sync_key != 0:
			wbdict["Sync"][0][1][0][1].append(("GetChanges","1"))
			wbdict["Sync"][0][1][0][1].append(("WindowSize","512"))
		if get_body:
			wbdict["Sync"][0][1][0][1].append(("Options",[
				("MIMESupport", "0"),
				("BodyPreference", [
					("Type", "2"),
					("TruncationSize", "5120"),
				], 17)
			]))
		wb = convert_dict_to_wbxml(wbdict, default_page_num=0)
		return WBXMLProducer.__init__(self, wb, verbose=verbose)

class ProvisionProducer(WBXMLProducer):
	def __init__(self, policyKey=None, verbose=False):
		wbdict = {
			"Provision": [
				("Policies", [
					("Policy", [
						("PolicyType", "MS-EAS-Provisioning-WBXML"),
					])
				])
			]
		}

		if policyKey != None:
			wbdict["Provision"][0][1][0][1].append(("PolicyKey",str(policyKey)))
			wbdict["Provision"][0][1][0][1].append(("Status","1"))
		
		wb = convert_dict_to_wbxml(wbdict, default_page_num=14)

		return WBXMLProducer.__init__(self, wb, verbose=verbose)