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

class FolderSync:
    """http://msdn.microsoft.com/en-us/library/ee237648(v=exchg.80).aspx"""

    @staticmethod
    def build(synckey):
        foldersync_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("FolderSync")
        foldersync_xmldoc_req.set_root(xmlrootnode, "folderhierarchy")
        xmlsynckeynode = wapxmlnode("SyncKey", xmlrootnode, synckey)
        return foldersync_xmldoc_req

    @staticmethod
    def parse(wapxml):

        namespace = "folderhierarchy"
        root_tag = "FolderSync"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        folderhierarchy_foldersync_children = root_element.get_children()
        if len(folderhierarchy_foldersync_children) >  3:
            raise AttributeError("%s response does not conform to any known %s responses." % (root_tag, root_tag))
        #if folderhierarchy_foldersync_children[0].tag != "Collections":
        #    raise AttributeError("%s response does not conform to any known %s responses." % (root_tag, root_tag))

        folderhierarchy_foldersync_status = None
        folderhierarchy_foldersync_synckey = None
        folderhierarchy_foldersync_changes = None

        changes = []

        for element in folderhierarchy_foldersync_children:
            if element.tag is "Status":
                folderhierarchy_foldersync_status = element.text
                if folderhierarchy_foldersync_status != "1":
                    print "FolderSync Exception: %s" % folderhierarchy_foldersync_status
            elif element.tag == "SyncKey":
                folderhierarchy_foldersync_synckey = element.text
            elif element.tag == "Changes":
                folderhierarchy_foldersync_changes = element.get_children()
                folderhierarchy_foldersync_changes_count = int(folderhierarchy_foldersync_changes[0].text)
                if folderhierarchy_foldersync_changes_count > 0:
                    for change_index in range(1, folderhierarchy_foldersync_changes_count+1):
                        folderhierarchy_foldersync_change_element = folderhierarchy_foldersync_changes[change_index]
                        folderhierarchy_foldersync_change_childern = folderhierarchy_foldersync_change_element.get_children()
                        new_change = FolderHierarchy.Folder()
                        for element in folderhierarchy_foldersync_change_childern:
                            if element.tag == "ServerId":
                                new_change.ServerId = element.text
                            elif element.tag == "ParentId":
                                new_change.ParentId = element.text
                            elif element.tag == "DisplayName":
                                new_change.DisplayName = element.text
                            elif element.tag == "Type":
                                new_change.Type = element.text
                        changes.append((folderhierarchy_foldersync_change_element.tag, new_change))
        return (changes, folderhierarchy_foldersync_synckey, folderhierarchy_foldersync_status)