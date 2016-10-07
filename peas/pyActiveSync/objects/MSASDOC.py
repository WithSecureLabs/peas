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

"""[MS-ASDOC] Document objects"""

@staticmethod
def parse_document(data):
    document_dict = {}
    document_base = data.get_children()
    document_dict.update({"server_id" : document_base[0].text})
    document_elements = document_base[1].get_children()
    for element in document_elements:
        if element.tag == "documentlibrary:ContentLength":
            document_dict.update({ "documentlibrary_ContentLength" : element.text })
        elif element.tag == "documentlibrary:ContentType":
            document_dict.update({ "documentlibrary_ContentType" : element.text })
        elif element.tag == "documentlibrary:CreationDate":
            document_dict.update({ "documentlibrary_CreationDate" : element.text })
        elif element.tag == "documentlibrary:DisplayName":
            document_dict.update({ "documentlibrary_DisplayName" : element.text })
        elif element.tag == "documentlibrary:IsFolder":
            document_dict.update({ "documentlibrary_IsFolder" : element.text })
        elif element.tag == "documentlibrary:IsHidden":
            document_dict.update({ "documentlibrary_IsHidden" : element.text })
        elif element.tag == "documentlibrary:LastModifiedDate":
            document_dict.update({ "documentlibrary_LastModifiedDate" : element.text })
        elif element.tag == "documentlibrary:LinkId":
            document_dict.update({ "documentlibrary_LinkId" : element.text })
    return document_dict