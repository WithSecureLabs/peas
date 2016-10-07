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

import sqlite3

class storage:
    @staticmethod
    def set_keyvalue(key, value, path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        curs.execute("INSERT INTO KeyValue VALUES ('%s', '%s')" % (key, value))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_keyvalue(key, value, path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        sql = "UPDATE KeyValue SET Value='%s' WHERE Key='%s'" % (value.replace("'","''"), key)
        curs.execute(sql)
        conn.commit()
        conn.close()

    @staticmethod
    def get_keyvalue(key, path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        curs.execute("SELECT Value FROM KeyValue WHERE Key='%s'" % key)
        try:
            value = curs.fetchone()[0]
            conn.close()
            return value
        except:
            conn.close()
            return None

    @staticmethod
    def create_db(path=None):
        if path:
            if path != "pyas.asdb":
                if not path[-1] == "\\":
                    path = path + "\\pyas.asdb"
        else:
            path="pyas.asdb"
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        curs.execute("""CREATE TABLE FolderHierarchy (ServerId text, ParentId text, DisplayName text, Type text)""")
        curs.execute("""CREATE TABLE SyncKeys (SyncKey text, CollectionId text)""")
        curs.execute("""CREATE TABLE KeyValue (Key text, Value blob)""")

        curs.execute("""CREATE TABLE MSASEMAIL (ServerId text, 
                                                email_To text, 
                                                email_Cc text,
                                                email_From text,
                                                email_Subject text,
                                                email_ReplyTo text,
                                                email_DateReceived text,
                                                email_DisplayTo text,
                                                email_ThreadTopic text,
                                                email_Importance text,
                                                email_Read text,
                                                airsyncbase_Attachments text,
                                                airsyncbase_Body text,
                                                email_MessageClass text,
                                                email_InternetCPID text,
                                                email_Flag text,
                                                airsyncbase_NativeBodyType text,
                                                email_ContentClass text,
                                                email2_UmCallerId text,
                                                email2_UmUserNotes text,
                                                email2_ConversationId text,
                                                email2_ConversationIndex text,
                                                email2_LastVerbExecuted text,
                                                email2_LastVerbExecutedTime text,
                                                email2_ReceivedAsBcc text,
                                                email2_Sender text,
                                                email_Categories text,
                                                airsyncbase_BodyPart text,
                                                email2_AccountId text,
                                                rm_RightsManagementLicense text)""")

        curs.execute("""CREATE TABLE MSASCAL (ServerId text, 
                                              calendar_TimeZone text, 
                                              calendar_DtStamp text,
                                              calendar_StartTime text,
                                              calendar_Subject text,
                                              calendar_UID text,
                                              calendar_OrganizerName text,
                                              calendar_OrganizerEmail text,
                                              calendar_Location text,
                                              calendar_EndTime text,
                                              airsyncbase_Body text,
                                              calendar_Sensitivity text,
                                              calendar_BusyStatus text,
                                              calendar_AllDayEvent text,
                                              calendar_Reminder text,
                                              calendar_MeetingStatus text,
                                              airsyncbase_NativeBodyType text,
                                              calendar_ResponseRequested text,
                                              calendar_ResponseType text,
                                              calendar_AppointmentReplyTime text,
                                              calendar_Attendees text,
                                              calendar_Categories text,
                                              calendar_Recurrence text,
                                              calendar_OnlineMeetingConfLink text,
                                              calendar_OnlineMeetingExternalLink text,
                                              calendar_DisallowNewTimeProposal text,
                                              calendar_Exceptions text)""")

        curs.execute("""CREATE TABLE MSASCNTC (ServerId text, 
                                                contacts2_AccountName text,
                                                contacts_Alias text,
                                                contacts_Anniversary text,
                                                contacts_AssistantName text,
                                                contacts_AssistantPhoneNumber text,
                                                contacts_Birthday text,
                                                airsyncbase_Body text,
                                                contacts_BusinessAddressCity text,
                                                contacts_BusinessAddressCountry text,
                                                contacts_BusinessAddressPostalCode text,
                                                contacts_BusinessAddressState text,
                                                contacts_BusinessAddressStreet text,
                                                contacts_BusinessFaxNumber text,
                                                contacts_BusinessPhoneNumber text,
                                                contacts_Business2PhoneNumber text,
                                                contacts_CarPhoneNumber text,
                                                contacts_Categories text,
                                                contacts_Children text,
                                                contacts_2CompanyMainPhone text,
                                                contacts_CompanyName text,
                                                contacts_2CustomerId text,
                                                contacts_Department text,
                                                contacts_FileAs text,
                                                contacts_FirstName text,
                                                contacts_LastName text,
                                                contacts_Email1Address text,
                                                contacts_Email2Address text,
                                                contacts_Email3Address text,
                                                contacts2_GovernmentId text,
                                                contacts_HomeAddressCity text,
                                                contacts_HomeAddressCountry text,
                                                contacts_HomeAddressPostalCode text,
                                                contacts_HomeAddressState text,
                                                contacts_HomeAddressStreet text,
                                                contacts_HomeFaxNumber text,
                                                contacts_HomePhoneNumber text,
                                                contacts_Home2PhoneNumber text,
                                                contacts2_IMAddress text,
                                                contacts2_IMAddress2 text,
                                                contacts2_IMAddress3 text,
                                                contacts_JobTitle text,
                                                contacts2_ManagerName text,
                                                contacts_MiddleName text,
                                                contacts2_MMS text,
                                                contacts_MobilePhoneNumber text,
                                                contacts2_NickName text,
                                                contacts_OfficeLocation text,
                                                contacts_OtherAddressCity text,
                                                contacts_OtherAddressCountry text,
                                                contacts_OtherAddressPostalCode text,
                                                contacts_OtherAddressState text,
                                                contacts_OtherAddressStreet text,
                                                contacts_PagerNumber text,
                                                contacts_Picture text,
                                                contacts_RadioPhoneNumber text,
                                                contacts_Spouse text,
                                                contacts_Suffix text,
                                                contacts_Title text,
                                                contacts_WebPage text,
                                                contacts_WeightedRank text,
                                                contacts_YomiCompanyName text,
                                                contacts_YomiFirstName text,
                                                contacts_YomiLastName text)""")

        curs.execute("""CREATE TABLE MSASNOTE (ServerId text,
                                                notes_Subject text,
                                                airsyncbase_Body text,
                                                notes_MessageClass text,
                                                notes_LastModifiedDate text)""")

        curs.execute("""CREATE TABLE MSASTASK (ServerId text,
                                                airsyncbase_Body text,
                                                tasks_Categories text,
                                                tasks_Complete text,
                                                tasks_DateCompleted text,
                                                tasks_DueDate text,
                                                tasks_Importance text,
                                                tasks_OrdinalDate text,
                                                tasks_Recurrence text,
                                                tasks_ReminderSet text,
                                                tasks_ReminderTime text,
                                                tasks_Sensitivity text,
                                                tasks_StartDate text,
                                                tasks_Subject text,
                                                tasks_SubOrdinalDate text,
                                                tasks_UtcDueDate text,
                                                tasks_UtcStartDate text)""")
        
        conn.commit()

        indicies = ['CREATE UNIQUE INDEX "main"."MSASEMAIL_ServerId_Idx" ON "MSASEMAIL" ("ServerId" ASC)', 
                    'CREATE UNIQUE INDEX "main"."MSASCAL_ServerId_Idx" ON "MSASCAL" ("ServerId" ASC)', 
                    'CREATE UNIQUE INDEX "main"."MSASCNTC_ServerId_Idx" ON "MSASCNTC" ("ServerId" ASC)', 
                    'CREATE UNIQUE INDEX "main"."MSASNOTE_ServerId_Idx" ON "MSASNOTE" ("ServerId" ASC)', 
                    'CREATE UNIQUE INDEX "main"."MSASTASK_ServerId_Idx" ON "MSASTASK" ("ServerId" ASC)', 
                    'CREATE UNIQUE INDEX "main"."SyncKey_CollectionId_Idx" ON "SyncKeys" ("CollectionId" ASC)',
                    'CREATE UNIQUE INDEX "main"."KeyValue_Key_Idx" ON "KeyValue" ("Key" ASC)',
                    'CREATE UNIQUE INDEX "main"."FolderHierarchy_ServerId_Idx" ON "FolderHierarchy" ("ServerId" ASC)',
                    'CREATE  INDEX "main"."FolderHierarchy_ParentType_Idx" ON "FolderHierarchy" ("ParentId" ASC, "Type" ASC)',
                    ]
        for index in indicies:
            curs.execute(index)
        storage.set_keyvalue("X-MS-PolicyKey", "0")
        storage.set_keyvalue("EASPolicies", "")
        storage.set_keyvalue("MID", "0")
        conn.commit()

        conn.close()
    
    @staticmethod
    def get_conn_curs(path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        return conn, curs

    @staticmethod
    def close_conn_curs(conn):
        try:
            conn.commit()
            conn.close()
        except:
            return False
        return True


    @staticmethod
    def insert_folderhierarchy_change(folder, curs):
        sql = "INSERT INTO FolderHierarchy VALUES ('%s', '%s', '%s', '%s')""" % (folder.ServerId, folder.ParentId, folder.DisplayName, folder.Type)
        curs.execute(sql)

    @staticmethod
    def update_folderhierarchy_change(folder, curs):
        sql = "UPDATE FolderHierarchy SET ParentId='%s', DisplayName='%s', Type='%s' WHERE ServerId == '%s'""" % (folder.ParentId, folder.DisplayName, folder.Type, folder.ServerId)
        curs.execute(sql)

    @staticmethod
    def delete_folderhierarchy_change(folder, curs):
        #Command only sent we permement delete is requested. Otherwise it would be 'Update' to ParentId='3' (Deleted Items).
        #sql = "UPDATE FolderHierarchy SET ParentId='4' WHERE ServerId == '%s'""" % (folder.ServerId)
        sql = "DELETE FROM MSASEMAIL WHERE ServerId like '%s:%%'" % (folder.ServerId)
        curs.execute(sql)
        sql = "DELETE FROM FolderHierarchy WHERE ServerId == '%s'" % (folder.ServerId)
        curs.execute(sql)

    @staticmethod
    def update_folderhierarchy(changes, path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        for change in changes:
            if change[0] == "Update":
                storage.update_folderhierarchy_change(change[1], curs)
            elif change[0] == "Delete":
                storage.delete_folderhierarchy_change(change[1], curs)
            elif change[0] == "Add":
                storage.insert_folderhierarchy_change(change[1], curs)
        conn.commit()
        conn.close()

    @staticmethod
    def get_folderhierarchy_folder_by_name(foldername, curs):
        sql = "SELECT * FROM FolderHierarchy WHERE DisplayName = '%s'" % foldername
        curs.execute(sql)
        folder_row = curs.fetchone()
        if folder_row:
            return folder_row
        else:
            return False

    @staticmethod
    def get_folderhierarchy_folder_by_id(server_id, curs):
        sql = "SELECT * FROM FolderHierarchy WHERE ServerId = '%s'" % server_id
        curs.execute(sql)
        folder_row = curs.fetchone()
        if folder_row:
            return folder_row
        else:
            return False

    @staticmethod
    def insert_item(table, calendar_dict, curs):
        server_id = calendar_dict["server_id"]
        del calendar_dict["server_id"]
        calendar_cols = ""
        calendar_vals = ""
        for calendar_field in calendar_dict.keys():
            calendar_cols += (", '%s'" % calendar_field)
            calendar_vals += (", '%s'"  % repr(calendar_dict[calendar_field]).replace("'","''"))
        sql = "INSERT INTO %s ( 'ServerId' %s ) VALUES ( '%s' %s )" % (table, calendar_cols, server_id, calendar_vals)
        curs.execute(sql)

    @staticmethod
    def update_item(table, calendar_dict, curs):
        server_id = calendar_dict["server_id"]
        del calendar_dict["server_id"]
        calendar_sql = ""
        for calendar_field in calendar_dict.keys():
            calendar_sql += (", %s='%s' "  % (calendar_field, repr(calendar_dict[calendar_field]).replace("'","''")))
        calendar_sql = calendar_sql.lstrip(", ")
        sql = "UPDATE %s SET %s WHERE ServerId='%s'" % (table, calendar_sql, server_id)
        curs.execute(sql)
    
    @staticmethod
    def delete_item(table, sever_id, curs):
        sql = "DELETE FROM %s WHERE ServerId='%s'" % (table, sever_id)
        curs.execute(sql)

    class ItemOps:
        Insert = 0
        Delete = 1
        Update = 2
        SoftDelete = 3

    class_to_table_dict = {
                        "Email" : "MSASEMAIL",
                        "Calendar" : "MSASCAL",
                        "Contacts" : "MSASCNTC",
                        "Tasks" : "MSASTASK",
                        "Notes" : "MSASNOTE",
                        "SMS" : "MSASMS",
                        "Document" : "MSASDOC"
                        }

    @staticmethod
    def item_operation(method, item_class, data, curs):
        if method == storage.ItemOps.Insert:
            storage.insert_item(storage.class_to_table_dict[item_class], data, curs)
        elif method == storage.ItemOps.Delete:
            storage.delete_item(storage.class_to_table_dict[item_class], data, curs)
        elif method == storage.ItemOps.Update:
            storage.update_item(storage.class_to_table_dict[item_class], data, curs)
        elif method == storage.ItemOps.SoftDelete:
            storage.delete_item(storage.class_to_table_dict[item_class], data, curs)

    @staticmethod
    def update_items(collections, path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        for collection in collections:
            for command in collection.Commands:
                if command[0] == "Add":
                    storage.item_operation(storage.ItemOps.Insert, command[1][1], command[1][0], curs)
                if command[0] == "Delete":
                    storage.item_operation(storage.ItemOps.Delete, command[1][1], command[1][0], curs)
                elif command[0] == "Change":
                    storage.item_operation(storage.ItemOps.Update, command[1][1], command[1][0], curs)
                elif command[0] == "SoftDelete":
                    storage.item_operation(storage.ItemOps.SoftDelete, command[1][1], command[1][0], curs)
            if collection.SyncKey > 1:
                storage.update_synckey(collection.SyncKey, collection.CollectionId, curs)
                conn.commit()
            else:
                conn.close()
                raise AttributeError("SyncKey incorrect")

        conn.commit()
        conn.close()

    @staticmethod
    def get_emails_by_collectionid(collectionid, curs):
        sql = "SELECT * from MSASEMAIL WHERE ServerId like '%s:%%'" % collectionid
        curs.execute(sql)
        return curs.fetchall()

    @staticmethod
    def update_synckey(synckey, collectionid, curs=None):
        cleanup = False
        if not curs:
            cleanup = True
            conn = sqlite3.connect("pyas.asdb")
            curs = conn.cursor()
        curs.execute("SELECT SyncKey FROM SyncKeys WHERE CollectionId = %s" % collectionid)
        prev_synckey = curs.fetchone()
        if not prev_synckey:
            curs.execute("INSERT INTO SyncKeys VALUES ('%s', '%s')" % (synckey, collectionid))
        else:
            curs.execute("UPDATE SyncKeys SET SyncKey='%s' WHERE CollectionId='%s'" % (synckey, collectionid)) 
        if cleanup:
            conn.commit()
            conn.close()

    @staticmethod
    def get_synckey(collectionid, path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        curs.execute("SELECT SyncKey FROM SyncKeys WHERE CollectionId = %s" % collectionid)
        try:
            synckey = curs.fetchone()[0]
        except TypeError:
            synckey = "0"
        conn.close()
        return synckey

    @staticmethod
    def create_db_if_none(path="pyas.asdb"):
        import os
        if not os.path.isfile(path):
            storage.create_db(path)


    @staticmethod
    def erase_db(path="pyas.asdb"):
        import os
        if os.path.isfile(path):
            os.remove(path)


    @staticmethod
    def get_folder_name_to_id_dict(path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        curs.execute("SELECT DisplayName, ServerId FROM FolderHierarchy")
        id_name_list_of_tuples = curs.fetchall()
        name_id_dict = {}
        for id_name in id_name_list_of_tuples:
            name_id_dict.update({ id_name[0] : id_name[1] })
        conn.close()
        return name_id_dict

    @staticmethod
    def get_synckeys_dict(curs, path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        curs.execute("SELECT * FROM SyncKeys")
        synckeys_rows = curs.fetchall()
        synckeys_dict = {}
        if synckeys_rows:
            if len(synckeys_rows) > 0:
                for synckey_row in synckeys_rows:
                    synckeys_dict.update({synckey_row[1]:synckey_row[0]})
        return synckeys_dict

    @staticmethod
    def get_new_mid(path="pyas.asdb"):
        pmid = int(storage.get_keyvalue("MID"))
        mid = str(pmid+1)
        storage.update_keyvalue("MID", mid)
        return mid

    @staticmethod
    def get_serverid_to_type_dict(path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        curs.execute("SELECT * FROM FolderHierarchy")
        folders_rows = curs.fetchall()
        conn.close()
        folders_dict = {}
        if folders_rows:
            if len(folders_rows) > 0:
                for folders_row in folders_rows:
                    folders_dict.update({folders_row[0]:folders_row[3]})
        else:
            raise LookupError("No folders found in FolderHierarchy table. Did you run a FolderSync yet?")
        return folders_dict