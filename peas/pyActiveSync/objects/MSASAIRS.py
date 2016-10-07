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

"""[MS-ASAIRS] AirSyncBase namespace objects"""

class airsyncbase_Type:             #http://msdn.microsoft.com/en-us/library/hh475675(v=exchg.80).aspx
    Plaintext = 1
    HTML =      2
    RTF =       3
    MIME =      4

class airsyncbase_NativeBodyType:   #http://msdn.microsoft.com/en-us/library/ee218276(v=exchg.80).aspx
    Plaintext = 1
    HTML =      2
    RTF =       3

class airsyncbase_Method:   #http://msdn.microsoft.com/en-us/library/ee160322(v=exchg.80).aspx
    Normal_attachment = 1   #Regular attachment
    Reserved1 =         2
    Reserved2 =         3
    Reserved3 =         4
    Embedded_message =  5   #Email with .eml extension
    Attach_OLE =        6   #OLE such as inline image

class airsyncbase_BodyPart_status:
    Success =   1
    Too_long =  176

class airsync_MIMESupport:
    Never =     0
    SMIMEOnly = 1
    Always =    2

class airsync_Class:
    Email =     "Email"
    Contacts =  "Contacts"
    Calendar =  "Calendar"
    Tasks =     "Tasks"
    Notes =     "Notes"
    SMS =       "SMS"

class airsync_FilterType:    #  Email | Calendar | Tasks
    NoFilter =          "0"  #    Y   |    Y     |   Y
    OneDay =            "1"  #    Y   |    N     |   N
    ThreeDays =         "2"  #    Y   |    N     |   N
    OneWeek =           "3"  #    Y   |    N     |   N
    TwoWeeks =          "4"  #    Y   |    Y     |   N
    OneMonth =          "5"  #    Y   |    Y     |   N
    ThreeMonths =       "6"  #    N   |    Y     |   N
    SixMonths =         "7"  #    N   |    Y     |   N
    IncompleteTasks =   "8"  #    N   |    N     |   Y

class airsync_Conflict:
    ClientReplacesServer = 0
    ServerReplacesClient = 1

class airsync_MIMETruncation:
    TruncateAll =       0
    Over4096chars =     1
    Over5120chars =     2
    Over7168chars =     3
    Over10240chars =    4
    Over20480chars =    5
    Over51200chars =    6
    Over102400chars =   7
    TruncateNone =      8

class airsyncbase_Body(object):
    def __init__(self):#, type, estimated_data_size=None, truncated=None, data=None, part=None, preview=None):
        self.airsyncbase_Type = None #type                                #Required. Integer. Max 1. See "MSASAIRS.Type" enum. 
        self.airsyncbase_EstimatedDataSize = None #estimated_data_size    #Optional. Integer. Max 1. Estimated data size before content filtering rules. http://msdn.microsoft.com/en-us/library/hh475714(v=exchg.80).aspx
        self.airsyncbase_Truncated = None #truncated                      #Optional. Boolean. Max 1. Specifies whether body is truncated as per airsync:BodyPreference element. http://msdn.microsoft.com/en-us/library/ee219390(v=exchg.80).aspx
        self.airsyncbase_Data = None #data                                #Optional. String (formated as per Type; RTF is base64 string). http://msdn.microsoft.com/en-us/library/ee202985(v=exchg.80).aspx
        self.airsyncbase_Part = None #part                                #Optional. Integer. See "MSASCMD.Part". Only present in multipart "MSASCMD.ItemsOperations" response. http://msdn.microsoft.com/en-us/library/hh369854(v=exchg.80).aspx
        self.airsyncbase_Preview = None #preview                          #Optional. String (unicode). Plaintext preview message. http://msdn.microsoft.com/en-us/library/ff849891(v=exchg.80).aspx
    def parse(self, imwapxml_airsyncbase_Body):
        body_elements = imwapxml_airsyncbase_Body.get_children()
        for element in body_elements:
            if element.tag == "airsyncbase:Type":
                self.airsyncbase_Type = element.text
            elif element.tag == "airsyncbase:EstimatedDataSize":
                self.airsyncbase_EstimatedDataSize = element.text
            elif element.tag == "airsyncbase:Truncated":
                self.airsyncbase_Truncated = element.text
            elif element.tag == "airsyncbase:Data":
                self.airsyncbase_Data = element.text
            elif element.tag == "airsyncbase:Part":
                self.airsyncbase_Part = element.text
            elif element.tag == "airsyncbase:Preview":
                self.airsyncbase_Preview = element.text
    def marshal(self):
        import base64
        return "%s//%s//%s//%s//%s//%s" % (repr(self.airsyncbase_Type), repr(self.airsyncbase_EstimatedDataSize), repr(self.airsyncbase_Truncated), base64.b64encode(self.airsyncbase_Data), repr(self.airsyncbase_Part), repr(self.airsyncbase_Preview))
    def __repr__(self):
        return self.marshal()

class airsyncbase_BodyPart(object):
    def __init__(self):
        self.airsyncbase_BodyPart_status = airsyncbase_BodyPart_status.Too_long #Required. Byte. See airsyncbase_BodyPart_status enum.
        self.airsyncbase_Type = airsyncbase_Type.HTML               #Required. Integer. Max 1. See "MSASAIRS.Type" enum. 
        self.airsyncbase_EstimatedDataSize = estimated_data_size    #Optional. Integer. Max 1. Estimated data size before content filtering rules. http://msdn.microsoft.com/en-us/library/hh475714(v=exchg.80).aspx
        self.airsyncbase_Truncated = truncated                      #Optional. Boolean. Max 1. Specifies whether body is truncated as per airsync:BodyPreference element. http://msdn.microsoft.com/en-us/library/ee219390(v=exchg.80).aspx
        self.airsyncbase_Data = data                                #Optional. String (formated as per Type; RTF is base64 string). http://msdn.microsoft.com/en-us/library/ee202985(v=exchg.80).aspx
        self.airsyncbase_Part = part                                #Optional. Integer. See "MSASCMD.Part". Only present in multipart "MSASCMD.ItemsOperations" response. http://msdn.microsoft.com/en-us/library/hh369854(v=exchg.80).aspx
        self.airsyncbase_Preview = preview                          #Optional. String (unicode). Plaintext preview message. http://msdn.microsoft.com/en-us/library/ff849891(v=exchg.80).aspx
    def parse(self, imwapxml_airsyncbase_BodyPart):
        bodypart_elements = imwapxml_airsyncbase_BodyPart.get_children()
        for element in bodypart_elements:
            if element.tag == "airsyncbase:Type":
                self.airsyncbase_Type = element.text
            elif element.tag == "airsyncbase:EstimatedDataSize":
                self.airsyncbase_EstimatedDataSize = element.text
            elif element.tag == "airsyncbase:Truncated":
                self.airsyncbase_Truncated = element.text
            elif element.tag == "airsyncbase:Data":
                self.airsyncbase_Data = element.text
            elif element.tag == "airsyncbase:Part":
                self.airsyncbase_Part = element.text
            elif element.tag == "airsyncbase:Preview":
                self.airsyncbase_Preview = element.text
            elif element.tag == "airsyncbase:Status":
                self.airsyncbase_BodyPart_status = element.text

class airsyncbase_Attachment(object): #Repsonse-only object.
    def __init__(self):#, file_reference, method, estimated_data_size, display_name=None, content_id=None, content_location = None, is_inline = None, email2_UmAttDuration=None, email2_UmAttOrder=None):
        self.airsyncbase_DisplayName = None #display_name                 #Optional. String. http://msdn.microsoft.com/en-us/library/ee160854(v=exchg.80).aspx
        self.airsyncbase_FileReference = None #file_reference             #Required. String. Location of attachment on server. http://msdn.microsoft.com/en-us/library/ff850023(v=exchg.80).aspx
        self.airsyncbase_Method = None #method                            #Required. Byte. See "MSASAIRS.Method". Type of attachment. http://msdn.microsoft.com/en-us/library/ee160322(v=exchg.80).aspx
        self.airsyncbase_EstimatedDataSize = None #estimated_data_size    #Required. Integer. Max 1. Estimated data size before content filtering rules. http://msdn.microsoft.com/en-us/library/hh475714(v=exchg.80).aspx
        self.airsyncbase_ContentId = None #content_id                     #Optional. String. Max 1. Unique object id of attachment - informational only.
        self.airsyncbase_ContentLocation = None #content_location         #Optional. String. Max 1. Contains the relative URI for an attachment, and is used to match a reference to an inline attachment in an HTML message to the attachment in the attachments table. http://msdn.microsoft.com/en-us/library/ee204563(v=exchg.80).aspx
        self.airsyncbase_IsInline = None #is_inline                       #Optional. Boolean. Max 1. Specifies whether the attachment is embedded in the message. http://msdn.microsoft.com/en-us/library/ee237093(v=exchg.80).aspx
        self.email2_UmAttDuration = None #email2_UmAttDuration            #Optional. Integer. Duration of the most recent electronic voice mail attachment in seconds. Only used in "IPM.Note.Microsoft.Voicemail", "IPM.Note.RPMSG.Microsoft.Voicemail", or "IPM.Note.Microsoft.Missed.Voice".
        self.email2_UmAttOrder = None #email2_UmAttOrder                  #Optional. Integer. Order of electronic voice mail attachments. Only used in "IPM.Note.Microsoft.Voicemail", "IPM.Note.RPMSG.Microsoft.Voicemail", or "IPM.Note.Microsoft.Missed.Voice".
    def parse(self, imwapxml_airsyncbase_Attachment):
        attachment_elements = imwapxml_airsyncbase_Attachment.get_children()
        for element in attachment_elements:
            if element.tag == "airsyncbase:DisplayName":
                self.airsyncbase_DisplayName = element.text
            elif element.tag == "airsyncbase:FileReference":
                self.airsyncbase_FileReference = element.text
            elif element.tag == "airsyncbase:Method":
                self.airsyncbase_Method = element.text
            elif element.tag == "airsyncbase:EstimatedDataSize":
                self.airsyncbase_EstimatedDataSize = element.text
            elif element.tag == "airsyncbase:ContentId":
                self.airsyncbase_ContentId = element.text
            elif element.tag == "airsyncbase:ContentLocation":
                self.airsyncbase_ContentLocation = element.text
            elif element.tag == "airsyncbase:IsInline":
                self.airsyncbase_IsInline = element.text
            elif element.tag == "email2:UmAttDuration":
                self.email2_UmAttDuration = element.text
            elif element.tag == "email2:UmAttOrder":
                self.email2_UmAttOrder = element.text
    def marshal(self):
        import base64
        return base64.b64encode("%s//%s//%s//%s//%s//%s//%s//%s//%s" % (repr(self.airsyncbase_DisplayName), repr(self.airsyncbase_FileReference), repr(self.airsyncbase_Method), repr(self.airsyncbase_EstimatedDataSize), repr(self.airsyncbase_ContentId),repr(self.airsyncbase_ContentLocation), repr(self.airsyncbase_IsInline), repr(self.email2_UmAttDuration),repr(self.email2_UmAttOrder)))
    def __repr__(self):
        return self.marshal()

class airsyncbase_Attachments:
    @staticmethod
    def parse(inwapxml_airsyncbase_Attachments):
        attachment_elements = inwapxml_airsyncbase_Attachments.get_children()
        attachments = []
        for attachment in attachment_elements:
            new_attachment = airsyncbase_Attachment()
            new_attachment.parse(attachment)
            attachments.append(new_attachment)
        return attachments




    
