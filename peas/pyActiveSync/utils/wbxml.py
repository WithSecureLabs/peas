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


from wapxml import wapxmltree, wapxmlnode

class wbxml_parser(object):
    """WBXML Parser"""

    VERSION_BYTE =              0x03
    PUBLIC_IDENTIFIER_BYTE =    0x01
    CHARSET_BYTE =              0x6A #Currently, only UTF-8 is used by MS-ASWBXML
    STRING_TABLE_LENGTH_BYTE =  0x00 #String tables are not used by MS-ASWBXML

    class GlobalTokens:
        SWITCH_PAGE = 0x00  
        END         = 0x01
        ENTITY      = 0x02 #Not used by MS-ASWBXML
        STR_I       = 0x03
        LITERAL     = 0x04 
        EXT_I_0     = 0x40 #Not used by MS-ASWBXML
        EXT_I_1     = 0x41 #Not used by MS-ASWBXML
        EXT_I_2     = 0x42 #Not used by MS-ASWBXML
        PI          = 0x43 #Not used by MS-ASWBXML
        LITERAL_C   = 0x44 #Not used by MS-ASWBXML
        EXT_T_0     = 0x80 #Not used by MS-ASWBXML
        EXT_T_1     = 0x81 #Not used by MS-ASWBXML
        EXT_T_2     = 0x82 #Not used by MS-ASWBXML
        STR_T       = 0x83 #Not used by MS-ASWBXML
        LITERAL_A   = 0x84 #Not used by MS-ASWBXML
        EXT_0       = 0xC0 #Not used by MS-ASWBXML
        EXT_1       = 0xC1 #Not used by MS-ASWBXML
        EXT_2       = 0xC2 #Not used by MS-ASWBXML
        OPAQUE      = 0xC3
        LITERAL_AC  = 0xC4 #Not used by MS-ASWBXML

    def __init__(self, code_pages, cp_shorthand={}):
        self.wapxml = None
        self.wbxml = None
        self.pointer = 0
        self.code_pages = code_pages
        self.cp_shorthand = cp_shorthand
        return

    def encode(self, inwapxml=None):
        wbxml_bytes = bytearray()

        if not inwapxml: return wbxml_bytes

        #add headers
        wbxml_bytes.append(self.VERSION_BYTE)
        wbxml_bytes.extend(self.encode_multibyte_integer(self.PUBLIC_IDENTIFIER_BYTE))
        wbxml_bytes.extend(self.encode_multibyte_integer(self.CHARSET_BYTE))
        wbxml_bytes.extend(self.encode_multibyte_integer(self.STRING_TABLE_LENGTH_BYTE))

        #add code_page/xmlns
        wbxml_bytes.append(self.GlobalTokens.SWITCH_PAGE)
        current_code_page_index = self.encode_xmlns_as_codepage(inwapxml.get_root().get_xmlns())
        wbxml_bytes.append(current_code_page_index)
        self.current_code_page = self.code_pages[current_code_page_index]
        self.default_code_page = self.code_pages[current_code_page_index]

        #add root token/tag
        token_tag = self.current_code_page.get_token(inwapxml.get_root().tag)
        if inwapxml.get_root().has_children():
            token_tag |= 0x40
        wbxml_bytes.append(token_tag)

        current_node = inwapxml.get_root()

        if current_node.has_children():
            for child in current_node.get_children():
                self.encode_node_recursive(child, wbxml_bytes)
        wbxml_bytes.append(self.GlobalTokens.END)
        return wbxml_bytes

    def encode_node_recursive(self, current_node, wbxml_bytes):
        if ":" in current_node.tag:
            split_xmlns_tag = current_node.tag.split(":")
            possibly_new_code_page = self.code_pages[self.encode_xmlns_as_codepage(split_xmlns_tag[0])]
            if possibly_new_code_page.index != self.current_code_page.index:
                wbxml_bytes.append(self.GlobalTokens.SWITCH_PAGE)
                wbxml_bytes.append(possibly_new_code_page.index)
                self.current_code_page = possibly_new_code_page
            token_tag = self.current_code_page.get_token(split_xmlns_tag[1])
        else:
            if self.current_code_page.index != self.default_code_page.index:
                wbxml_bytes.append(self.GlobalTokens.SWITCH_PAGE)
                wbxml_bytes.append(self.default_code_page.index)
                self.current_code_page = self.code_pages[self.default_code_page.index]
            token_tag = self.current_code_page.get_token(current_node.tag)
        token_tag |= 0x40
        wbxml_bytes.append(token_tag)
        #text, cdata = None, None
        if current_node.text:
            wbxml_bytes.append(self.GlobalTokens.STR_I)
            wbxml_bytes.extend(self.encode_string(current_node.text))
        elif current_node.cdata:
            wbxml_bytes.append(self.GlobalTokens.OPAQUE)
            if current_node.tag == "Mime":
                wbxml_bytes.extend(self.encode_string_as_opaquedata(current_node.cdata.as_string()))
            else: #ConversationMode or ConversationId
                wbxml_bytes.extend(self.encode_hexstring_as_opaquedata(current_node.cdata))
        if current_node.has_children():
            for child in current_node.get_children():
                self.encode_node_recursive(child, wbxml_bytes)   #will have to use class var for current_code_page since stack is being replaced on recursive iter
        wbxml_bytes.append(self.GlobalTokens.END)
    
    def decode(self, inwbxml=None):
        if inwbxml:
            self.wbxml = bytearray()
            self.wbxml.extend(inwbxml)
        elif not self.wbxml:
            raise AttributeError("Cannot decode if no wbxml. wbxml must be passed to decode as wbxml_parser.decode(inwbxml), or bytearray() must be set directly at wbxml_parser.wbxml.")
        self.pointer = 0
        ver = self.decode_byte()
        public_id = self.decode_multibyte_integer()
        charset = self.decode_multibyte_integer()
        string_table_len = self.decode_multibyte_integer()

        if charset is not 0x6A:
            raise AttributeError("Currently, only UTF-8 is used by MS-ASWBXML")
            return
        if string_table_len > 0:
            raise AttributeError("String tables are not used by MS-ASWBXML")
            return

        wapxmldoc = wapxmltree()
        current_element = None
        first_iter = True

        byte = self.decode_byte()
        if byte is not self.GlobalTokens.SWITCH_PAGE:
            if self.default_code_page:
                default_code_page = self.default_code_page
                self.pointer-=1
            else:
                raise AttributeError("No first or default code page defined.")
        else:
            default_code_page = self.code_pages[self.decode_byte()]
        root_element = wapxmlnode("?")
        current_code_page = default_code_page
        root_element.set_xmlns(current_code_page.xmlns)
        wapxmldoc.set_root(root_element, root_element.get_xmlns())
        current_element = root_element

        temp_xmlns = ""


        while self.pointer < len(inwbxml):
            byte = self.decode_byte()
            if byte is self.GlobalTokens.SWITCH_PAGE:
                current_code_page = self.code_pages[self.decode_byte()]
                if current_code_page != default_code_page:
                    temp_xmlns = current_code_page.xmlns + ":"
                else:
                    temp_xmlns = ""
            elif byte is self.GlobalTokens.END:
                if not current_element.is_root():
                    current_element = current_element.get_parent()
                else:
                    if self.pointer < len(self.wbxml):
                        raise EOFError("END token incorrectly placed after root node.")
                    else:
                        return wapxmldoc
            elif byte is self.GlobalTokens.STR_I:
                current_element.text = self.decode_string()
            elif byte is self.GlobalTokens.OPAQUE:
                opq_len = self.decode_byte()
                opq_str = ""
                if current_element.tag == "Mime":
                    opq_str = self.decode_string(opq_len)
                else:
                    import binascii
                    opq_str = binascii.hexlify(self.decode_binary(opq_len))
                current_element.text = opq_str
            else:
                if byte & 0x80 > 0:
                    raise AttributeError("Token has attributes. MS-ASWBXML does not use attributes.")
                token = byte & 0x3f
                tag_token = temp_xmlns + current_code_page.get_tag(token)
                if not first_iter:
                    new_element = wapxmlnode(tag_token, current_element)
                    if (byte & 0x40): #check to see if new element has children 
                        current_element = new_element
                elif current_element.is_root():
                    current_element.tag = tag_token
                    first_iter = False
                else:
                    raise IndexError("Missing root element.")
        return wapxmldoc


    # encode helper functions
    def encode_xmlns_as_codepage(self, inxmlns_or_namespace):
        lc_inxmlns = inxmlns_or_namespace.lower()
        for cp_index, code_page in self.code_pages.items():
            if code_page.xmlns == lc_inxmlns:
                return cp_index
        if inxmlns_or_namespace in self.cp_shorthand.keys():
            lc_inxmlns = self.cp_shorthand[inxmlns_or_namespace].lower()
            for cp_index, code_page in self.code_pages.items():
                if code_page.xmlns == lc_inxmlns:
                    return cp_index
        raise IndexError("No such code page exists in current object")

    def encode_string(self, string):
        string = str(string)
        retarray = bytearray(string, "utf-8")
        retarray.append("\x00")
        return retarray

    def encode_string_as_opaquedata(self, string):
        retarray = bytearray()
        retarray.extend(self.encode_multibyte_integer(len(string)))
        retarray.extend(bytearray(string, "utf-8"))
        return retarray

    def encode_hexstring_as_opaquedata(self, hexstring):
        retarray = bytearray()
        retarray.extend(self.encode_multibyte_integer(len(hexstring)))
        retarray.extend(hexstring)
        return retarray

    def encode_multibyte_integer(self, integer):
        retarray = bytearray()
        if integer == 0:
            retarray.append(integer)
            return retarray
        last = True
        while integer > 0:
            if last:
                retarray.append( integer & 0x7f )
                last = False
            else:
                retarray.append( ( integer & 0x7f ) | 0x80 )
            integer = integer >> 7
        retarray.reverse()
        return retarray

    # decode helper functions
    def decode_codepages_as_xmlns(self):
        return

    def decode_string(self, length=None):
        retarray = bytearray()
        if length is None:
            #terminator = b"\x00"
            while self.wbxml[self.pointer] != 0:#terminator:
                retarray.append(self.wbxml[self.pointer])
                self.pointer += 1
            self.pointer+=1
        else:
            for i in range(0, length):
                retarray.append(self.wbxml[self.pointer])
                self.pointer+=1
        return str(retarray)

    def decode_byte(self):
        self.pointer+=1
        return self.wbxml[self.pointer-1]

    def decode_multibyte_integer(self):
        #print "indices: ", self.pointer, "of",  len(self.wbxml)
        if self.pointer >= len(self.wbxml):
            raise IndexError("wbxml is truncated. nothing left to decode") 
        integer = 0
        while ( self.wbxml[self.pointer] & 0x80 ) != 0:
            integer = integer << 7
            integer = integer + ( self.wbxml[self.pointer] & 0x7f )
            self.pointer += 1
        integer = integer << 7
        integer = integer + ( self.wbxml[self.pointer] & 0x7f )
        self.pointer += 1
        return integer

    def decode_binary(self, length=0):
        retarray = bytearray()
        for i in range(0, length):
            retarray.append(self.wbxml[self.pointer])
            self.pointer+=1
        return retarray
