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


class code_page(object):
    """A code page is a map of tokens to tags"""
    def __init__(self, namespace=None, xmlns=None, index=None):
        self.namespace = namespace
        self.xmlns = xmlns
        self.index = index
        self.tokens = {}
        self.tags = {}

    def add(self, token, tag):
        self.tags.update({ token : tag })
        self.tokens.update({ tag : token })

    def get(self, t, token_or_tag):
        if t == 0:
            return get_token(token_or_tag)
        elif t == 1:
            return get_tag(token_or_tag)

    def get_token(self, tag):
        return self.tokens[tag]

    def get_tag(self, token):
        #print token, self.xmlns
        return self.tags[token]

    def __repr__(self):
        import pprint
        return "\r\n Namespace:%s - Xmlns:%s\r\n%s\r\n" % (self.namespace, self.xmlns, pprint.pformat(self.tokens))

    def __iter__(self):
        lnamespace = self.namespace
        lxmlns = self.xmlns
        for tag, token in self.tags.items():
            yield (lnamespace, lxmlns, tag, token)
