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
import base64

class ValidateCert:
    """http://msdn.microsoft.com/en-us/library/gg675590(v=exchg.80).aspx"""

    @staticmethod
    def build(certificate, certificate_chain_list=[], pre_encoded = False, check_crl = True):
        validatecert_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("ValidateCert")
        validatecert_xmldoc_req.set_root(xmlrootnode, "validatecert")
        if len(certificate_chain_list) > 0:
            xmlcertchainnode = wapxmlnode("CertificateChain", xmlrootnode)
            for cert in certificate_chain_list:
                if pre_encoded:
                    wapxmlnode("Certificate", xmlcertchainnode, cert)
                else:
                    wapxmlnode("Certificate", xmlcertchainnode, base64.b64encode(cert))
        xmlcertsnode = wapxmlnode("Certificates", xmlrootnode)
        if pre_encoded:
            xmlcertnode = wapxmlnode("Certificate", xmlcertsnode, certificate)
        else:
            xmlcertnode = wapxmlnode("Certificate", xmlcertsnode, base64.b64encode(certificate))
        if check_crl:
            xmlcertsnode = wapxmlnode("CheckCRL", xmlrootnode, "1")
        return validatecert_xmldoc_req

    @staticmethod
    def parse(wapxml):

        namespace = "validatecert"
        root_tag = "ValidateCert"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        validatecert_validatecert_status = None
        validatecert_validatecert_cert_status = None

        for element in validatecert_validatecert_children:
            if element.tag is "Status":
                validatecert_validatecert_status = element.text
                if validatecert_validatecert_status != "1":
                    print "ValidateCert Exception: %s" % validatecert_validatecert_status
            elif element.tag == "Certificate":
                validatecert_validatecert_cert_status = element.get_children()[0].text
        return (validatecert_validatecert_status, validatecert_validatecert_cert_status)


