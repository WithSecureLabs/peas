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

from ..utils.wapxml import wapxmltree, wapxmlnode

from ..objects.MSASAIRS import airsyncbase_Body, airsyncbase_BodyPart

class ItemOperations:
    """http://msdn.microsoft.com/en-us/library/ee202415(v=exchg.80).aspx"""

    @staticmethod
    def build(operations):
        itemoperations_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("ItemOperations")
        itemoperations_xmldoc_req.set_root(xmlrootnode, "itemoperations")

        for operation in range(0,len(operations)):
            if operations[operation]["Name"] == "EmptyFolderContents":
                xmlemptyfoldercontentsnode = wapxmlnode("EmptyFolderContents", xmlrootnode)
                xmlcollectionidnode = wapxmlnode("airsync:CollectionId", xmlemptyfoldercontentsnode, operations[operation]["CollectionId"])
                if operations[operation].has_key("DeleteSubFolders"):
                    xmloptionsnode = wapxmlnode("Options", xmlemptyfoldercontentsnode)
                    xmldeletesubfoldersnode = wapxmlnode("DeleteSubFolders", xmloptionsnode, operations[operation]["DeleteSubFolders"])

            elif operations[operation]["Name"] == "Fetch":
                xmlfetchnode = wapxmlnode("Fetch", xmlrootnode)
                xmloptionsnode = wapxmlnode("Store", xmlfetchnode, operations[operation]["Store"])
                if operations[operation].has_key("LinkId"):
                    xmllinkidnode = wapxmlnode("documentlibrary:LinkId", xmlfetchnode, operations[operation]["LinkId"]) #URI of document
                if operations[operation].has_key("LongId"):
                    xmllongidnode = wapxmlnode("search:LongId", xmlfetchnode, operations[operation]["LongId"])
                if operations[operation].has_key("CollectionId"):
                    xmlcollectionidnode = wapxmlnode("airsync:CollectionId", xmlfetchnode, operations[operation]["CollectionId"])
                if operations[operation].has_key("ServerId"):
                    xmlserveridnode = wapxmlnode("airsync:ServerId", xmlfetchnode, operations[operation]["ServerId"])
                if operations[operation].has_key("FileReference"):
                    xmlfilereferencenode = wapxmlnode("airsyncbase:FileReference", xmlfetchnode, operations[operation]["FileReference"]) #only range option can be specified
                if operations[operation].has_key("RemoveRightsManagementProtection"):
                    xmlremovermnode = wapxmlnode("rm:RemoveRightsManagementProtection", xmlfetchnode) #Empty element
                if len(xmlfetchnode.get_children()) < 2: #let's make sure one of the above item locations was supplied
                    raise AttributeError("ItemOperations Fetch: No item to be fetched supplied.")

                xmloptionsnode = wapxmlnode("Options")
                if operations[operation].has_key("Schema"):
                    xmlschemanode = wapxmlnode("Schema", xmloptionsnode, operations[operation]["Schema"]) #fetch only specific properties of an item. mailbox store only. cannot use for attachments.
                if operations[operation].has_key("Range"):
                    xmlrangenode = wapxmlnode("Range", xmloptionsnode, operations[operation]["Range"]) #select bytes is only for documents and attachments
                if operations[operation].has_key("UserName"): #select username and password to use for fetch. i imagine this is  only for documents.
                    if not operations[operation].has_key("Password"):
                        raise AttributeError("ItemOperations Fetch: Username supplied for fetch operation, but no password supplied. Aborting.")
                        return
                    xmlusernamenode = wapxmlnode("UserName", xmloptionsnode, operations[operation]["UserName"]) #username to use for fetch
                    xmlpasswordnode = wapxmlnode("Password", xmloptionsnode, operations[operation]["Password"]) #password to use for fetch
                if operations[operation].has_key("MIMESupport"):
                    xmlmimesupportnode = wapxmlnode("airsync:MIMESupport", xmloptionsnode, operations[operation]["MIMESupport"]) #objects.MSASAIRS.airsync_MIMESupport
                if operations[operation].has_key("BodyPreference"):
                    xmlbodypreferencenode = wapxmlnode("airsyncbase:BodyPreference", xmloptionsnode, operations[operation]["BodyPreference"])
                if operations[operation].has_key("BodyPartPreference"):
                    xmlbodypartpreferencenode = wapxmlnode("airsyncbase:BodyPartPreference", xmloptionsnode, operations[operation]["BodyPartPreference"])
                if operations[operation].has_key("RightsManagementSupport"):
                    xmlrmsupportnode = wapxmlnode("rm:RightsManagementSupport", xmloptionsnode, operations[operation]["RightsManagementSupport"])#1=Supports RM. Decrypt message before send. 2=Do not decrypt message before send 
                if len(xmloptionsnode.get_children()) > 0:
                    xmloptionsnode.set_parent(xmlfetchnode)

            elif operations[operation]["Name"] == "Move":
                xmlmovenode = wapxmlnode("Move", xmlrootnode)
                xmlconversationidnode = wapxmlnode("ConversationId", xmlmovenode, operations[operation]["ConversationId"])
                xmldstfldidnode = wapxmlnode("DstFldId", xmlmovenode, operations[operation]["DstFldId"])
                if operations[operation].has_key("MoveAlways"):
                    xmloptionsnode = wapxmlnode("Options", xmlmovenode)
                    xmlmovealwaysnode = wapxmlnode("MoveAlways", xmloptionsnode, operations[operation]["MoveAlways"]) #also move future emails in this conversation to selected folder.
            else:
               raise AttributeError("Unknown operation %s submitted to ItemOperations wapxml builder." % operation)

        return itemoperations_xmldoc_req

    @staticmethod
    def parse(wapxml):

        namespace = "itemoperations"
        root_tag = "ItemOperations"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        itemoperations_itemoperations_children = root_element.get_children()

        itemoperations_itemoperations_status = None

        responses = []

        for element in itemoperations_itemoperations_children:
            if element.tag is "Status":
                itemoperations_itemoperations_status = element.text
                if itemoperations_itemoperations_status != "1":
                    print "FolderSync Exception: %s" % itemoperations_itemoperations_status
            elif element.tag == "Response":
                response_elements = element.get_children()
                for response_element in response_elements:
                    if response_element.tag == "EmptyFolderContents":
                        efc_elements = response_element.get_children()
                        for efc_element in efc_elements:
                            if efc_element.tag == "Status":
                                efc_status = efc_element.text
                            elif efc_element.tag == "airsync:CollectionId":
                                efc_collectionid = efc_element.text
                        responses.append(("EmptyFolderContents", efc_status, efc_collectionid))
                    elif response_element.tag == "Fetch":
                        fetch_elements = response_element.get_children()
                        fetch_id = None
                        fetch_properties = None
                        fetch_class = None
                        for fetch_element in fetch_elements:
                            if fetch_element.tag == "Status":
                                fetch_status = fetch_element.text
                            elif fetch_element.tag == "search:LongId":
                                fetch_id = fetch_element.text
                            elif fetch_element.tag == "airsync:CollectionId":
                                fetch_id = fetch_element.text
                            elif fetch_element.tag == "airsync:ServerId":
                                fetch_id = fetch_element.text
                            elif fetch_element.tag == "documentlibrary:LinkId":
                                fetch_id = fetch_element.text
                            elif fetch_element.tag == "airsync:Class":
                                fetch_class = fetch_element.text
                            elif fetch_element.tag == "Properties":
                                property_elements = fetch_element.get_children()
                                fetch_properties = {}
                                for property_element in property_elements:
                                    if property_element.tag == "Range":
                                        fetch_properties.update({ "Range" : property_element.text })
                                    elif property_element.tag == "Data":
                                        fetch_properties.update({ "Data" : property_element.text })
                                    elif property_element.tag == "Part":
                                        fetch_properties.update({ "Part" : property_element.text })
                                    elif property_element.tag == "Version": #datetime
                                        fetch_properties.update({ "Version" : property_element.text })
                                    elif property_element.tag == "Total":
                                        fetch_properties.update({ "Total" : property_element.text })
                                    elif property_element.tag == "airsyncbase:Body":
                                        fetch_properties.update({ "Body" : airsyncbase_Body(property_element) })
                                    elif property_element.tag == "airsyncbase:BodyPart":
                                        fetch_properties.update({ "BodyPart" : airsyncbase_BodyPart(property_element) })
                                    elif property_element.tag == "rm:RightsManagementLicense":
                                        fetch_properties.update({ "RightsManagementLicense" : property_element }) #need to create rm license parser
                        responses.append(("Fetch", fetch_status, fetch_id, fetch_properties, fetch_class))
                    elif response_element.tag == "Move":
                        move_elements = response_element.get_children()
                        for move_element in move_elements:
                            if move_element.tag == "Status":
                                move_status = move_element.text
                            elif move_element.tag == "ConversationId":
                                move_conversationid = move_element.text
                        responses.append(("Move", move_status, move_conversationid))
        return responses