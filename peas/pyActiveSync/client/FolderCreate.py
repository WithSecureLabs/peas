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

class FolderCreate:
    """http://msdn.microsoft.com/en-us/library/gg650949(v=exchg.80).aspx"""

    @staticmethod
    def build(synckey, parent_id, display_name, _type):
        foldercreate_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("FolderCreate")
        foldercreate_xmldoc_req.set_root(xmlrootnode, "folderhierarchy")
        xmlsynckeynode = wapxmlnode("SyncKey", xmlrootnode, synckey)
        xmlparentidnode = wapxmlnode("ParentId", xmlrootnode, parent_id)
        xmldisplaynamenode = wapxmlnode("DisplayName", xmlrootnode, display_name)
        xmltypenode = wapxmlnode("Type", xmlrootnode, _type) #See objects.MSASCMD.FolderHierarchy.FolderCreate.Type
        return foldercreate_xmldoc_req

    @staticmethod
    def parse(wapxml):

        namespace = "folderhierarchy"
        root_tag = "FolderCreate"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        folderhierarchy_foldercreate_children = root_element.get_children()

        folderhierarchy_foldercreate_status = None
        folderhierarchy_foldercreate_synckey = None
        folderhierarchy_foldercreate_serverid = None

        for element in folderhierarchy_foldercreate_children:
            if element.tag is "Status":
                folderhierarchy_foldercreate_status = element.text
                if folderhierarchy_foldercreate_status != "1":
                     print "FolderCreate Exception: %s" % folderhierarchy_foldercreate_status
            elif element.tag == "SyncKey":
                folderhierarchy_foldercreate_synckey = element.text
            elif element.tag == "ServerId":
                folderhierarchy_foldercreate_serverid = element.text
        return (folderhierarchy_foldercreate_status, folderhierarchy_foldercreate_synckey, folderhierarchy_foldercreate_serverid)