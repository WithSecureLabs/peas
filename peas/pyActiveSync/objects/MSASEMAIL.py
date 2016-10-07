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

"""[MS-ASEMAIL] Email class namespace objects"""

from MSASAIRS import airsyncbase_Type, airsyncbase_Body, airsyncbase_Attachment, airsyncbase_Attachments, airsyncbase_Method, airsyncbase_NativeBodyType, airsyncbase_BodyPart

class email_Importance:
    Low =    0
    Normal = 1
    High =   2

class email_MessageClass:                     #http://msdn.microsoft.com/en-us/library/ee200767(v=exchg.80).aspx
    IPM_Note =                          "IPM.Note"                         #Normal e-mail message.
    IPM_Note_SMIME =                    "IPM.Note.SMIME"                   #The message is encrypted and can also be signed.
    IPM_Note_SMIME_MultipartSigned =    "IPM.Note.SMIME.MultipartSigned"   #The message is clear signed.
    IPM_Note_Receipt_SMIME =            "IPM.Note.Receipt.SMIME"           #The message is a secure read receipt.
    IPM_InfoPathForm =                  "IPM.InfoPathForm"                 #An InfoPath form.
    IPM_Schedule_Meeting =              "IPM.Schedule.Meeting"             #Meeting request.
    IPM_Notification_Meeting =          "IPM.Notification.Meeting"         #Meeting notification.
    IPM_Post =                          "IPM.Post"                         #Post.
    IPM_Octel_Voice =                   "IPM.Octel.Voice"                  #Octel voice message.
    IPM_Voicenotes =                    "IPM.Voicenotes"                   #Electronic voice notes.
    IPM_Sharing =                       "IPM.Sharing"                      #Shared message.

    REPORT_IPM_NOTE_NDR =                           "REPORT.IPM.NOTE.NDR"                       #Non-delivery report for a standard message.
    REPORT_IPM_NOTE_DR =                            "REPORT.IPM.NOTE.DR"                        #Delivery receipt for a standard message.
    REPORT_IPM_NOTE_DELAYED =                       "REPORT.IPM.NOTE.DELAYED"                   #Delivery receipt for a delayed message.
    REPORT_IPM_NOTE_IPNRN =                         "REPORT.IPM.NOTE.IPNRN"                     #Read receipt for a standard message.
    REPORT_IPM_NOTE_IPNNRN =                        "REPORT.IPM.NOTE.IPNNRN"                    #Non-read receipt for a standard message.
    REPORT_IPM_SCHEDULE_MEETING_REQUEST_NDR =       "REPORT.IPM.SCHEDULE.MEETING.REQUEST.NDR"   #Non-delivery report for a meeting request.
    REPORT_IPM_SCHEDULE_MEETING_RESP_POS_NDR =      "REPORT.IPM.SCHEDULE.MEETING.RESP.NDR"      #Non-delivery report for a positive meeting response (accept).
    REPORT_IPM_SCHEDULE_MEETING_RESP_TENT_NDR =     "REPORT.IPM.SCHEDULE.MEETING.TENT.NDR"      #Non-delivery report for a Tentative meeting response.
    REPORT_IPM_SCHEDULE_MEETING_CANCELED_NDR =      "REPORT.IPM.SCHEDULE.MEETING.CANCELED.NDR"  #Non-delivery report for a cancelled meeting notification.
    REPORT_IPM_NOTE_SMIME_NDR =                     "REPORT.IPM.NOTE.SMIME.NDR"                 #Non-delivery report for a Secure MIME (S/MIME) encrypted and opaque-signed message.
    REPORT_IPM_NOTE_SMIME_DR =                      "REPORT.IPM.NOTE.SMIME.DR"                  #Delivery receipt for an S/MIME encrypted and opaque-signed message.
    REPORT_IPM_NOTE_SMIME_MULTIPARTSIGNED_NDR =     "REPORT.IPM.NOTE.SMIME.MULTIPARTSIGNED.NDR" #Non-delivery report for an S/MIME clear-signed message.
    REPORT_IPM_NOTE_SMIME_MULTIPARTSIGNED_DR =      "REPORT.IPM.NOTE.SMIME.MULTIPARTSIGNED.DR"  #Delivery receipt for an S/MIME clear-signed message.

class email_InstanceType:
    Single =              0
    Recurring_Master =    1
    Recurring_Instance =  2
    Recurring_Exception = 3


class email_Type: #Recurrence type            #http://msdn.microsoft.com/en-us/library/ee203639(v=exchg.80).aspx
    Daily =                             0
    Weekly =                            1
    Monthly_Nth_day =                   2
    Monthly =                           3
    Yearly_Nth_day_Nth_month =          4
    Yearly_Nth_day_of_week_Nth_month =  5

class email2_CalendarType:                 #http://msdn.microsoft.com/en-us/library/ee625428(v=exchg.80).aspx
    Default =                       0
    Gregorian =                     1
    Gregorian_US =                  2
    Japan =                         3 
    Tiawan =                        4
    Korea =                         5
    Hijri =                         6
    Thai =                          7
    Hebrew =                        8
    GregorianMeFrench =             9
    Gregorian_Arabic =              10
    Gregorian_translated_English =  11
    Gregorian_translated_French =   12
    Japanese_Lunar =                13
    Chinese_Lunar =                 14
    Korean_Lunar =                  15

class email_DayOfWeek:
    Sunday =    1
    Monday =    2
    Tuesday =   4
    Wednesday = 8
    Thursday =  16
    Friday =    32
    Saturday =  64

class email2_FirstDayOfWeek:
    Sunday =    0
    Monday =    1
    Tuesday =   2
    Wednesday = 2
    Thursday =  4
    Friday =    4
    Saturday =  6

class email_Sensitivity:
    Normal =        0
    Personal =      1
    Private =       2 
    Confidential =  3

class email_BusyStatus:
    Free =          0
    Tentative =     1
    Busy =          2
    OutOfOffice =   3

class email_Flag_status:
    Cleared =   0
    Complete =  1
    Active =    2

class email2_MeetingMessageType:    #http://msdn.microsoft.com/en-us/library/ff631404(v=exchg.80).aspx
    Silent =            0           #A silent update was performed, or the message type is unspecified.
    Initial =           1           #Initial meeting request.
    Full =              2           #Full update.
    Informational =     3           #Informational update.
    Outdated =          4           #Outdated. A newer meeting request or meeting update was received after this message.
    Delegators_Copy =   5           #Identifies the delegator's copy of the meeting request.
    Delegated =         6           #Identifies that the meeting request has been delegated and the meeting request MUST NOT be responded to.

class email2_LastVerbExecuted: #http://msdn.microsoft.com/en-us/library/ee201536(v=exchg.80).aspx
    Unknown =       0
    ReplyToSender = 1
    ReplyToAll =    2
    Forward =       3

class email_Recurrence(object):                                       #http://msdn.microsoft.com/en-us/library/ee160268(v=exchg.80).aspx
    def __init__(self):
        self.email_Type = email_Type.Daily                                  #Required. Byte. See "MSASEMAIL.Type" for enum.
        self.email_Interval = 1                                       #Required. Integer. An Interval element value of 1 indicates that the meeting occurs every week, month, or year, depending upon the value of "self".Type. An Interval value of 2 indicates that the meeting occurs every other week, month, or year.
        self.email_Until = None                                       #Optional. dateTime. End of recurrence.
        self.email_Occurances = None                                  #Optional. Integer. Number of occurrences before the series of recurring meetings ends.
        self.email_WeekOfMonth = None                                 #Optional. Integer. The week of the month in which the meeting recurs. Required when the Type is set to a value of 6.
        self.email_DayOfMonth = None                                  #Optional. Integer. The day of the month on which the meeting recurs. Required when the Type is set to a value of 2 or 5.
        self.email_DayOfWeek = None                                   #Optional. Integer. See "MSASEMAIL.DayOfWeek" emun for values. The day of the week on which this meeting recurs. Can be anded together for multiple days of week. Required when the Type is set to a value of 1 or 6
        self.email_MonthOfYear = None                                 #Optional. Integer. The month of the year in which the meeting recurs. Required when the Type is set to a value of 6.
        self.email2_CalendarType = email2_CalendarType.Default  #Required. Byte. See "MSASEMAIL.email2_CalendarType" for enum.
        self.email2_IsLeapMonth = 0                             #Optional. Byte. Does the recurrence takes place in the leap month of the given year?
        self.email2_FirstDayOfWeek = email2_FirstDayOfWeek.Sunday #Optional. Byte. See "MSASEMAIL.email2_FirstDayOfWeek" for enum. What is considered the first day  of the week for this recurrence?

class email_MeetingRequest(object):                   #http://msdn.microsoft.com/en-us/library/ee157541(v=exchg.80).aspx
    def __init__(self):
        self.email_AllDayEvent = False                #Optional. Byte. Is meeting all day? 0 or 1.
        self.email_StartTime = None                   #Optional. dateTime.
        self.email_DtStamp = None                     #Required. dateTime. Time that the MeetingRequest item was created.
        self.email_EndTime = None                     #Optional. dateTime.
        self.email_InstanceType = email_InstanceType.Single #Optional. Byte. See "MSASEMAIL.InstanceTypes" enum.
        self.email_Location = ""                      #Optional. String. Location of meeting.
        self.email_Organizer = ""                     #Optional. Email address as String. Email address of  meeting organizer.
        self.email_RecurrenceId = None                #Optional. dateTime of specific instance of recurring meeting.
        self.email_Reminder = 0                       #Optional. Interger?. Time in seconds before meeting that reminder will be triggered.
        self.email_ResponseRequested = 1              #Optional. Byte. Has the organizer requested a response of this MeetingRequest? 0 or 1.
        self.email_Recurrences = []                   #Optional. List of "MSASEMAIL.Recurrence". If specified, at least one recurrence in list is required.
        self.email_Sensitivity = email_Sensitivity.Normal   #Optional. Integer. See "MSASEMAIL.Sensitivity" for enum. How sensitive is the meeting? Default is Normal.
        self.email_BusyStatus = email_BusyStatus.Tentative  #Optional. Integer. See "MSASEMAIL.BusyStatus" for enum. Default is Tentantive.
        self.email_TimeZone = ""                      #Required. String formated as per http://msdn.microsoft.com/en-us/library/ee204550(v=exchg.80).aspx.
        self.email_GlobalObjId = self.set_GlobalObjId()                   #Required. Generated by self.generate_GlobalObjId()
        self.email_DisallowNewTimeProposal = 0                            #Optional. Byte. 0 = new time proposals allowed, >0 = new time proposals not allowed. Default is 0.
        self.email_MeetingMessageType = email2_MeetingMessageType.Silent  #Optional. Byte. See "MSASEMAIL.email2_MeetingMessageType" for enum. Default is Silent.
    def set_GlobalObjId(self):
        #TODO
        return
    def set_TimeZone(self, intimezone=None):
        from MSASDTYPE import datatype_TimeZone
        if intimezone:
            self.TimeZone = datatype_TimeZone.get_timezone_bytes(intimezone)
        else:
            self.TimeZone = datatype_TimeZone.get_local_timezone_bytes()

class email_Flag(object):                   #http://msdn.microsoft.com/en-us/library/ee160518(v=exchg.80).aspx
    def __init__(self):
        self.tasks_Subject = ""             #Optional. String.
        self.email_flag_Status = email_Flag_status.Active
        self.email_FlagType = ""            #Optional. String. A string the 'explains' the flagging, such as "flag for follow up".
        self.tasks_DateCompleted = None     #Optional. dateTime. If set, email_CompleteTime is also required.
        self.email_CompleteTime = None      #Require if complete. dateTime.
        self.tasks_StartDate = None         #Optional. dateTime. If set, the other tasks_*Date elements must also be set.
        self.tasks_DueDate = None           #Optional. dateTime. If set, the other tasks_*Date elements must also be set.
        self.tasks_UtcStartDate = None      #Optional. dateTime. If set, the other tasks_*Date elements must also be set.
        self.tasks_UtcDueDate = None        #Optional. dateTime. If set, the other tasks_*Date elements must also be set.
        self.tasks_ReminderSet = 0          #Optional. Byte. Is reminder set? 0 or 1.
        self.tasks_ReminderTime = None      #Optional. dateTime
        self.tasks_OrdinalDate = None       #Optional. dateTime. Time at which flag was set.
        self.tasks_SubOrdinalDate = None    #Optional. String. Should be used for sorting.
    def parse(self, inwapxml_airsync_Flag):
        email_elements = inwapxml_airsync_Flag.get_children()
        for element in email_elements:
            if element.tag == "tasks:Subject":
                self.tasks_Subject = element.text
            elif element.tag == "email:Status":
                self.email_flag_Status = element.text
            elif element.tag == "email:FlagType":
                self.email_FlagType = element.text
            elif element.tag == "tasks:DateCompleted":
                self.tasks_DateCompleted = element.text
            elif element.tag == "email:CompleteTime":
                self.email_CompleteTime = element.text
            elif element.tag == "tasks:StartDate":
                self.tasks_StartDate = element.text
            elif element.tag == "tasks:DueDate":
                self.tasks_DueDate = element.text
            elif element.tag == "tasks:UtcStartDate":
                self.tasks_UtcStartDate = element.text
            elif element.tag == "tasks:UtcDueDate":
                self.tasks_UtcDueDate = element.text
            elif element.tag == "tasks:ReminderSet":
                self.tasks_ReminderSet = element.text
            elif element.tag == "tasks:ReminderTime":
                self.tasks_ReminderTime = element.text
            elif element.tag == "tasks:OrdinalDate":
                self.tasks_OrdinalDate = element.text
            elif element.tag == "tasks:SubOrdinalDate":
                self.tasks_SubOrdinalDate = element.text
    def marshal(self):
        import base64
        return base64.b64encode("%s//%s//%s//%s//%s//%s//%s//%s//%s//%s//%s//%s//%s" % (self.tasks_Subject, str(self.email_flag_Status), self.email_FlagType, self.tasks_DateCompleted, self.email_CompleteTime, self.tasks_StartDate,
                                                                                        self.tasks_DueDate, self.tasks_UtcStartDate, self.tasks_UtcDueDate, self.tasks_ReminderSet, self.tasks_ReminderTime, self.tasks_OrdinalDate, self.tasks_SubOrdinalDate))
    def __repr__(self):
        return self.marshal()

#class email_Category(object):
#    def __init__(self, category):
#        self.name = category #Required. String. Name of category.

class Email(object):
    """Aggregation of email elements that can be included in an 'Email' item to or from an AS server."""
    def __init__(self):
        self.server_id = ""
        self.email_To = []                #String. List of string seperated by commas.
        self.email_Cc = []                #String. List of string seperated by commas.
        self.email_From = ""              #String
        self.email_Subject = ""           #String
        self.email_ReplyTo = ""           #String. Specifies the e-mail address to which replies will be addressed by default.
        self.email_DateReceived = None    #dataTime. 
        self.email_DisplayTo = []         #String. List of display names of recipient seperated by semi-colons.
        self.email_ThreadTopic = ""       #String
        self.email_Importance = 1         #Byte. See "MSASEMAIL.Importance"
        self.email_Read = 0               #Boolean. Whether or not email has been read.
        self.airsyncbase_Attachments = [] #"MSASAIRS.Attachments". List of "MSASAIRS.Attachment"s.
        self.airsyncbase_Body = None      #"MSASAIRS.Body". Email message body.
        self.email_MessageClass = email_MessageClass.IPM_Note #String. See "MSASEMAIL.MessageClass" enum.
        self.email_InternetCPID = ""      #Required. String. Original MIME language code page ID.
        self.email_Flag = None            #Optional. email_Flag object.
        self.airsyncbase_NativeBodyType = airsyncbase_NativeBodyType.HTML #Optional. Byte enum. BodyType stored on server before any modification during transport. 
        self.email_ContentClass = ""            #Optional. String. The content class of the data.
        self.email2_UmCalledId = ""             #Optional. Server to client. See http://msdn.microsoft.com/en-us/library/ee200631(v=exchg.80).aspx for when required.
        self.email2_UmUserNotes = ""            #Optional. Server to client. See http://msdn.microsoft.com/en-us/library/ee158056(v=exchg.80).aspx for when required.
        self.email2_ConversationId = ""         #Required. Byte array transfered as wbxml opaque data.
        self.email2_ConversationIndex = ""      #Required. Byte array transfered as wbxml opaque data. Contains a set of timestamps used by clients to generate a conversation tree view. The first timestamp identifies the date and time when the message was originally sent by the server. Additional timestamps are added when the message is forwarded or replied to.
        self.email2_LastVerbExecuted = ""       #Optional. Integer. Contains the most recent email action. Can be used to choose email message icon.
        self.email2_LastVerbExecutedTime = ""   #Optional. dateTime. Contains the time of the email2_LastVerbExecuted.
        self.email2_ReceivedAsBcc = "0"         #Optional. Boolean. Was email received as BCC.
        self.email2_Sender = ""                 #Optional. String. If email was from delegate, the delegate's name appears here.
        self.email_Categories = []              #Optional. List of "email_Category"s that apply to this message. Max 300. http://msdn.microsoft.com/en-us/library/ee625079(v=exchg.80).aspx
        self.airsyncbase_BodyPart = ""          #Optional. See "airsyncbase_BodyPart".
        self.email2_AccountId = ""              #Optional. Specific account email was sent to (i.e. if not to PrimarySmtpAddress).
        self.rm_RightsManagementLicense = []    #Optional. Contains rights management information.
    def __repr__(self):
        return "\r\n%s\r\n------Start Email------\r\nFrom: %s\r\nTo: %s\r\nCc: %s\r\nSubject: %s\r\nDateReceived: %s\r\nMessageClass: %s\r\nContentClass: %s\r\n\r\n%s\r\n-------End Email-------\r\n" % (super(Email, self).__repr__(), self.email_From, self.email_To, self.email_Cc, self.email_Subject, self.email_DateReceived, self.email_MessageClass,self.email_ContentClass,self.airsyncbase_Body.airsyncbase_Data)
    def parse(self, inwapxml_airsync_command):
        email_base = inwapxml_airsync_command.get_children()
        self.server_id = email_base[0].text
        email_elements = email_base[1].get_children()
        for element in email_elements:
            if element.tag == "email:To":
                self.email_To = element.text
            elif element.tag == "email:Cc":
                self.email_Cc = element.text
            elif element.tag == "email:From":
                self.email_From = element.text
            elif element.tag == "email:Subject":
                self.email_Subject = element.text
            elif element.tag == "email:ReplyTo":
                self.email_ReplyTo = element.text
            elif element.tag == "email:DateReceived":
                self.email_DateReceived = element.text
            elif element.tag == "email:DisplayTo":
                self.email_DisplayTo = element.text
            elif element.tag == "email:ThreadTopic":
                self.email_TreadTopic = element.text
            elif element.tag == "email:Importance":
                self.email_Importance = element.text
            elif element.tag == "email:Read":
                self.email_Read = element.text
            elif element.tag == "airsyncbase:Attachments":
                self.airsyncbase_Attachments = airsyncbase_Attachments.parse(element)
            elif element.tag == "airsyncbase:Body":
                body = airsyncbase_Body()
                body.parse(element)
                self.airsyncbase_Body = body
            elif element.tag == "email:MessageClass":
                self.email_MessageClass = element.text
            elif element.tag == "email:InternetCPID":
                self.email_InternetCPID = element.text
            elif element.tag == "email:Flag":
                flag = email_Flag()
                flag.parse(element)
                self.email_Flag = flag
            elif element.tag == "airsyncbase:NativeBodyType":
                self.airsyncbase_NativeBodyType = element.text
            elif element.tag == "email:ContentClass":
                self.email_ContentClass = element.text
            elif element.tag == "email2:UmCallerId":
                self.email2_UmCalledId = element.text
            elif element.tag == "email2:UmUserNotes":
                self.email2_UmUserNotes = element.text
            elif element.tag == "email2:ConversationId":
                self.email2_ConversationId = element.text
            elif element.tag == "email2:ConversationIndex":
                self.email2_ConversationIndex = element.text
            elif element.tag == "email2:LastVerbExecuted":
                self.email2_LastVerbExecuted = element.text
            elif element.tag == "email2:LastVerbExecutedTime":
                self.email2_LastVerbExecutedTime = element.text
            elif element.tag == "email2:ReceivedAsBcc":
                self.email2_ReceivedAsBcc = element.text
            elif element.tag == "email2:Sender":
                self.email2_Sender = element.text
            elif element.tag == "email:Categories":
                categories_elements = element.get_children()
                for category in categories_elements:
                    self.email_Categories.append(category.text)
            elif element.tag == "airsyncbase:BodyPart":
                self.airsyncbase_Body = airsyncbase_BodyPart.parse(element)
            elif element.tag == "email2:AccountId":
                self.email2_AccountId = element.text
            elif element.tag == "rm:RightsManagementLicense":
                continue
      
def parse_email(data, type=1):
    email_dict = {}
    if type == 1:
        email_base = data.get_children()
        email_dict.update({"server_id" : email_base[0].text})
        email_elements = email_base[1].get_children()
        for element in email_elements:
            if element.tag == "email:To":
                    email_dict.update({ "email_To" : element.text })
            elif element.tag == "email:Cc":
                    email_dict.update({ "email_Cc" : element.text })
            elif element.tag == "email:From":
                    email_dict.update({ "email_From" : element.text })
            elif element.tag == "email:Subject":
                    email_dict.update({ "email_Subject" : element.text })
            elif element.tag == "email:ReplyTo":
                    email_dict.update({ "email_ReplyTo" : element.text })
            elif element.tag == "email:DateReceived":
                    email_dict.update({ "email_DateReceived" : element.text })
            elif element.tag == "email:DisplayTo":
                    email_dict.update({ "email_DisplayTo" : element.text })
            elif element.tag == "email:ThreadTopic":
                    email_dict.update({ "email_ThreadTopic" : element.text })
            elif element.tag == "email:Importance":
                    email_dict.update({ "email_Importance" : element.text })
            elif element.tag == "email:Read":
                    email_dict.update({ "email_Read" : element.text })
            elif element.tag == "airsyncbase:Attachments":
                    email_dict.update({ "airsyncbase_Attachments" : airsyncbase_Attachments.parse(element)})
            elif element.tag == "airsyncbase:Body":
                body = airsyncbase_Body()
                body.parse(element)
                email_dict.update({ "airsyncbase_Body" : body })
            elif element.tag == "email:MessageClass":
                    email_dict.update({ "email_MessageClass" : element.text })
            elif element.tag == "email:InternetCPID":
                    email_dict.update({ "email_InternetCPID" : element.text })
            elif element.tag == "email:Flag":
                    flag = email_Flag()
                    flag.parse(element)
                    email_dict.update({ "email_Flag" : flag})
            elif element.tag == "airsyncbase:NativeBodyType":
                    email_dict.update({ "airsyncbase_NativeBodyType" : element.text })
            elif element.tag == "email:ContentClass":
                    email_dict.update({ "email_ContentClass" : element.text })
            elif element.tag == "email2:UmCallerId":
                    email_dict.update({ "email2_UmCalledId" : element.text })
            elif element.tag == "email2:UmUserNotes":
                    email_dict.update({ "email2_UmUserNotes" : element.text })
            elif element.tag == "email2:ConversationId":
                    email_dict.update({ "email2_ConversationId" : element.text })
            elif element.tag == "email2:ConversationIndex":
                    email_dict.update({ "email2_ConversationIndex" : element.text })
            elif element.tag == "email2:LastVerbExecuted":
                    email_dict.update({ "email2_LastVerbExecuted" : element.text })
            elif element.tag == "email2:LastVerbExecutedTime":
                    email_dict.update({ "email2_LastVerbExecutedTime" : element.text })
            elif element.tag == "email2:ReceivedAsBcc":
                    email_dict.update({ "email2_ReceivedAsBcc" : element.text })
            elif element.tag == "email2:Sender":
                    email_dict.update({ "email2_Sender" : element.text })
            elif element.tag == "email:Categories":
                categories_list = []
                categories = element.get_children()
                for category_element in categories:
                    categories_list.append(category_element.text)
                email_dict.update({ "email_Categories" : categories_list })
            elif element.tag == "airsyncbase:BodyPart":
                    email_dict.update({ "airsyncbase_Body" : airsyncbase_BodyPart.parse(element)})
            elif element.tag == "email2:AccountId":
                    email_dict.update({ "email2_AccountId" : element.text })
            elif element.tag == "rm:RightsManagementLicense":
                continue
    return email_dict