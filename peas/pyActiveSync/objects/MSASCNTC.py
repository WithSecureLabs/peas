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

"""[MS-ASCNTC] Contact objects"""

from MSASEMAIL import airsyncbase_Body

def parse_contact(data):
    contact_dict = {}
    contact_base = data.get_children()
    contact_dict.update({"server_id" : contact_base[0].text})
    contact_elements = contact_base[1].get_children()
    for element in contact_elements:
        if element.tag == "contacts2:AccountName":
            contact_dict.update({ "contacts2_AccountName" : element.text })
        elif element.tag == "contacts:Alias":
            contact_dict.update({ "contacts_Alias" : element.text })
        elif element.tag == "contacts:Anniversary":
            contact_dict.update({ "contacts_Anniversary" : element.text })
        elif element.tag == "contacts:AssistantName":
            contact_dict.update({ "contacts_AssistantName" : element.text })
        elif element.tag == "contacts:AssistantPhoneNumber":
            contact_dict.update({ "contacts_AssistantPhoneNumber" : element.text })
        elif element.tag == "contacts:Birthday":
            contact_dict.update({ "contacts_Birthday" : element.text })
        elif element.tag == "airsyncbase:Body":
            body = airsyncbase_Body()
            body.parse(element)
            contact_dict.update({ "airsyncbase_Body" : body })
        elif element.tag == "contacts:BusinessAddressCity":
            contact_dict.update({ "contacts_BusinessAddressCity" : element.text })
        elif element.tag == "contacts:BusinessAddressCountry":
            contact_dict.update({ "contacts_BusinessAddressCountry" : element.text })
        elif element.tag == "contacts:BusinessAddressPostalCode":
            contact_dict.update({ "contacts_BusinessAddressPostalCode" : element.text })
        elif element.tag == "contacts:BusinessAddressState":
            contact_dict.update({ "contacts_BusinessAddressState" : element.text })
        elif element.tag == "contacts:BusinessAddressStreet":
            contact_dict.update({ "contacts_BusinessAddressStreet" : element.text })
        elif element.tag == "contacts:BusinessFaxNumber":
            contact_dict.update({ "contacts_BusinessFaxNumber" : element.text })
        elif element.tag == "contacts:BusinessPhoneNumber":
            contact_dict.update({ "contacts_BusinessPhoneNumber" : element.text })
        elif element.tag == "contacts:Business2PhoneNumber":
            contact_dict.update({ "contacts_Business2PhoneNumber" : element.text })
        elif element.tag == "contacts:CarPhoneNumber":
            contact_dict.update({ "contacts_CarPhoneNumber" : element.text })
        elif element.tag == "contacts:Categories":
            categories_list = []
            categories = element.get_children()
            for category_element in categories:
                categories_list.append(category_element.text)
            contact_dict.update({ "contacts_Categories" : categories_list })
        elif element.tag == "contacts:Children":
            children_list = []
            children = element.get_children()
            for child_element in children:
                children_list.append(child_element.text)
            contact_dict.update({ "contacts_Children" : children_list })
        elif element.tag == "contacts2:CompanyMainPhone":
            contact_dict.update({ "contacts2_CompanyMainPhone" : element.text })
        elif element.tag == "contacts:CompanyName":
            contact_dict.update({ "contacts_CompanyName" : element.text })
        elif element.tag == "contacts2:CustomerId":
            contact_dict.update({ "contacts2_CustomerId" : element.text })
        elif element.tag == "contacts:Department":
            contact_dict.update({ "contacts_Department" : element.text })
        elif element.tag == "contacts:Email1Address":
            contact_dict.update({ "contacts_Email1Address" : element.text })
        elif element.tag == "contacts:Email2Address":
            contact_dict.update({ "contacts_Email2Address" : element.text })
        elif element.tag == "contacts:Email3Address":
            contact_dict.update({ "contacts_Email3Address" : element.text })
        elif element.tag == "contacts:FileAs":
            contact_dict.update({ "contacts_FileAs" : element.text })
        elif element.tag == "contacts:FirstName":
            contact_dict.update({ "contacts_FirstName" : element.text })
        elif element.tag == "contacts2:GovernmentId":
            contact_dict.update({ "contacts2_GovernmentId" : element.text })
        elif element.tag == "contacts:HomeAddressCity":
            contact_dict.update({ "contacts_HomeAddressCity" : element.text })
        elif element.tag == "contacts:HomeAddressCountry":
            contact_dict.update({ "contacts_HomeAddressCountry" : element.text })
        elif element.tag == "contacts:HomeAddressPostalCode":
            contact_dict.update({ "contacts_HomeAddressPostalCode" : element.text })
        elif element.tag == "contacts:HomeAddressState":
            contact_dict.update({ "contacts_HomeAddressState" : element.text })
        elif element.tag == "contacts:HomeAddressStreet":
            contact_dict.update({ "contacts_HomeAddressStreet" : element.text })
        elif element.tag == "contacts:HomeFaxNumber":
            contact_dict.update({ "contacts_HomeFaxNumber" : element.text })
        elif element.tag == "contacts:HomePhoneNumber":
            contact_dict.update({ "contacts_HomePhoneNumber" : element.text })
        elif element.tag == "contacts:Home2PhoneNumber":
            contact_dict.update({ "contacts_Home2PhoneNumber" : element.text })
        elif element.tag == "contacts2:IMAddress":
            contact_dict.update({ "contacts2_IMAddress" : element.text })
        elif element.tag == "contacts2:IMAddress2":
            contact_dict.update({ "contacts2_IMAddress2" : element.text })
        elif element.tag == "contacts2:IMAddress3":
            contact_dict.update({ "contacts_IMAddress3" : element.text })
        elif element.tag == "contacts:JobTitle":
            contact_dict.update({ "contacts_JobTitle" : element.text })
        elif element.tag == "contacts:LastName":
            contact_dict.update({ "contacts_LastName" : element.text })
        elif element.tag == "contacts2:ManagerName":
            contact_dict.update({ "contacts2_ManagerName" : element.text })
        elif element.tag == "contacts:MiddleName":
            contact_dict.update({ "contacts_MiddleName" : element.text })
        elif element.tag == "contacts2:MMS":
            contact_dict.update({ "contacts2_MMS" : element.text })
        elif element.tag == "contacts:MobilePhoneNumber":
            contact_dict.update({ "contacts_MobilePhoneNumber" : element.text })
        elif element.tag == "contacts2:NickName":
            contact_dict.update({ "contacts2_NickName" : element.text })
        elif element.tag == "contacts:OfficeLocation":
            contact_dict.update({ "contacts_OfficeLocation" : element.text })
        elif element.tag == "contacts:OtherAddressCity":
            contact_dict.update({ "contacts_OtherAddressCity" : element.text })
        elif element.tag == "contacts:OtherAddressCountry":
            contact_dict.update({ "contacts_OtherAddressCountry" : element.text })
        elif element.tag == "contacts:OtherAddressPostalCode":
            contact_dict.update({ "contacts_OtherAddressPostalCode" : element.text })
        elif element.tag == "contacts:OtherAddressState":
            contact_dict.update({ "contacts_OtherAddressState" : element.text })
        elif element.tag == "contacts:OtherAddressStreet":
            contact_dict.update({ "contacts_OtherAddressStreet" : element.text })
        elif element.tag == "contacts:PagerNumber":
            contact_dict.update({ "contacts_PagerNumber" : element.text })
        elif element.tag == "contacts:Picture":
            contact_dict.update({ "contacts_Picture" : element.text })
        elif element.tag == "contacts:RadioPhoneNumber":
            contact_dict.update({ "contacts_RadioPhoneNumber" : element.text })
        elif element.tag == "contacts:Spouse":
            contact_dict.update({ "contacts_Spouse" : element.text })
        elif element.tag == "contacts:Suffix":
            contact_dict.update({ "contacts_Suffix" : element.text })
        elif element.tag == "contacts:Title":
            contact_dict.update({ "contacts_Title" : element.text })
        elif element.tag == "contacts:WebPage":
            contact_dict.update({ "contacts_WebPage" : element.text })
        elif element.tag == "contacts:WeightedRank":
            contact_dict.update({ "contacts_WeightedRank" : element.text })
        elif element.tag == "contacts:YomiCompanyName":
            contact_dict.update({ "contacts_YomiCompanyName" : element.text })
        elif element.tag == "contacts:YomiFirstName":
            contact_dict.update({ "contacts_YomiFirstName" : element.text })
        elif element.tag == "contacts:YomiLastName":
            contact_dict.update({ "contacts_YomiLastName" : element.text })
    return contact_dict