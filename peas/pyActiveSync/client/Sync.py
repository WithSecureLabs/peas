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

from ..objects.MSASCMD import FolderHierarchy
from ..objects.MSASEMAIL import parse_email
from ..objects.MSASCNTC import parse_contact
from ..objects.MSASCAL import parse_calendar
from ..objects.MSASTASK import parse_task
from ..objects.MSASNOTE import parse_note

class Sync:
    """'Sync' command builders and parsers"""
    class sync_response_collection:
        def __init__(self):
            self.SyncKey = 0
            self.CollectionId = None
            self.Status = 0
            self.MoreAvailable = None
            self.Commands = []
            self.Responses = None

    @staticmethod
    def build(synckeys, collections):
        as_sync_xmldoc_req = wapxmltree()
        xml_as_sync_rootnode = wapxmlnode("Sync")
        as_sync_xmldoc_req.set_root(xml_as_sync_rootnode, "airsync")

        xml_as_collections_node = wapxmlnode("Collections", xml_as_sync_rootnode)

        for collection_id in collections.keys():
            xml_as_Collection_node = wapxmlnode("Collection", xml_as_collections_node)  #http://msdn.microsoft.com/en-us/library/gg650891(v=exchg.80).aspx
            try:
                xml_as_SyncKey_node = wapxmlnode("SyncKey", xml_as_Collection_node, synckeys[collection_id])    #http://msdn.microsoft.com/en-us/library/gg663426(v=exchg.80).aspx
            except KeyError:
                xml_as_SyncKey_node = wapxmlnode("SyncKey", xml_as_Collection_node, "0")
                
            xml_as_CollectionId_node = wapxmlnode("CollectionId", xml_as_Collection_node, collection_id) #http://msdn.microsoft.com/en-us/library/gg650886(v=exchg.80).aspx

            for parameter in collections[collection_id].keys():
                if parameter == "Options":
                    xml_as_Options_node = wapxmlnode(parameter, xml_as_Collection_node)
                    for option_parameter in collections[collection_id][parameter].keys():
                        if option_parameter.startswith("airsync"):
                            for airsyncpref_node in collections[collection_id][parameter][option_parameter]:
                                xml_as_Options_airsyncpref_node = wapxmlnode(option_parameter.replace("_",":"), xml_as_Options_node)
                                wapxmlnode("airsyncbase:Type", xml_as_Options_airsyncpref_node, airsyncpref_node["Type"])
                                tmp = airsyncpref_node["Type"]
                                del airsyncpref_node["Type"]
                                for airsyncpref_parameter in airsyncpref_node.keys():
                                    wapxmlnode("airsyncbase:%s" % airsyncpref_parameter, xml_as_Options_airsyncpref_node, airsyncpref_node[airsyncpref_parameter])
                                airsyncpref_node["Type"] = tmp
                        elif option_parameter.startswith("rm"):
                            wapxmlnode(option_parameter.replace("_",":"), xml_as_Options_node, collections[collection_id][parameter][option_parameter])
                        else:
                            wapxmlnode(option_parameter, xml_as_Options_node, collections[collection_id][parameter][option_parameter])
                else:
                    wapxmlnode(parameter, xml_as_Collection_node, collections[collection_id][parameter])
        return as_sync_xmldoc_req

    @staticmethod
    def deepsearch_content_class(item):
        elements = item.get_children()
        for element in elements:
            if element.has_children():
                content_class = Sync.deepsearch_content_class(element)
                if content_class:
                    return content_class
            if (element.tag == "email:To") or (element.tag == "email:From"):
                return "Email"
            elif (element.tag == "contacts:FileAs") or (element.tag == "contacts:Email1Address"):
                return "Contacts"
            elif (element.tag == "calendar:Subject") or (element.tag == "calendar:UID"):
                return "Calendar"
            elif (element.tag == "tasks:Type"):
                return "Tasks"
            elif (element.tag == "notes:MessageClass"):
                return "Notes"

    @staticmethod
    def parse_item(item, collection_id, collectionid_to_type_dict = None):
        if collectionid_to_type_dict:
            try:
                content_class = FolderHierarchy.FolderTypeToClass[collectionid_to_type_dict[collection_id]]
            except:
                content_class = Sync.deepsearch_content_class(item)
        else:
            content_class = Sync.deepsearch_content_class(item)
        try:
            if content_class == "Email":
                return parse_email(item), content_class
            elif content_class == "Contacts":
                return parse_contact(item), content_class
            elif content_class == "Calendar":
                return parse_calendar(item), content_class
            elif content_class == "Tasks":
                return parse_task(item), content_class
            elif content_class == "Notes":
                return parse_note(item), content_class
        except Exception, e:
            if collectionid_to_type_dict:
                return Sync.parse_item(item, collection_id, None)
            else:
                print e
                pass
        raise LookupError("Could not determine content class of item for parsing. \r\n------\r\nItem:\r\n%s" % repr(item))

    @staticmethod
    def parse(wapxml, collectionid_to_type_dict = None):

        namespace = "airsync"
        root_tag = "Sync"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        airsyncbase_sync_children = root_element.get_children()
        if len(airsyncbase_sync_children) >  1:
            raise AttributeError("%s response does not conform to any known %s responses." % (root_tag, root_tag))
        if airsyncbase_sync_children[0].tag == "Status":
            if airsyncbase_sync_children[0].text == "4":
                print "Sync Status: 4, Protocol Error."
        if airsyncbase_sync_children[0].tag != "Collections":
            raise AttributeError("%s response does not conform to any known %s responses." % (root_tag, root_tag))

        response = []            

        airsyncbase_sync_collections_children = airsyncbase_sync_children[0].get_children()
        airsyncbase_sync_collections_children_count = len(airsyncbase_sync_collections_children)
        collections_counter = 0
        while collections_counter < airsyncbase_sync_collections_children_count:

            if airsyncbase_sync_collections_children[collections_counter].tag != "Collection":
                raise AttributeError("Sync response does not conform to any known Sync responses.")

            airsyncbase_sync_collection_children = airsyncbase_sync_collections_children[collections_counter].get_children()
            airsyncbase_sync_collection_children_count = len(airsyncbase_sync_collection_children)
            collection_counter = 0
            new_collection = Sync.sync_response_collection()
            while collection_counter < airsyncbase_sync_collection_children_count:
                if airsyncbase_sync_collection_children[collection_counter].tag == "SyncKey":
                    new_collection.SyncKey = airsyncbase_sync_collection_children[collection_counter].text
                elif airsyncbase_sync_collection_children[collection_counter].tag == "CollectionId":
                    new_collection.CollectionId = airsyncbase_sync_collection_children[collection_counter].text
                elif airsyncbase_sync_collection_children[collection_counter].tag == "Status":
                    new_collection.Status = airsyncbase_sync_collection_children[collection_counter].text
                    if new_collection.Status != "1":
                        response.append(new_collection)
                elif airsyncbase_sync_collection_children[collection_counter].tag == "MoreAvailable":
                    new_collection.MoreAvailable = True
                elif airsyncbase_sync_collection_children[collection_counter].tag == "Commands":
                    airsyncbase_sync_commands_children = airsyncbase_sync_collection_children[collection_counter].get_children()
                    airsyncbase_sync_commands_children_count = len(airsyncbase_sync_commands_children)
                    commands_counter = 0
                    while commands_counter < airsyncbase_sync_commands_children_count:
                        if airsyncbase_sync_commands_children[commands_counter].tag == "Add":
                            add_item = Sync.parse_item(airsyncbase_sync_commands_children[commands_counter], new_collection.CollectionId, collectionid_to_type_dict)
                            new_collection.Commands.append(("Add", add_item))
                        elif airsyncbase_sync_commands_children[commands_counter].tag == "Delete":
                            new_collection.Commands.append(("Delete", airsyncbase_sync_commands_children[commands_counter].get_children()[0].text))
                        elif airsyncbase_sync_commands_children[commands_counter].tag == "Change":
                            update_item = Sync.parse_item(airsyncbase_sync_commands_children[commands_counter], new_collection.CollectionId, collectionid_to_type_dict)
                            new_collection.Commands.append(("Change", update_item))
                        elif airsyncbase_sync_commands_children[commands_counter].tag == "SoftDelete":
                            new_collection.Commands.append(("SoftDelete", airsyncbase_sync_commands_children[commands_counter].get_children()[0].text))
                        commands_counter+=1
                elif airsyncbase_sync_collection_children[collection_counter].tag == "Responses":
                    print airsyncbase_sync_collection_children[collection_counter]
                collection_counter+=1
            response.append(new_collection)
            collections_counter+=1
        return response
