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

class MoveItems(object):
    """http://msdn.microsoft.com/en-us/library/gg675499(v=exchg.80).aspx"""

    @staticmethod
    def build(moves):
        if len(moves) < 1:
            raise AttributeError("MoveItems builder: No moves supplied to MoveItems request builder.")
        moveitems_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("MoveItems")
        moveitems_xmldoc_req.set_root(xmlrootnode, "move")
        for move in moves:
            xmlmovenode = wapxmlnode("Move", xmlrootnode)
            src_msg_id, src_fld_id, dst_fld_id = move
            xmlsrcmsgidnode = wapxmlnode("SrcMsgId", xmlmovenode, src_msg_id)
            xmlsrcfldidnode = wapxmlnode("SrcFldId", xmlmovenode, src_fld_id)
            xmldstfldidnode = wapxmlnode("DstFldId", xmlmovenode, dst_fld_id)
        return moveitems_xmldoc_req

    @staticmethod
    def parse(wapxml):

        namespace = "move"
        root_tag = "MoveItems"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        move_moveitems_children = root_element.get_children()

        responses = []

        for response_element in move_moveitems_children:
            src_id = ""
            status = ""
            dst_id = ""
            for element in response_element:
                if element.tag is "Status":
                    status = element.text
                    if status != "3":
                         print "MoveItems Exception: %s" % status
                elif element.tag == "SrcMsgId":
                    src_id = element.text
                elif element.tag == "DstMsgId":
                    dst_id = element.text
            responses.append((src_id, status, dst_id))

        return responses


