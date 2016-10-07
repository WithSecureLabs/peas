########################################################################
#  Modified 2016 from code copyright (C) 2013 Sol Birnbaum
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


class wapxmltree(object):
    def __init__(self, inwapxmlstr=None):
        self.header = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
        self._root_node = None
        if inwapxmlstr:
            self.parse_string(inwapxmlstr)
        return
    def parse_string(self, xmlstr):
        return
    def set_root(self, root_node, xmlns):
        self._root_node = root_node
        self._root_node.set_root(True, xmlns, self)
    def get_root(self):
        return self._root_node
    def __repr__(self):
        if self._root_node:
            return self.header + repr(self._root_node)


class wapxmlnode(object):
    def __init__(self, tag, parent=None, text=None, cdata=None):
        self.tag = tag
        self.text = text
        self.cdata = cdata
        self._children = []
        self._is_root = None
        self._xmlns = None
        self._parent = None
        if parent:
            try:
                self.set_parent(parent)
            except Exception, e:
                print e
    def set_parent(self, parent):
        parent.add_child(self)
        self._parent = parent
    def get_parent(self):
        return self._parent
    def add_child(self, child):
        self._children.append(child)
    def remove_child(self, child):
        self._children.remove(child)
    def set_root(self, true_or_false, xmlns=None, parent=None):
        self._is_root = true_or_false
        self._xmlns = xmlns
        self._parent = parent
    def is_root(self):
        return self._is_root
    def set_xmlns(self, xmlns):
        self._xmlns = xmlns
    def get_xmlns(self):
        return self._xmlns
    def has_children(self):
        if len(self._children) > 0:
            return True
        else:
            return False
    def get_children(self):
        return self._children

    def basic_xpath(self, tag_path):
        """Get all the children with the final tag name after following the tag path list e.g. search/results."""

        tag_path = tag_path.split('/')

        results = []
        for child in self._children:
            if child.tag == tag_path[0]:
                if len(tag_path) == 1:
                    results.append(child)
                else:
                    results.extend(child.basic_xpath('/'.join(tag_path[1:])))
        return results

    def __repr__(self, tabs="  "):
        if (self.text != None) or (self.cdata != None) or (len(self._children)>0):
            inner_text = ""
            if self.text != None:
                inner_text+=str(self.text)
            if self.cdata != None:
                inner_text+= "<![CDATA[%s]]>" % str(self.cdata)
            if self.has_children():
                for child in self._children:
                    inner_text+=child.__repr__(tabs+"  ")
            if not self._is_root:
                end_tabs = ""
                if self.has_children(): end_tabs = "\r\n"+tabs
                return "\r\n%s<%s>%s%s</%s>" % (tabs, self.tag, inner_text, end_tabs, self.tag)
            else: return  "\r\n<%s xmlns=\"%s:\">%s\r\n</%s>" % (self.tag, self._xmlns, inner_text, self.tag)
        elif self._is_root:
            return "\r\n<%s xmlns=\"%s:\"></%s>" % (self.tag, self._xmlns, self.tag)
        else:
            return "%s<%s />" % (tabs, self.tag)
    def __iter__(self):
        if len(self._children) > 0:
            for child in self._children:
                yield child
    def __str__(self):
        return self.__repr__()
                    




