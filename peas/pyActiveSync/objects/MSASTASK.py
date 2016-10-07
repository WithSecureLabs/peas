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

"""[MS-ASTASK] Task objects"""

from MSASEMAIL import airsyncbase_Body

def parse_task(data):
    task_dict = {}
    task_base = data.get_children()
    task_dict.update({"server_id" : task_base[0].text})
    task_elements = task_base[1].get_children()
    for element in task_elements:
        if element.tag == "airsyncbase:Body":
            body = airsyncbase_Body()
            body.parse(element)
            task_dict.update({ "airsyncbase_Body" : body })
        elif element.tag == "tasks:CalendarType":
            task_dict.update({ "tasks_CalendarType" : element.text })
        elif element.tag == "tasks:Categories":
            categories_list = []
            categories = element.get_children()
            for category_element in categories:
                categories_list.append(category_element.text)
            task_dict.update({ "tasks_Categories" : categories_list })
        elif element.tag == "tasks:Complete":
            task_dict.update({ "tasks_Complete" : element.text })
        elif element.tag == "tasks:DateCompleted":
            task_dict.update({ "tasks_DateCompleted" : element.text })
        elif element.tag == "tasks:DueDate":
            task_dict.update({ "tasks_DueDate" : element.text })
        elif element.tag == "tasks:Importance":
            task_dict.update({ "tasks_Importance" : element.text })
        elif element.tag == "tasks:OrdinalDate":
            task_dict.update({ "tasks_OrdinalDate" : element.text })
        elif element.tag == "tasks:Recurrence":
            recurrence_dict = {}
            for recurrence_element in element.get_children():
                if recurrence_element.tag == "tasks:Type":
                    recurrence_dict.update({ "tasks_Type" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:Occurrences":
                    recurrence_dict.update({ "tasks_Occurrences" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:Regenerate":
                    recurrence_dict.update({ "tasks_Regenerate" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:DeadOccur":
                    recurrence_dict.update({ "tasks_DeadOccur" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:FirstDayOfWeek":
                    recurrence_dict.update({ "tasks_FirstDayOfWeek" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:Interval":
                    recurrence_dict.update({ "tasks_Interval" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:IsLeapMonth":
                    recurrence_dict.update({ "tasks_IsLeapMonth" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:WeekOfMonth":
                    recurrence_dict.update({ "tasks_WeekOfMonth" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:DayOfMonth":
                    recurrence_dict.update({ "tasks_DayOfMonth" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:DayOfWeek":
                    recurrence_dict.update({ "tasks_DayOfWeek" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:MonthOfYear":
                    recurrence_dict.update({ "tasks_MonthOfYear" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:Until":
                    recurrence_dict.update({ "tasks_Until" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:Start":
                    recurrence_dict.update({ "tasks_Start" : recurrence_element.text })
                elif recurrence_element.tag == "tasks:CalendarType":
                    recurrence_dict.update({ "tasks_CalendarType" : recurrence_element.text })
            task_dict.update({ "tasks_Recurrence" : recurrence_dict })
        elif element.tag == "tasks:ReminderSet":
            task_dict.update({ "tasks_ReminderSet" : element.text })
        elif element.tag == "tasks:ReminderTime":
            task_dict.update({ "tasks_ReminderTime" : element.text })
        elif element.tag == "tasks:Sensitivity":
            task_dict.update({ "tasks_Sensitivity" : element.text })
        elif element.tag == "tasks:StartDate":
            task_dict.update({ "tasks_StartDate" : element.text })
        elif element.tag == "tasks:Subject":
            task_dict.update({ "tasks_Subject" : element.text })
        elif element.tag == "tasks:SubOrdinalDate":
            task_dict.update({ "tasks_SubOrdinalDate" : element.text })
        elif element.tag == "tasks:UtcDueDate":
            task_dict.update({ "tasks_UtcDueDate" : element.text })
        elif element.tag == "tasks:UtcStartDate":
            task_dict.update({ "tasks_UtcStartDate" : element.text })
    return task_dict