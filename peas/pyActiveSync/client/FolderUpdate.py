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

class FolderUpdate:
    """http://msdn.microsoft.com/en-us/library/ee160573(v=exchg.80).aspx"""

    @staticmethod
    def build(synckey, server_id, parent_id, display_name):
        folderupdate_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("FolderUpdate")
        folderupdate_xmldoc_req.set_root(xmlrootnode, "folderhierarchy")
        xmlsynckeynode = wapxmlnode("SyncKey", xmlrootnode, synckey)
        xmlserveridnode = wapxmlnode("ServerId", xmlrootnode, server_id)
        xmlparentidnode = wapxmlnode("ParentId", xmlrootnode, parent_id)
        xmldisplaynamenode = wapxmlnode("DisplayName", xmlrootnode, display_name)
        return folderupdate_xmldoc_req

    @staticmethod
    def parse(wapxml):

        namespace = "folderhierarchy"
        root_tag = "FolderUpdate"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        folderhierarchy_folderupdate_children = root_element.get_children()

        folderhierarchy_folderupdate_status = None
        folderhierarchy_folderupdate_synckey = None
        folderhierarchy_folderupdate_serverid = None

        for element in folderhierarchy_folderupdate_children:
            if element.tag is "Status":
                folderhierarchy_folderupdate_status = element.text
                if folderhierarchy_folderupdate_status != "1":
                     print "FolderUpdate Exception: %s" % folderhierarchy_folderupdate_status
            elif element.tag == "SyncKey":
                folderhierarchy_folderupdate_synckey = element.text
        return (folderhierarchy_folderupdate_status, folderhierarchy_folderupdate_synckey)