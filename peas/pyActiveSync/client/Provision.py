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

class Provision:
    """http://msdn.microsoft.com/en-us/library/ff850179(v=exchg.80).aspx"""

    @staticmethod
    def build(policykey, settings=None):
        provision_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("Provision")
        provision_xmldoc_req.set_root(xmlrootnode, "provision")

        if policykey == "0":
            xml_settings_deviceinformation_node = wapxmlnode("settings:DeviceInformation", xmlrootnode)
            xml_settings_set_node = wapxmlnode("settings:Set", xml_settings_deviceinformation_node)
            xml_settings_model_node = wapxmlnode("settings:Model", xml_settings_set_node, settings["Model"])
            xml_settings_model_node = wapxmlnode("settings:IMEI", xml_settings_set_node, settings["IMEI"])
            xml_settings_model_node = wapxmlnode("settings:FriendlyName", xml_settings_set_node, settings["FriendlyName"])
            xml_settings_model_node = wapxmlnode("settings:OS", xml_settings_set_node, settings["OS"])
            xml_settings_model_node = wapxmlnode("settings:OSLanguage", xml_settings_set_node, settings["OSLanguage"])
            xml_settings_model_node = wapxmlnode("settings:PhoneNumber", xml_settings_set_node, settings["PhoneNumber"])
            xml_settings_model_node = wapxmlnode("settings:MobileOperator", xml_settings_set_node, settings["MobileOperator"])
            xml_settings_model_node = wapxmlnode("settings:UserAgent", xml_settings_set_node, settings["UserAgent"])

            xml_policies_node = wapxmlnode("Policies", xmlrootnode)
            xml_policy_node = wapxmlnode("Policy", xml_policies_node)
            xml_policytype_node = wapxmlnode("PolicyType", xml_policy_node, "MS-EAS-Provisioning-WBXML")
        else:
            xml_policies_node = wapxmlnode("Policies", xmlrootnode)
            xml_policy_node = wapxmlnode("Policy", xml_policies_node)
            xml_policytype_node = wapxmlnode("PolicyType", xml_policy_node, "MS-EAS-Provisioning-WBXML")
            xml_policytype_node = wapxmlnode("PolicyKey", xml_policy_node, policykey)
            xml_policytype_node = wapxmlnode("Status", xml_policy_node, "1")

        return provision_xmldoc_req

    @staticmethod
    def parse(wapxml):
        
        namespace = "provision"
        root_tag = "Provision"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        provison_provison_children = root_element.get_children()

        policy_dict = {}
        settings_status = ""
        policy_status = ""
        policy_key = "0"
        policy_type = ""
        status = ""

        for element in provison_provison_children:
            if element.tag is "Status":
                status = element.text
                if (status != "1") and (status != "2"):
                     print "Provision Exception: %s" % status
            elif element.tag == "Policies":
                policy_elements = element.get_children()[0].get_children()
                for policy_element in policy_elements:
                    if policy_element.tag == "PolicyType":
                        policy_type = policy_element.text
                    elif policy_element.tag == "Status":
                        policy_status = policy_element.text
                    elif policy_element.tag == "PolicyKey":
                        policy_key = policy_element.text
                    elif policy_element.tag == "Data":
                        eas_provision_elements = policy_element.get_children()[0].get_children()
                        for eas_provision_element in eas_provision_elements:
                            if eas_provision_element.tag == "AllowBluetooth":
                                policy_dict.update({"AllowBluetooth":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowBluetooth":
                                policy_dict.update({"AllowBluetooth":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowBrowser":
                                policy_dict.update({"AllowBrowser":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowCamera":
                                policy_dict.update({"AllowCamera":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowConsumerEmail":
                                policy_dict.update({"AllowConsumerEmail":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowDesktopSync":
                                policy_dict.update({"AllowDesktopSync":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowHTMLEmail":
                                policy_dict.update({"AllowHTMLEmail":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowInternetSharing":
                                policy_dict.update({"AllowInternetSharing":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowIrDA":
                                policy_dict.update({"AllowIrDA":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowPOPIMAPEmail":
                                policy_dict.update({"AllowPOPIMAPEmail":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowRemoteDesktop":
                                policy_dict.update({"AllowRemoteDesktop":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowSimpleDevicePassword":
                                policy_dict.update({"AllowSimpleDevicePassword":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowSMIMEEncryptionAlgorithmNegotiation":
                                policy_dict.update({"AllowSMIMEEncryptionAlgorithmNegotiation":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowSMIMESoftCerts":
                                policy_dict.update({"AllowSMIMESoftCerts":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowStorageCard":
                                policy_dict.update({"AllowStorageCard":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowTextMessaging":
                                policy_dict.update({"AllowTextMessaging":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowUnsignedApplications":
                                policy_dict.update({"AllowUnsignedApplications":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowUnsignedInstallationPackages":
                                policy_dict.update({"AllowUnsignedInstallationPackages":eas_provision_element.text})
                            elif eas_provision_element.tag == "AllowWifi":
                                policy_dict.update({"AllowWifi":eas_provision_element.text})
                            elif eas_provision_element.tag == "AlphanumericDevicePasswordRequired":
                                policy_dict.update({"AlphanumericDevicePasswordRequired":eas_provision_element.text})
                            elif eas_provision_element.tag == "ApprovedApplicationList":
                                policy_dict.update({"ApprovedApplicationList":eas_provision_element.text})
                            elif eas_provision_element.tag == "AttachmentsEnabled":
                                policy_dict.update({"AttachmentsEnabled":eas_provision_element.text})
                            elif eas_provision_element.tag == "DevicePasswordEnabled":
                                policy_dict.update({"DevicePasswordEnabled":eas_provision_element.text})
                            elif eas_provision_element.tag == "DevicePasswordExpiration":
                                policy_dict.update({"DevicePasswordExpiration":eas_provision_element.text})
                            elif eas_provision_element.tag == "DevicePasswordHistory":
                                policy_dict.update({"DevicePasswordHistory":eas_provision_element.text})
                            elif eas_provision_element.tag == "MaxAttachmentSize":
                                policy_dict.update({"MaxAttachmentSize":eas_provision_element.text})
                            elif eas_provision_element.tag == "MaxCalendarAgeFilter":
                                policy_dict.update({"MaxCalendarAgeFilter":eas_provision_element.text})
                            elif eas_provision_element.tag == "MaxDevicePasswordFailedAttempts":
                                policy_dict.update({"MaxDevicePasswordFailedAttempts":eas_provision_element.text})
                            elif eas_provision_element.tag == "MaxEmailAgeFilter":
                                policy_dict.update({"MaxEmailAgeFilter":eas_provision_element.text})
                            elif eas_provision_element.tag == "MaxEmailBodyTruncationSize":
                                policy_dict.update({"MaxEmailBodyTruncationSize":eas_provision_element.text})
                            elif eas_provision_element.tag == "MaxEmailHTMLBodyTruncationSize":
                                policy_dict.update({"MaxEmailHTMLBodyTruncationSize":eas_provision_element.text})
                            elif eas_provision_element.tag == "MaxInactivityTimeDeviceLock":
                                policy_dict.update({"MaxInactivityTimeDeviceLock":eas_provision_element.text})
                            elif eas_provision_element.tag == "MinDevicePasswordComplexCharacters":
                                policy_dict.update({"MinDevicePasswordComplexCharacters":eas_provision_element.text})
                            elif eas_provision_element.tag == "MinDevicePasswordLength":
                                policy_dict.update({"MinDevicePasswordLength":eas_provision_element.text})
                            elif eas_provision_element.tag == "PasswordRecoveryEnabled":
                                policy_dict.update({"PasswordRecoveryEnabled":eas_provision_element.text})
                            elif eas_provision_element.tag == "RequireDeviceEncryption":
                                policy_dict.update({"RequireDeviceEncryption":eas_provision_element.text})
                            elif eas_provision_element.tag == "RequireEncryptedSMIMEMessages":
                                policy_dict.update({"RequireEncryptedSMIMEMessages":eas_provision_element.text})
                            elif eas_provision_element.tag == "RequireEncryptionSMIMEAlgorithm":
                                policy_dict.update({"RequireEncryptionSMIMEAlgorithm":eas_provision_element.text})
                            elif eas_provision_element.tag == "RequireManualSyncWhenRoaming":
                                policy_dict.update({"RequireManualSyncWhenRoaming":eas_provision_element.text})
                            elif eas_provision_element.tag == "RequireSignedSMIMEAlgorithm":
                                policy_dict.update({"RequireSignedSMIMEAlgorithm":eas_provision_element.text})
                            elif eas_provision_element.tag == "RequireSignedSMIMEMessages":
                                policy_dict.update({"RequireSignedSMIMEMessages":eas_provision_element.text})
                            elif eas_provision_element.tag == "RequireStorageCardEncryption":
                                policy_dict.update({"RequireStorageCardEncryption":eas_provision_element.text})
                            elif eas_provision_element.tag == "UnapprovedInROMApplicationList":
                                policy_dict.update({"UnapprovedInROMApplicationList":eas_provision_element.text})
            elif element.tag == "settings:DeviceInformation":
                device_information_children = element.get_children()
                for device_information_element in device_information_children:
                    if device_information_element == "settings:Status":
                        settings_status = device_information_element.text
        return (status, policy_status, policy_key, policy_type, policy_dict, settings_status)