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

"""[MS-ASNOTE] Note objects"""

from MSASEMAIL import airsyncbase_Body

def parse_note(data):
    note_dict = {}
    note_base = data.get_children()
    note_dict.update({"server_id" : note_base[0].text})
    note_elements = note_base[1].get_children()
    for element in note_elements:
        if element.tag == "airsyncbase:Body":
            body = airsyncbase_Body()
            body.parse(element)
            note_dict.update({ "airsyncbase_Body" : body })
        elif element.tag == "notes:Subject":
            note_dict.update({ "notes_Subject" : element.text })
        elif element.tag == "notes:MessageClass":
            note_dict.update({ "notes_MessageClass" : element.text })
        elif element.tag == "notes:LastModifiedDate":
            note_dict.update({ "notes_LastModifiedDate" : element.text })
        elif element.tag == "notes:Categories":
            categories_list = []
            categories = element.get_children()
            for category_element in categories:
                categories_list.append(category_element.text)
            note_dict.update({ "notes_Categories" : categories_list })
    return note_dict