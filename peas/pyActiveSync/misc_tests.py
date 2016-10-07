########################################################################
#  Copyright (C) 2013 Sol Birnbaum
# 
#  This program is free software; you can redistribute it and/or
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

# Tests

import sys, time
import ssl

from utils.as_code_pages import as_code_pages
from utils.wbxml import wbxml_parser
from utils.wapxml import wapxmltree, wapxmlnode
from client.storage import storage

from client.FolderSync import FolderSync
from client.Sync import Sync
from client.GetItemEstimate import GetItemEstimate
from client.ResolveRecipients import ResolveRecipients
from client.FolderCreate import FolderCreate
from client.FolderUpdate import FolderUpdate
from client.FolderDelete import FolderDelete
from client.Ping import Ping
from client.MoveItems import MoveItems
from client.Provision import Provision
from client.ItemOperations import ItemOperations
from client.ValidateCert import ValidateCert
from client.SendMail import SendMail
from client.SmartForward import SmartForward
from client.SmartReply import SmartReply

from objects.MSASHTTP import ASHTTPConnector
from objects.MSASCMD import FolderHierarchy, as_status
from objects.MSASAIRS import airsync_FilterType, airsync_Conflict, airsync_MIMETruncation, airsync_MIMESupport, airsync_Class, airsyncbase_Type

from proto_creds import * #create a file proto_creds.py with vars: as_server, as_user, as_pass


# Disable SSL certificate verification.
ssl._create_default_https_context = ssl._create_unverified_context


pyver = sys.version_info

storage.create_db_if_none()
conn, curs = storage.get_conn_curs()
device_info = {"Model":"%d.%d.%d" % (pyver[0], pyver[1], pyver[2]), "IMEI":"123456", "FriendlyName":"My pyAS Client", "OS":"Python", "OSLanguage":"en-us", "PhoneNumber": "NA", "MobileOperator":"NA", "UserAgent": "pyAS"}

#create wbxml_parser test
cp, cp_sh = as_code_pages.build_as_code_pages()
parser = wbxml_parser(cp, cp_sh)

#create activesync connector
as_conn = ASHTTPConnector(as_server) #e.g. "as.myserver.com"
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

#ItemOperations
itemoperations_params = [{"Name":"Fetch","Store":"Mailbox", "FileReference":"%34%67%32"}]
itemoperations_xmldoc_req = ItemOperations.build(itemoperations_params)
print "\r\nItemOperations Request:\r\n", itemoperations_xmldoc_req
#itemoperations_xmldoc_res, attachment_file = as_conn.fetch_multipart(itemoperations_xmldoc_req, "myattachment1.txt")
#itemoperations_xmldoc_res_parsed = ItemOperations.parse(itemoperations_xmldoc_res)
#print itemoperations_xmldoc_res

#FolderCreate
parent_folder = storage.get_folderhierarchy_folder_by_name("Inbox", curs)
new_folder = FolderHierarchy.Folder(parent_folder[0], "TestFolder1", str(FolderHierarchy.FolderCreate.Type.Mail))
foldercreate_xmldoc_req = FolderCreate.build(storage.get_synckey("0"), new_folder.ParentId, new_folder.DisplayName, new_folder.Type)
foldercreate_xmldoc_res = as_request("FolderCreate", foldercreate_xmldoc_req)
foldercreate_res_parsed = FolderCreate.parse(foldercreate_xmldoc_res)
if foldercreate_res_parsed[0] == "1":
    new_folder.ServerId = foldercreate_res_parsed[2]
    storage.insert_folderhierarchy_change(new_folder, curs)
    storage.update_synckey(foldercreate_res_parsed[1], "0", curs)
    conn.commit()
else:
    print as_status("FolderCreate", foldercreate_res_parsed[0])

time.sleep(5)

#FolderUpdate
old_folder_name = "TestFolder1"
new_folder_name = "TestFolder2"
#new_parent_id = parent_folder = storage.get_folderhierarchy_folder_by_name("Inbox", curs)
folder_row = storage.get_folderhierarchy_folder_by_name(old_folder_name, curs)
update_folder = FolderHierarchy.Folder(folder_row[1], new_folder_name, folder_row[3], folder_row[0])
folderupdate_xmldoc_req = FolderUpdate.build(storage.get_synckey("0"), update_folder.ServerId, update_folder.ParentId, update_folder.DisplayName)
folderupdate_xmldoc_res = as_request("FolderUpdate", folderupdate_xmldoc_req)
folderupdate_res_parsed = FolderUpdate.parse(folderupdate_xmldoc_res)
if folderupdate_res_parsed[0] == "1":
    new_folder.DisplayName = new_folder_name
    storage.update_folderhierarchy_change(new_folder, curs)
    storage.update_synckey(folderupdate_res_parsed[1], "0", curs)
    conn.commit()

time.sleep(5)

#FolderDelete
try:
    folder_name = "TestFolder2"
    folder_row = storage.get_folderhierarchy_folder_by_name(folder_name, curs)
    delete_folder = FolderHierarchy.Folder()
    delete_folder.ServerId = folder_row[0]
    folderdelete_xmldoc_req = FolderDelete.build(storage.get_synckey("0"), delete_folder.ServerId)
    folderdelete_xmldoc_res = as_request("FolderDelete", folderdelete_xmldoc_req)
    folderdelete_res_parsed = FolderDelete.parse(folderdelete_xmldoc_res)
    if folderdelete_res_parsed[0] == "1":
        storage.delete_folderhierarchy_change(delete_folder, curs)
        storage.update_synckey(folderdelete_res_parsed[1], "0", curs)
        conn.commit()
except TypeError, e:
    print "\r\n%s\r\n" % e
    pass

#ResolveRecipients
resolverecipients_xmldoc_req = ResolveRecipients.build("thunderbird")
resolverecipients_xmldoc_res = as_request("ResolveRecipients", resolverecipients_xmldoc_req)


#SendMail
import email.mime.text
email_mid = storage.get_new_mid()
my_email = email.mime.text.MIMEText("Test email #%s from pyAS." % email_mid)
my_email["Subject"] = "Test #%s from pyAS!" % email_mid

my_email["From"] = as_user
my_email["To"] = as_user

sendmail_xmldoc_req = SendMail.build(email_mid, my_email)
print "\r\nRequest:"
print sendmail_xmldoc_req
res = as_conn.post("SendMail", parser.encode(sendmail_xmldoc_req))
print "\r\nResponse:"
if res == '':
    print "\r\nTest message sent successfully!"
else:
    sendmail_xmldoc_res = parser.decode(res)
    print sendmail_xmldoc_res
    sendmail_res = SendMail.parse(sendmail_xmldoc_res)

##MoveItems
#moveitems_xmldoc_req = MoveItems.build([("5:24","5","10")])
#moveitems_xmldoc_res = as_request("MoveItems", moveitems_xmldoc_req)
#moveitems_res = MoveItems.parse(moveitems_xmldoc_res)
#for moveitem_res in moveitems_res:
#    if moveitem_res[1] == "3":
#        storage.update_email({"server_id": moveitem_res[0] ,"ServerId": moveitem_res[2]}, curs)
#        conn.commit()