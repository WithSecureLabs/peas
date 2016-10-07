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

"""[MS-ASCAL] Calendar objects"""

from MSASEMAIL import airsyncbase_Body

def parse_calendar(data):
    calendar_dict = {}
    calendar_base = data.get_children()
    calendar_dict.update({"server_id" : calendar_base[0].text})
    calendar_elements = calendar_base[1].get_children()
    for element in calendar_elements:
        if element.tag == "calendar:AllDayEvent":
            calendar_dict.update({ "calendar_AllDayEvent" : element.text })
        elif element.tag == "calendar:AppointmentReplyTime":
            calendar_dict.update({ "calendar_AppointmentReplyTime" : element.text })
        elif element.tag == "calendar:Attendees":
            attendees_list = []
            for attendee in element.get_children():
                attendee_dict = {}
                for attendee_element in attendee.get_children():
                    if attendee_element.tag == "calendar:AttendeeStatus":
                        attendee_dict.update({ "calendar_AttendeeStatus" : attendee_element.text })
                    elif attendee_element.tag == "calendar:AttendeeType":
                        attendee_dict.update({ "calendar_AttendeeType" : attendee_element.text })
                    elif attendee_element.tag == "calendar:Name":
                        attendee_dict.update({ "calendar_Name" : attendee_element.text })
                    elif attendee_element.tag == "calendar:Email":
                        attendee_dict.update({ "calendar_Email" : attendee_element.text })
                    attendees_list.append(attendee_dict)
            calendar_dict.update({ "calendar_Attendees" : attendees_list })
        elif element.tag == "airsyncbase:Body":
            body = airsyncbase_Body()
            body.parse(element)
            calendar_dict.update({ "airsyncbase_Body" : body })
        elif element.tag == "calendar:BusyStatus":
            calendar_dict.update({ "calendar_BusyStatus" : element.text })
        elif element.tag == "calendar:Categories":
            categories_list = []
            categories = element.get_children()
            for category_element in categories:
                categories_list.append(category_element.text)
            calendar_dict.update({ "calendar_Categories" : categories_list })
        elif element.tag == "calendar:DisallowNewTimeProposal":
            calendar_dict.update({ "calendar_DisallowNewTimeProposal" : element.text })
        elif element.tag == "calendar:DtStamp":
            calendar_dict.update({ "calendar_DtStamp" : element.text })
        elif element.tag == "calendar:EndTime":
            calendar_dict.update({ "calendar_EndTime" : element.text })
        elif element.tag == "calendar:Exceptions":
            exceptions_list = []
            for recurrence_exception in element.get_children():
                exception_dict = {}
                for exception_element in recurrence_exception.get_children():
                    if exception_element.tag == "calendar:Deleted":
                        exception_dict.update({ "calendar_Deleted" : exception_element.text })
                    elif exception_element.tag == "calendar:ExceptionStartTime":
                        exception_dict.update({ "calendar_ExceptionStartTime" : exception_element.text })
                    elif exception_element.tag == "calendar:AllDayEvent":
                        exception_dict.update({ "calendar_AllDayEvent" : exception_element.text })
                    elif exception_element.tag == "calendar:AppointmentReplyTime":
                        exception_dict.update({ "calendar_AppointmentReplyTime" : exception_element.text })
                    elif exception_element.tag == "calendar:Attendees":
                        attendees_list = []
                        for attendee in element.get_children():
                            attendee_dict = {}
                            for attendee_element in attendee.get_children():
                                if attendee_element.tag == "calendar:AttendeeStatus":
                                    attendee_dict.update({ "calendar_AttendeeStatus" : attendee_element.text })
                                elif attendee_element.tag == "calendar:AttendeeType":
                                    attendee_dict.update({ "calendar_AttendeeType" : attendee_element.text })
                                elif attendee_element.tag == "calendar:Name":
                                    attendee_dict.update({ "calendar_Name" : attendee_element.text })
                                elif attendee_element.tag == "calendar:Email":
                                    attendee_dict.update({ "calendar_Email" : attendee_element.text })
                                attendees_list.append(attendee_dict)
                        exception_dict.update({ "calendar_Attendees" : attendees_list })
                    elif exception_element.tag == "airsyncbase:Body":
                        body = airsyncbase_Body()
                        body.parse(element)
                        exception_dict.update({ "airsyncbase_Body" : body })
                    elif exception_element.tag == "calendar:BusyStatus":
                        exception_dict.update({ "calendar_BusyStatus" : exception_element.text })
                    elif exception_element.tag == "calendar:Categories":
                        categories_list = []
                        categories = element.get_children()
                        for category_element in categories:
                            categories_list.append(category_element.text)
                        exception_dict.update({ "calendar_Categories" : categories_list })
                    elif exception_element.tag == "calendar:StartTime":
                        exception_dict.update({ "calendar_StartTime" : exception_element.text })
                    elif exception_element.tag == "calendar:OnlineMeetingConfLink":
                        exception_dict.update({ "calendar_OnlineMeetingConfLink" : exception_element.text })
                    elif exception_element.tag == "calendar:OnlineMeetingExternalLink":
                        exception_dict.update({ "calendar_OnlineMeetingExternalLink" : exception_element.text })
                    elif exception_element.tag == "calendar:ResponseType":
                        exception_dict.update({ "calendar_ResponseType" : exception_element.text })
                    elif exception_element.tag == "calendar:Location":
                        exception_dict.update({ "calendar_Location" : exception_element.text })
                    elif exception_element.tag == "calendar:MeetingStatus":
                        exception_dict.update({ "calendar_MeetingStatus" : exception_element.text })
                    elif exception_element.tag == "calendar:EndTime":
                        exception_dict.update({ "calendar_EndTime" : exception_element.text })
                    elif exception_element.tag == "calendar:DtStamp":
                        exception_dict.update({ "calendar_DtStamp" : exception_element.text })
                    elif exception_element.tag == "calendar:Sensitivity":
                        exception_dict.update({ "calendar_Sensitivity" : exception_element.text })
                    elif exception_element.tag == "calendar:Reminder":
                        exception_dict.update({ "calendar_Reminder" : exception_element.text })
                    elif exception_element.tag == "calendar:Subject":
                        exception_dict.update({ "calendar_Subject" : exception_element.text })
                    exceptions_list.append(exception_dict)
            calendar_dict.update({ "calendar_Exceptions" : exceptions_list })
        elif element.tag == "calendar:Location":
            calendar_dict.update({ "calendar_Location" : element.text })
        elif element.tag == "calendar:MeetingStatus":
            calendar_dict.update({ "calendar_MeetingStatus" : element.text })
        elif element.tag == "airsyncbase:NativeBodyType":
            calendar_dict.update({ "airsyncbase_NativeBodyType" : element.text })
        elif element.tag == "calendar:OnlineMeetingConfLink":
            calendar_dict.update({ "calendar_OnlineMeetingConfLink" : element.text })
        elif element.tag == "calendar:OnlineMeetingExternalLink":
            calendar_dict.update({ "calendar_OnlineMeetingExternalLink" : element.text })
        elif element.tag == "calendar:OrganizerEmail":
            calendar_dict.update({ "calendar_OrganizerEmail" : element.text })
        elif element.tag == "calendar:OrganizerName":
            calendar_dict.update({ "calendar_OrganizerName" : element.text })
        elif element.tag == "calendar:Recurrence":
            recurrence_dict = {}
            for recurrence_element in element.get_children():
                if recurrence_element.tag == "calendar:Type":
                    recurrence_dict.update({ "calendar_Type" : recurrence_element.text })
                elif recurrence_element.tag == "calendar:Occurrences":
                    recurrence_dict.update({ "calendar_Occurrences" : recurrence_element.text })
                elif recurrence_element.tag == "calendar:FirstDayOfWeek":
                    recurrence_dict.update({ "calendar_FirstDayOfWeek" : recurrence_element.text })
                elif recurrence_element.tag == "calendar:Interval":
                    recurrence_dict.update({ "calendar_Interval" : recurrence_element.text })
                elif recurrence_element.tag == "calendar:IsLeapMonth":
                    recurrence_dict.update({ "calendar_IsLeapMonth" : recurrence_element.text })
                elif recurrence_element.tag == "calendar:WeekOfMonth":
                    recurrence_dict.update({ "calendar_WeekOfMonth" : recurrence_element.text })
                elif recurrence_element.tag == "calendar:DayOfMonth":
                    recurrence_dict.update({ "calendar_DayOfMonth" : recurrence_element.text })
                elif recurrence_element.tag == "calendar:DayOfWeek":
                    recurrence_dict.update({ "calendar_DayOfWeek" : recurrence_element.text })
                elif recurrence_element.tag == "calendar:MonthOfYear":
                    recurrence_dict.update({ "calendar_MonthOfYear" : recurrence_element.text })
                elif recurrence_element.tag == "calendar:Until":
                    recurrence_dict.update({ "calendar_Until" : recurrence_element.text })
                elif recurrence_element.tag == "calendar:CalendarType":
                    recurrence_dict.update({ "calendar_CalendarType" : recurrence_element.text })
            calendar_dict.update({ "calendar_Recurrence" : recurrence_dict })
        elif element.tag == "calendar:Reminder":
            calendar_dict.update({ "calendar_Reminder" : element.text })
        elif element.tag == "calendar:ResponseRequested":
            calendar_dict.update({ "calendar_ResponseRequested" : element.text })
        elif element.tag == "calendar:ResponseType":
            calendar_dict.update({ "calendar_ResponseType" : element.text })
        elif element.tag == "calendar:Sensitivity":
            calendar_dict.update({ "calendar_Sensitivity" : element.text })
        elif element.tag == "calendar:StartTime":
            calendar_dict.update({ "calendar_StartTime" : element.text })
        elif element.tag == "calendar:Subject":
            calendar_dict.update({ "calendar_Subject" : element.text })
        elif element.tag == "calendar:Timezone":
            calendar_dict.update({ "calendar_Timezone" : element.text })
        elif element.tag == "calendar:UID":
            calendar_dict.update({ "calendar_UID" : element.text })
    return calendar_dict

class calendar_Attendee(object):
    def __init__(self, email=None, name=None, attendee_status=None, attendee_type=None):
        self.email = email
        self.name = name
        self.attendee_status = attendee_status
        self.attendee_type = attendee_type
        self.delim = "/&*/"
    def init_from_storage(self, blob):
        import base64
        parts = base64.b64decode(blob).split(self.delim)
        self.email = parts[0]
        self.name = parts[1]
        self.attendee_status = parts[2]
        self.attendee_type = parts[3]
    def marshal_for_storage(self):
        import base64
        return base64.b64encode("%s%s%s%s%s%s%s%s" % (self.email, self.delim, self.name, self.delim, self.attendee_status, self.delim, self.attendee_type))

class calendar_Recurrence(object):
    def __init__(self):
        self.calendar_Type = calendar_Type.Daily                         # Required. Byte. See "MSASCAL.Type" for enum.
        self.calendar_Interval = 1                                       # Required. Integer. An Interval element value of 1 indicates that the meeting occurs every week, month, or year, depending upon the value of "self".Type. An Interval value of 2 indicates that the meeting occurs every other week, month, or year.
        self.calendar_Until = None                                       # Optional. dateTime. End of recurrence.
        self.calendar_Occurances = None                                  # Optional. Integer. Number of occurrences before the series of recurring meetings ends.
        self.calendar_WeekOfMonth = None                                 # Optional. Integer. The week of the month in which the meeting recurs. Required when the Type is set to a value of 6.
        self.calendar_DayOfMonth = None                                  # Optional. Integer. The day of the month on which the meeting recurs. Required when the Type is set to a value of 2 or 5.
        self.calendar_DayOfWeek = None                                   # Optional. Integer. See "MSASCAL.DayOfWeek" emun for values. The day of the week on which this meeting recurs. Can be anded together for multiple days of week. Required when the Type is set to a value of 1 or 6
        self.calendar_MonthOfYear = None                                 # Optional. Integer. The month of the year in which the meeting recurs. Required when the Type is set to a value of 6.
        self.calendar_CalendarType = calendar_CalendarType.Default       # Required. Byte. See "MSASCAL.calendar_CalendarType" for enum.
        self.calendar_IsLeapMonth = 0                                    # Optional. Byte. Does the recurrence takes place in the leap month of the given year?
        self.calendar_FirstDayOfWeek = calendar_FirstDayOfWeek.Sunday    # Optional. Byte. See "MSASCAL.calendar_FirstDayOfWeek" for enum. What is considered the first day  of the week for this recurrence?

class calendar_Exception(object):
    def __init__(self):
        self.calendar_Deleted = None 					  # This element is optional.
        self.calendar_ExceptionStartTime = None 		  # One instance of this element is required.
        self.calendar_Subject = None 					  # This element is optional.
        self.calendar_StartTime = None					  # This element is optional.
        self.calendar_EndTime = None 					  # This element is optional.
        self.airsyncbase_Body = None 					  # This element is optional.
        self.calendar_Location = None 					  # This element is optional.
        self.calendar_Categories = None 				  # This element is optional.
        self.calendar_Sensitivity = None 				  # This element is optional.
        self.calendar_BusyStatus = None 				  # This element is optional.
        self.calendar_AllDayEvent = None 				  # This element is optional.
        self.calendar_Reminder = None 					  # This element is optional.
        self.calendar_DtStamp = None 					  # This element is optional.
        self.calendar_MeetingStatus = None 				  # This element is optional.
        self.calendar_Attendees = None 					  # This element is optional.
        self.calendar_AppointmentReplyTime = None 		  # This element is optional in command responses. It is not included in command requests.
        self.calendar_ResponseType = None 				  # This element is optional in command responses. It is not included in command requests.
        self.calendar_OnlineMeetingConfLink = None 		  # This element is optional in command responses. It is not included in command requests.
        self.calendar_OnlineMeetingExternalLink = None	  # This element is optional in command responses. It is not included in command requests.