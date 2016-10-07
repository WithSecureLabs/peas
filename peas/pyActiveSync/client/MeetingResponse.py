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

class MeetingResponse:
    """description of class"""

    @staticmethod
    def build(responses):
        meetingresponse_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("MeetingResponse")
        meetingresponse_xmldoc_req.set_root(xmlrootnode, "meetingresponse")
        for response in responses:
            xmlrequestnode = wapxmlnode("Request", xmlrootnode)
            xmluserresponsenode = wapxmlnode("UserResponse", xmlrequestnode, response["UserResponse"])
            if response.has_Key("CollectionId"):
                xmlcollectionidnode = wapxmlnode("CollectionId", xmlrequestnode, response["CollectionId"])
                xmlrequestidnode = wapxmlnode("RequestId", xmlrequestnode, response["RequestId"])
            elif response.has_Key("LongId"):
                xmllongidnode = wapxmlnode("search:LongId", xmlrequestnode, response["LongId"])
            else:
                raise AttributeError("MeetingResponse missing meeting id")
            xmlinstanceidnode = wapxmlnode("InstanceId", xmlrequestnode, response["InstanceId"])
        return meetingresponse_xmldoc_req

    @staticmethod
    def parse(wapxml):

        namespace = "meetingresponse"
        root_tag = "MeetingResponse"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        meetingresponse_meetingresponse_children = root_element.get_children()

        responses = []

        for element in meetingresponse_meetingresponse_children:
            if element.tag is "Result":
                result_elements = element.get_children()
                for result_element in result_elements:
                    request_id = None
                    calendar_id = None
                    if result_element.tag == "RequestId":
                        request_id = result_element.text
                    elif result_element.tag == "Status":
                        status = result_element.text
                    elif result_element.tag == "CalendarId":
                        calendar_id = result_element.text
                responses.append(status, request_id, calendar_id)
            else:
                raise AttributeError("MeetingResponse error. Server returned unknown element instead of 'Result'.")
        return responses

