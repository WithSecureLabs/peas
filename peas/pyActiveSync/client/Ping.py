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

class Ping(object):
    """http://msdn.microsoft.com/en-us/library/gg675609(v=exchg.80).aspx"""

    @staticmethod
    def build(heatbeat_interval="30", folders=None):
        if not folders:
            raise AttributeError("Ping builder: No folders included in ping request builder. Must ping at least one folder.")
        ping_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("Ping")
        ping_xmldoc_req.set_root(xmlrootnode, "ping")
        xmlheartbeatintervalnode = wapxmlnode("HeartbeatInterval", xmlrootnode, heatbeat_interval)
        xmlfoldersnode = wapxmlnode("Folders", xmlrootnode)
        for folder in folders:
            xmlfoldernode = wapxmlnode("Folder", xmlfoldersnode)
            xmlidnode = wapxmlnode("Id", xmlfoldernode, folder[0])
            xmlclassnode = wapxmlnode("Class", xmlfoldernode, folder[1])
        return ping_xmldoc_req

    @staticmethod
    def parse(wapxml):

        namespace = "ping"
        root_tag = "Ping"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        ping_ping_children = root_element.get_children()

        heartbeat_interval = ""
        status = ""
        folders = []
        max_folders = ""

        for element in ping_ping_children:
            if element.tag is "Status":
                status = element.text
                if (status != "1") and (status != "2"):
                     print "Ping Exception: %s" % status
            elif element.tag == "HeartbeatInterval":
                heartbeat_interval = element.text
            elif element.tag == "MaxFolders":
                max_folders = element.text
            elif element.tag == "Folders":
                folders_list = element.get_children()
                if len(folders_list) > 0:
                    for folder in folders_list:
                        folders.append(folder.text)
        return (status, heartbeat_interval, max_folders, folders)

