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

class SmartReply:
    """http://msdn.microsoft.com/en-us/library/ee217283(v=exchg.80).aspx"""

    @staticmethod
    def build(client_id, source, mime, replace_mime=False, save_in_sent_items=True, template_id=None):
        smartreply_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("SmartReply")
        smartreply_xmldoc_req.set_root(xmlrootnode, "composemail")
        xml_clientid_node = wapxmlnode("ClientId", xmlrootnode, client_id)
        xml_source_node = wapxmlnode("Source", xmlrootnode)
        if source.has_key("FolderId"):
            wapxmlnode("FolderId", xml_source_node, source["FolderId"])
        if source.has_key("ItemId"):
            wapxmlnode("ItemId", xml_source_node, source["ItemId"])
        if source.has_key("LongId"):
            wapxmlnode("LongId", xml_source_node, source["LongId"]) 
        if source.has_key("InstanceId"):
            wapxmlnode("InstanceId", xml_source_node, source["InstanceId"])        
        xml_accountid_node = wapxmlnode("AccountId", xmlrootnode, display_name)
        xml_saveinsentiems_node = wapxmlnode("SaveInSentItems", xmlrootnode, str(int(save_in_sent_items)))
        if replace_mime:
            xml_replacemime_node = wapxmlnode("ReplaceMime", xmlrootnode)
        xml_mime_node = wapxmlnode("Mime", xmlrootnode, mime)
        xml_templateid_node = wapxmlnode("rm:TemplateID", xmlrootnode, template_id)
        return smartreply_xmldoc_req

    @staticmethod
    def parse(wapxml):

        namespace = "composemail"
        root_tag = "SmartReply"
       
        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        smartreply_children = root_element.get_children()

        status = None

        for element in smartreply_children:
            if element.tag is "Status":
                status = element.text
        return status

