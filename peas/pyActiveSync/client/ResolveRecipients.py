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

class ResolveRecipients:
    """http://msdn.microsoft.com/en-us/library/gg650949(v=exchg.80).aspx"""

    @staticmethod
    def build(to, cert_retrieval=0, max_certs=9999, max_recipients=9999, start_time=None, end_time=None, max_picture_size=100, max_pictures=9999):
        resolverecipients_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("ResolveRecipients")
        resolverecipients_xmldoc_req.set_root(xmlrootnode, "resolverecipients")
        xmltonode = wapxmlnode("To", xmlrootnode, to)
        #xmloptionsnode = wapxmlnode("Options", xmlrootnode)
        #xmlcertificateretrievalnode = wapxmlnode("CertificateRetrieval", xmloptionsnode, cert_retrieveal)
        #xmlmaxcertificatesnode = wapxmlnode("MaxCertificates", xmloptionsnode, max_certs)                       #0-9999
        #xmlmaxambiguousrecipientsnode = wapxmlnode("MaxAmbiguousRecipients", xmloptionsnode, max_recipients)    #0-9999
        #xmlavailabilitynode = wapxmlnode("Availability", xmloptionsnode)
        #xmlstarttimenode = wapxmlnode("StartTime", xmlavailabilitynode, start_time) #datetime
        #xmlendtimenode = wapxmlnode("EndTime", xmlavailabilitynode, end_time) #datetime
        #xmlpicturenode = wapxmlnode("Picture", xmloptionsnode)
        #xmlmaxsizenode = wapxmlnode("MaxSize", xmlpicturenode, max_size) #must be > 100KB
        #xmlmaxpicturesnode = wapxmlnode("MaxPictures", xmlpicturenode, max_pictures)
        return resolverecipients_xmldoc_req

    @staticmethod
    def parse(wapxml):

        namespace = "resolverecipients"
        root_tag = "ResolveRecipients"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        folderhierarchy_resolverecipients_children = root_element.get_children()

        recipients = []

        for element in folderhierarchy_resolverecipients_children:
            if element.tag is "Status":
                folderhierarchy_resolverecipients_status = element.text
                if folderhierarchy_resolverecipients_status != "1":
                     print "ResolveRecipients Status: %s" % folderhierarchy_resolverecipients_status
            elif element.tag == "Response":
                for response_element in element.get_children():
                    if response_element.tag == "To":
                        response_to = response_element.text
                    elif response_element.tag == "Status":
                        response_status = response_element.text
                    elif response_element.tag == "RecipientCount":
                        response_count = response_element.text
                    elif response_element.tag == "Recipient":
                        response_status = response_element.text
                        for recipient_element in response_element.get_children():
                            if recipient_element.tag == "Type":
                                recipient_type = recipient_element.text
                            elif recipient_element.tag == "DisplayName":
                                recipient_displayname = recipient_element.text
                            elif recipient_element.tag == "EmailAddress":
                                recipient_emailaddress = recipient_element.text
                            elif recipient_element.tag == "Availability":
                                recipient_availability = recipient_element
                            elif recipient_element.tag == "Certificates":
                                recipient_certificates = recipient_element
                            elif recipient_element.tag == "Picture":
                                recipient_picture = recipient_element.text
                            recipients.append((recipient_type, recipient_displayname, recipient_emailaddress, recipient_availability, recipient_certificates, recipient_picture))

        return (response_status, recipients, response_count)