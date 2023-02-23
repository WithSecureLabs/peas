########################################################################
# Copyright (C) 2013 Sol Birnbaum
# 
# This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
########################################################################

# Code Playground

import sys, time
import ssl

from utils.as_code_pages import as_code_pages
from utils.wbxml import wbxml_parser
from utils.wapxml import wapxmltree, wapxmlnode
from client.storage import storage

from client.FolderSync import FolderSync
from client.Sync import Sync
from client.GetItemEstimate import GetItemEstimate
from client.Ping import Ping
from client.Provision import Provision
from client.ValidateCert import ValidateCert

from objects.MSASHTTP import ASHTTPConnector
from objects.MSASCMD import FolderHierarchy, as_status
from objects.MSASAIRS import airsync_FilterType, airsync_Conflict, airsync_MIMETruncation, airsync_MIMESupport, \
    airsync_Class, airsyncbase_Type

from proto_creds import *  #create a file proto_creds.py with vars: as_server, as_user, as_pass

# Disable SSL certificate verification.
ssl._create_default_https_context = ssl._create_unverified_context

pyver = sys.version_info

storage.create_db_if_none()
conn, curs = storage.get_conn_curs()
device_info = {
    "Model": "Outlook for iOS and Android",
    "IMEI": "2095f3b9f442a32220d4d54e641bd4aa",
    "FriendlyName": "Outlook for iOS and Android",
    "OS": "OutlookBasicAuth",
    "OSLanguage": "en-us",
    "PhoneNumber": "NA",
    "MobileOperator": "NA",
    "UserAgent": "Outlook-iOS-Android/1.0"
}

#create wbxml_parser test
cp, cp_sh = as_code_pages.build_as_code_pages()
parser = wbxml_parser(cp, cp_sh)

#create ActiveSync connector
as_conn = ASHTTPConnector(as_server)  #e.g. "as.myserver.com"
as_conn.set_credential(as_user, as_pass)
as_conn.options()
policykey = storage.get_keyvalue("X-MS-PolicyKey")
if policykey:
    as_conn.set_policykey(policykey)


def as_request(cmd, wapxml_req):
    print "\r\n%s Request:" % cmd
    print wapxml_req
    res = as_conn.post(cmd, parser.encode(wapxml_req))
    wapxml_res = parser.decode(res)
    print "\r\n%s Response:" % cmd
    print wapxml_res
    return wapxml_res


#Provision functions
def do_apply_eas_policies(policies):
    for policy in policies.keys():
        print "Virtually applying %s = %s" % (policy, policies[policy])
    return True


def do_provision():
    provision_xmldoc_req = Provision.build("0", device_info)
    as_conn.set_policykey("0")
    provision_xmldoc_res = as_request("Provision", provision_xmldoc_req)
    status, policystatus, policykey, policytype, policydict, settings_status = Provision.parse(provision_xmldoc_res)
    as_conn.set_policykey(policykey)
    storage.update_keyvalue("X-MS-PolicyKey", policykey)
    storage.update_keyvalue("EASPolicies", repr(policydict))
    if do_apply_eas_policies(policydict):
        provision_xmldoc_req = Provision.build(policykey)
        provision_xmldoc_res = as_request("Provision", provision_xmldoc_req)
        status, policystatus, policykey, policytype, policydict, settings_status = Provision.parse(provision_xmldoc_res)
        if status == "1":
            as_conn.set_policykey(policykey)
            storage.update_keyvalue("X-MS-PolicyKey", policykey)

#FolderSync + Provision
foldersync_xmldoc_req = FolderSync.build(storage.get_synckey("0"))
foldersync_xmldoc_res = as_request("FolderSync", foldersync_xmldoc_req)
changes, synckey, status = FolderSync.parse(foldersync_xmldoc_res)
if int(status) > 138 and int(status) < 145:
    print as_status("FolderSync", status)
    do_provision()
    foldersync_xmldoc_res = as_request("FolderSync", foldersync_xmldoc_req)
    changes, synckey, status = FolderSync.parse(foldersync_xmldoc_res)
    if int(status) > 138 and int(status) < 145:
        print as_status("FolderSync", status)
        raise Exception("Unresolvable provisoning error: %s. Cannot continue..." % status)
if len(changes) > 0:
    storage.update_folderhierarchy(changes)
    storage.update_synckey(synckey, "0", curs)
    conn.commit()

collection_id_of = storage.get_folder_name_to_id_dict()

INBOX = collection_id_of["Inbox"]
SENT_ITEMS = collection_id_of["Sent Items"]
CALENDAR = collection_id_of["Calendar"]
CONTACTS = collection_id_of["Contacts"]
if 'Suggested Contacts' in collection_id_of:
    SUGGESTED_CONTACTS = collection_id_of["Suggested Contacts"]
else:
    SUGGESTED_CONTACTS = None
NOTES = collection_id_of["Notes"]
TASKS = collection_id_of["Tasks"]

collection_sync_params = {
    INBOX:
        {  #"Supported":"",
           #"DeletesAsMoves":"1",
           #"GetChanges":"1",
           "WindowSize": "512",
           "Options": {
               "FilterType": airsync_FilterType.OneMonth,
               "Conflict": airsync_Conflict.ServerReplacesClient,
               "MIMETruncation": airsync_MIMETruncation.TruncateNone,
               "MIMESupport": airsync_MIMESupport.SMIMEOnly,
               "Class": airsync_Class.Email,
               #"MaxItems":"300", #Recipient information cache sync requests only. Max number of frequently used contacts.
               "airsyncbase_BodyPreference": [{
                                                  "Type": airsyncbase_Type.HTML,
                                                  "TruncationSize": "1000000000",  # Max 4,294,967,295
                                                  "AllOrNone": "1",
                                                  # I.e. Do not return any body, if body size > tuncation size
                                                  #"Preview": "255", # Size of message preview to return 0-255
                                              },
                                              {
                                                  "Type": airsyncbase_Type.MIME,
                                                  "TruncationSize": "3000000000",  # Max 4,294,967,295
                                                  "AllOrNone": "1",
                                                  # I.e. Do not return any body, if body size > tuncation size
                                                  #"Preview": "255", # Size of message preview to return 0-255
                                              }
               ],
               #"airsyncbase_BodyPartPreference":"",
               #"rm_RightsManagementSupport":"1"
           },
           #"ConversationMode":"1",
           #"Commands": {"Add":None, "Delete":None, "Change":None, "Fetch":None}
           },
    SENT_ITEMS:
        {  #"Supported":"",
           #"DeletesAsMoves":"1",
           #"GetChanges":"1",
           "WindowSize": "512",
           "Options": {
               "FilterType": airsync_FilterType.OneMonth,
               "Conflict": airsync_Conflict.ServerReplacesClient,
               "MIMETruncation": airsync_MIMETruncation.TruncateNone,
               "MIMESupport": airsync_MIMESupport.SMIMEOnly,
               "Class": airsync_Class.Email,
               #"MaxItems":"300", #Recipient information cache sync requests only. Max number of frequently used contacts.
               "airsyncbase_BodyPreference": [{
                                                  "Type": airsyncbase_Type.HTML,
                                                  "TruncationSize": "1000000000",  # Max 4,294,967,295
                                                  "AllOrNone": "1",
                                                  # I.e. Do not return any body, if body size > tuncation size
                                                  #"Preview": "255", # Size of message preview to return 0-255
                                              },
                                              {
                                                  "Type": airsyncbase_Type.MIME,
                                                  "TruncationSize": "3000000000",  # Max 4,294,967,295
                                                  "AllOrNone": "1",
                                                  # I.e. Do not return any body, if body size > tuncation size
                                                  #"Preview": "255", # Size of message preview to return 0-255
                                              }
               ],
               #"airsyncbase_BodyPartPreference":"",
               #"rm_RightsManagementSupport":"1"
           },
           #"ConversationMode":"1",
           #"Commands": {"Add":None, "Delete":None, "Change":None, "Fetch":None}
           },
    CALENDAR:
        {
            "WindowSize": "512",
            "Options": {
                "FilterType": airsync_FilterType.OneMonth,
                "Conflict": airsync_Conflict.ServerReplacesClient,
                "MIMETruncation": airsync_MIMETruncation.TruncateNone,
                "MIMESupport": airsync_MIMESupport.SMIMEOnly,
                "Class": airsync_Class.Calendar,
                "airsyncbase_BodyPreference": [{
                                                   "Type": airsyncbase_Type.HTML,
                                                   "TruncationSize": "1000000000",  # Max 4,294,967,295
                                                   "AllOrNone": "1",
                                                   # I.e. Do not return any body, if body size > tuncation size
                                                   #"Preview": "255", # Size of message preview to return 0-255
                                               },
                                               {
                                                   "Type": airsyncbase_Type.MIME,
                                                   "TruncationSize": "3000000000",  # Max 4,294,967,295
                                                   "AllOrNone": "1",
                                                   # I.e. Do not return any body, if body size > tuncation size
                                               }
                ],
            },
        },
    CONTACTS:
        {
            "WindowSize": "512",
            "Options": {
                #"FilterType": airsync_FilterType.OneWeek,
                "Conflict": airsync_Conflict.ServerReplacesClient,
                "MIMETruncation": airsync_MIMETruncation.TruncateNone,
                "MIMESupport": airsync_MIMESupport.SMIMEOnly,
                "Class": airsync_Class.Contacts,
                "airsyncbase_BodyPreference": [{
                                                   "Type": airsyncbase_Type.HTML,
                                                   "TruncationSize": "1000000000",  # Max 4,294,967,295
                                                   "AllOrNone": "1",
                                                   # I.e. Do not return any body, if body size > tuncation size
                                                   #"Preview": "255", # Size of message preview to return 0-255
                                               },
                                               {
                                                   "Type": airsyncbase_Type.MIME,
                                                   "TruncationSize": "3000000000",  # Max 4,294,967,295
                                                   "AllOrNone": "1",
                                                   # I.e. Do not return any body, if body size > tuncation size
                                               }
                ],
            },
        },

    NOTES:
        {
            "WindowSize": "512",
            "Options": {
                #"FilterType": airsync_FilterType.OneWeek,
                "Conflict": airsync_Conflict.ServerReplacesClient,
                "MIMETruncation": airsync_MIMETruncation.TruncateNone,
                "MIMESupport": airsync_MIMESupport.SMIMEOnly,
                "Class": airsync_Class.Notes,
                "airsyncbase_BodyPreference": [{
                                                   "Type": airsyncbase_Type.HTML,
                                                   "TruncationSize": "1000000000",  # Max 4,294,967,295
                                                   "AllOrNone": "1",
                                                   # I.e. Do not return any body, if body size > tuncation size
                                                   #"Preview": "255", # Size of message preview to return 0-255
                                               },
                                               {
                                                   "Type": airsyncbase_Type.MIME,
                                                   "TruncationSize": "3000000000",  # Max 4,294,967,295
                                                   "AllOrNone": "1",
                                                   # I.e. Do not return any body, if body size > tuncation size
                                               }
                ],
            },
        },
    TASKS:
        {
            "WindowSize": "512",
            "Options": {
                #"FilterType": airsync_FilterType.OneWeek,
                "Conflict": airsync_Conflict.ServerReplacesClient,
                "MIMETruncation": airsync_MIMETruncation.TruncateNone,
                "MIMESupport": airsync_MIMESupport.SMIMEOnly,
                "Class": airsync_Class.Tasks,
                "airsyncbase_BodyPreference": [{
                                                   "Type": airsyncbase_Type.HTML,
                                                   "TruncationSize": "1000000000",  # Max 4,294,967,295
                                                   "AllOrNone": "1",
                                                   # I.e. Do not return any body, if body size > tuncation size
                                                   #"Preview": "255", # Size of message preview to return 0-255
                                               },
                                               {
                                                   "Type": airsyncbase_Type.MIME,
                                                   "TruncationSize": "3000000000",  # Max 4,294,967,295
                                                   "AllOrNone": "1",
                                                   # I.e. Do not return any body, if body size > tuncation size
                                               }
                ],
            },
        }
}

if SUGGESTED_CONTACTS:
    collection_sync_params[SUGGESTED_CONTACTS] = {
        "WindowSize": "512",
        "Options": {
            #"FilterType": airsync_FilterType.OneWeek,
            "Conflict": airsync_Conflict.ServerReplacesClient,
            "MIMETruncation": airsync_MIMETruncation.TruncateNone,
            "MIMESupport": airsync_MIMESupport.SMIMEOnly,
            "Class": airsync_Class.Contacts,
            "airsyncbase_BodyPreference": [{
                                               "Type": airsyncbase_Type.HTML,
                                               "TruncationSize": "1000000000",  # Max 4,294,967,295
                                               "AllOrNone": "1",
                                               # I.e. Do not return any body, if body size > tuncation size
                                               #"Preview": "255", # Size of message preview to return 0-255
                                           },
                                           {
                                               "Type": airsyncbase_Type.MIME,
                                               "TruncationSize": "3000000000",  # Max 4,294,967,295
                                               "AllOrNone": "1",
                                               # I.e. Do not return any body, if body size > tuncation size
                                           }
            ],
        },
    }

gie_options = {
    INBOX:
        {  #"ConversationMode": "0",
           "Class": airsync_Class.Email,
           "FilterType": airsync_FilterType.OneMonth
           #"MaxItems": "" #Recipient information cache sync requests only. Max number of frequently used contacts.
           },
    SENT_ITEMS:
        {
            "Class": airsync_Class.Email,
            "FilterType": airsync_FilterType.OneMonth
        },
    CALENDAR:
        {"Class": airsync_Class.Calendar,
         "FilterType": airsync_FilterType.OneMonth},
    CONTACTS:
        {
            "Class": airsync_Class.Contacts,
        },
    SUGGESTED_CONTACTS:
        {
            "Class": airsync_Class.Contacts,
        },
    NOTES:
        {
            "Class": airsync_Class.Notes,
        },
    TASKS:
        {
            "Class": airsync_Class.Tasks,
        }
}


#Sync function
def do_sync(collections):
    as_sync_xmldoc_req = Sync.build(storage.get_synckeys_dict(curs), collections)
    print "\r\nRequest:"
    print as_sync_xmldoc_req
    res = as_conn.post("Sync", parser.encode(as_sync_xmldoc_req))
    print "\r\nResponse:"
    if res == '':
        print "Nothing to Sync!"
    else:
        collectionid_to_type_dict = storage.get_serverid_to_type_dict()
        as_sync_xmldoc_res = parser.decode(res)
        print as_sync_xmldoc_res
        sync_res = Sync.parse(as_sync_xmldoc_res, collectionid_to_type_dict)
        storage.update_items(sync_res)
        return sync_res


#GetItemsEstimate
def do_getitemestimates(collection_ids):
    getitemestimate_xmldoc_req = GetItemEstimate.build(storage.get_synckeys_dict(curs), collection_ids, gie_options)
    getitemestimate_xmldoc_res = as_request("GetItemEstimate", getitemestimate_xmldoc_req)

    getitemestimate_res = GetItemEstimate.parse(getitemestimate_xmldoc_res)
    return getitemestimate_res


def getitemestimate_check_prime_collections(getitemestimate_responses):
    has_synckey = []
    needs_synckey = {}
    for response in getitemestimate_responses:
        if response.Status == "1":
            has_synckey.append(response.CollectionId)
        elif response.Status == "2":
            print "GetItemEstimate Status: Unknown CollectionId (%s) specified. Removing." % response.CollectionId
        elif response.Status == "3":
            print "GetItemEstimate Status: Sync needs to be primed."
            needs_synckey.update({response.CollectionId: {}})
            has_synckey.append(
                response.CollectionId)  #technically *will* have synckey after do_sync() need end of function
        else:
            print as_status("GetItemEstimate", response.Status)
    if len(needs_synckey) > 0:
        do_sync(needs_synckey)
    return has_synckey, needs_synckey


def sync(collections):
    getitemestimate_responses = do_getitemestimates(collections)

    has_synckey, just_got_synckey = getitemestimate_check_prime_collections(getitemestimate_responses)

    if (len(has_synckey) < collections) or (len(just_got_synckey) > 0):  #grab new estimates, since they changed
        getitemestimate_responses = do_getitemestimates(has_synckey)

    collections_to_sync = {}

    for response in getitemestimate_responses:
        if response.Status == "1":
            if int(response.Estimate) > 0:
                collections_to_sync.update({response.CollectionId: collection_sync_params[response.CollectionId]})
        else:
            print "GetItemEstimate Status (error): %s, CollectionId: %s." % (response.Status, response.CollectionId)

    if len(collections_to_sync) > 0:
        sync_res = do_sync(collections_to_sync)
        if sync_res:
            while True:
                for coll_res in sync_res:
                    if coll_res.MoreAvailable is None:
                        del collections_to_sync[coll_res.CollectionId]
                if len(collections_to_sync.keys()) > 0:
                    print collections_to_sync
                    sync_res = do_sync(collections_to_sync)
                else:
                    break


collections = [INBOX, SENT_ITEMS, CALENDAR, CONTACTS, NOTES, TASKS]
if SUGGESTED_CONTACTS:
    collections.append(SUGGESTED_CONTACTS)
sync(collections)

#Ping (push), GetItemsEstimate and Sync process test
#Ping


ping_args = [(INBOX, "Email"), (SENT_ITEMS, "Email"), (CALENDAR, "Calendar"), (CONTACTS, "Contacts"),
                              (NOTES, "Notes"), (TASKS, "Tasks")]
if SUGGESTED_CONTACTS:
    ping_args.append((SUGGESTED_CONTACTS, "Contacts"))
ping_xmldoc_req = Ping.build("120", ping_args)
ping_xmldoc_res = as_request("Ping", ping_xmldoc_req)
ping_res = Ping.parse(ping_xmldoc_res)
if ping_res[0] == "2":  #2=New changes available
    sync(ping_res[3])

if storage.close_conn_curs(conn):
    del conn, curs