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

"""[MS-ASCMD] Generic/various class namespace objects"""

class FolderHierarchy:
    Status = {
                "1": ( "Success.", "Server successfully completed command.", "None.", "Global" ),
                "6": ( "An error occurred on the server.", "Server misconfiguration, temporary system issue, or bad item. This is frequently a transient condition.", "Retry the FolderSync command. If continued attempts to synchronization fail, consider returning to synchronization key zero (0).", "Global" ),
                "9": ( "Synchronization key mismatch or invalid synchronization key.", "The client sent a malformed or mismatched synchronization key, or the synchronization state is corrupted on the server.", "Delete folders added since last synchronization and return to synchronization key to zero (0).", "Global" ),
                "10": ( "Malformed request.", "The client sent a command request that contains a semantic error, or the client attempted to create a default folder, such as the Inbox folder, Outbox folder, or Contacts folder.", "Double-check the request for accuracy.", "Global" ),
                "11": ( "An unknown error occurred.", "Unknown.", "None.", "Global" ),
                "12": ( "Code unknown.", "Unusual back-end issue.", "None.", "Global" )
                }
    class DefaultFoldersIds:
        Calendar =      1
        Contacts =      2
        DeletedItems =  3
        Drafts =        4
        Inbox =         5
        Journal =       6
        JunkEmail =     7
        Notes =         8
        Outbox =        9
        SentItems =     10
        Tasks =         11
        RecipientInfo = "RI"
    class Type:
        Generic =       1
        Inbox =         2
        Drafts =        3
        DeletedItems =  4
        SentItems =     5
        Outbox =        6
        Tasks =         7
        Calendar =      8
        Contacts =      9
        Notes =         10
        Journal =       11
        JunkEmail =     12
        MailG =         12
        CalendarG =     13
        ContactsG =     14
        TasksG =        15
        JournalG =      16
        NotesG =        17
        RecipientInfo = 19
    FolderTypeToClass = {
                            "1" : "Email",
                            "2" : "Email",
                            "3" : "Email",
                            "4" : "Email",
                            "5" : "Email",
                            "6" : "Email",
                            "7" : "Tasks",
                            "8" : "Calendar",
                            "9" : "Contacts",
                            "10" : "Notes",
                            "11" : "Email",
                            "12" : "Email",
                            "13" : "Calendar",
                            "14" : "Contacts",
                            "15" : "Tasks",
                            "16" : "Email",
                            "17" : "Notes",
                            "19" : "Contacts" #?
                        }

    class FolderCreate:
        Status = {
              "2": ( "A folder that has this name already exists.", "The parent folder already contains a folder that has this name.", "Prompt user to supply a unique name.", "Item" ),
              "3": ( "The specified parent folder is a special system folder.", "The specified parent folder is the Recipient information folder.", "Create the folder under a different parent.", "Item" ),
              "5": ( "The specified parent folder was not found.", "The parent folder does not exist on the server, possibly because it has been deleted or renamed.", "Issue a FolderSync command for the new hierarchy and prompt the user for a new parent folder.", "Item" )
              }

        class Type:
            Generic =   1
            Mail =      12
            Calendar =  13
            Contacts =  14
            Tasks =     15
            Journal =   16
            Notes =     17

    class FolderDelete:
        Status = {
                  "3": ( "The specified folder is a special system folder, such as the Inbox folder, Outbox folder, Contacts folder, Recipient information, or Drafts folder, and cannot be deleted by the client.", "The client specified a special folder in a FolderDelete command request. special folders cannot be deleted.", "None.", "Item" ),
                  "4": ( "The specified folder does not exist.", "The client specified a nonexistent folder in a FolderDelete command request.", "Issue a FolderSync command for the new hierarchy.", "Item" )
                  }
    class FolderUpdate:
        Status = {
                  "2": ( "A folder with that name already exists or the specified folder is a special folder.", "A folder with that name already exists or the specified folder is a special folder, such as the Inbox, Outbox, Contacts, or Drafts folders. Special folders cannot be updated.", "None.", "Item" ),
                  "3": ( "The specified folder is the Recipient information folder, which cannot be updated by the client.", "The client specified the Recipient information folder, which is a special folder. Special folders cannot be updated.", "None.", "Item" ),
                  "4": ( "The specified folder does not exist.", "Client specified a nonexistent folder in a FolderUpdate command request.", "Issue a FolderSync command for the new hierarchy.", "Item" ),
                  "5": ( "The specified parent folder was not found.", "Client specified a nonexistent folder in a FolderUpdate command request.", "Issue a FolderSync command for the new hierarchy.", "Item" ),
                  }
    class FolderSync:
        Status = {}

    class Folder:
        def __init__(self, ParentId=None, DisplayName=None, Type=None, ServerId=None):
            self.ServerId = ServerId
            self.ParentId = ParentId
            self.DisplayName = DisplayName
            self.Type = Type

class ResolveRecipients:
    class ResolveRecipients:
        Status = {
                  "1": "Success.",
                  "5": "Protocol error. Either an invalid parameter was specified or the range exceeded limits.",
                  "6": "An error occurred on the server. The client SHOULD retry the request.",
                  }
    class Response:
        Status = {
                  "1": "The recipient was resolved successfully.",
                  "2": "The recipient was found to be ambiguous. The returned list of recipients are suggestions. No certificate nodes were returned. Prompt the user to select the intended recipient from the list returned.",
                  "3": "The recipient was found to be ambiguous. The returned list is a partial list of suggestions. The total count of recipients can be obtained from the RecipientCount element. No certificate nodes were returned. Prompt the user to select the intended recipient from the list returned or to get more recipients.",
                  "4": "The recipient did not resolve to any contact or GAL entry. No certificates were returned. Inform the user of the error and direct the user to check the spelling.",
                  }
    class Availability:
        Status = {
                  "1": "Free/busy data was successfully retrieved for a given recipient. This value does not indicate that the response is complete.",
                  "160": "There were more than 100 recipients identified by the To elements in the ResolveRecipient request.",
                  "161": "The distribution group identified by the To element of the ResolveRecipient request included more than 20 recipients.",
                  "162": "The free/busy data could not be retrieved by the server due to a temporary failure. The client SHOULD reissue the request. This error is caused by a timeout value being reached while requesting free/busy data for some users, but not others.",
                  "163": "Free/busy data could not be retrieved from the server for a given recipient. Clients SHOULD NOT reissue the request as it is caused by a lack of permission to retrieve the data.",
                  }
    class Certificates:
        Status = {
                  "1": "One or more certificates were successfully returned.",
                  "7": "The recipient does not have a valid S/MIME certificate. No certificates were returned.",
                  "8": "The global certificate limit was reached and the recipient's certificate could not be returned. The count certificates not returned can be obtained from the CertificateCount element. Retry with fewer recipients if possible, otherwise prompt the user.",
                  }
    class Picture:
        Status = {
                  "1": "The contact photo was retrieved successfully.",
                  "173": "The user does not have a contact photo.",
                  "174": "The contact photo exceeded the size limit set by the MaxSize element.",
                  "175": "The number of contact photos returned exceeded the size limit set by the MaxPictures element.",
                  }

    class CertificateRetrieval:
        DoNotRetrieve = 0
        RetrieveFull =  1
        RetrieveMini =  2
    class Type:
        Contacts =  1
        GAL =       2

class Provision:
    Status = {
              "1": ( "Success.", "Server successfully completed command.", "None.", "Global" ),
              "2": ("Protocol error.", "Syntax error in the Provision command request.", "Fix syntax in the request and resubmit."),
              "3": ("An error occurred on the server.", "Server misconfiguration, temporary system issue, or bad item. This is frequently a transient condition.", "Retry."),
              }
    class Policy:
        Status = {
                  "1": ("Success.", "The requested policy data is included in the response.", "Apply the policy."),
                  "2": ("Policy not defined.", "No policy of the requested type is defined on the server.", "Stop sending policy information. No policy is implemented."),
                  "3": ("The policy type is unknown.", "The client sent a policy that the server does not recognize.", "Issue a request with a value of \"MS-EAS-Provisioning-WBXML\" in the PolicyType element."),
                  "4": ("Policy data is corrupt.", "The policy data on the server is corrupt.", "Server administrator intervention is required."),
                  "5": ("Policy key mismatch.", "The client is trying to acknowledge an out-of-date or invalid policy.", "Issue a new Provision request to obtain a valid policy key."),
                }

class Ping:
    Status = {
                "1": ( "The heartbeat interval expired before any changes occurred in the folders being monitored. ", "", "Reissue the Ping command request.", "Global" ),
                "2": ( "Changes occurred in at least one of the monitored folders. The response specifies the changed folders.", "", "Issue a Sync command request for each folder that was specified in the Ping command response to retrieve the server changes. Reissue the Ping command when the Sync command completes to stay up to date.", "Global" ),
                "3": ( "The Ping command request omitted required parameters.", "The Ping command request did not specify all the necessary parameters. The client MUST issue a Ping request that includes both the heartbeat interval and the folder list at least once. The server saves the heartbeat interval value, so only the folder list is required on subsequent requests.", "Reissue the Ping command request with the entire XML body.", "Global" ),
                "4": ( "Syntax error in Ping command request.", "Frequently caused by poorly formatted WBXML.", "Double-check the request for accuracy.", "Global" ),
                "5": ( "The specified heartbeat interval is outside the allowed range. For intervals that were too short, the response contains the shortest allowed interval. For intervals that were too long, the response contains the longest allowed interval.", "The client sent a Ping command request with a heartbeat interval that was either too long or too short.", "Reissue the Ping command by using a heartbeat interval inside the allowed range. Setting the interval to the value returned in the Ping response will most closely accommodate the original value specified.", "Global" ),
                "6": ( "The Ping command request specified more than the allowed number of folders to monitor. The response indicates the allowed number in the MaxFolders element.", "The client sent a Ping command request that specified more folders than the server is configured to monitor.", "Direct the user to select fewer folders to monitor. Resend the Ping command request with the new, shorter list.", "Global" ),
                "7": ( "Direct the user to select fewer folders to monitor. Resend the Ping command request with the new, shorter list.", "The folder hierarchy is out of date; a folder hierarchy sync is required.", "Issue a FolderSync command to get the new hierarchy and prompt the user, if it is necessary, for new folders to monitor. Reissue the Ping command.", "Global" ),
                "8": ( "An error occurred on the server.", "Server misconfiguration, temporary system issue, or bad item. This is frequently a transient condition.", "Retry the Ping command.", "Global" ),
                }
    class Class:
        Email = "Email"
        Calendar = "Calendar"
        Contacts = "Contacts"
        Tasks = "Tasks"
        Notes = "Notes"

class GetItemEstimate:
    Status = {
                "1": ( "Success.", "Server successfully completed command.", "None.", "Global" ),
                "2": ( "A collection was invalid or one of the specified collection IDs was invalid. ", "One or more of the specified folders does not exist or an incorrect folder was requested.", "Issue a FolderSync command to get the new hierarchy. Then retry with a valid collection or collection ID.", "Item" ),
                "3": ( "The synchronization state has not been primed.", "The client has issued a GetItemEstimate command without first issuing a Sync command request with an SyncKey element value of zero (0).", "Issue a Sync command with synchronization key of zero (0) before issuing the GetItemEstimate command again.", "Item" ),
                "4": ( "The specified synchronization key was invalid.", "Malformed or mismatched synchronization key, or the synchronization state is corrupted on the server.", "Issue a successful Sync command prior to issuing the GetItemEstimate command again. If the error is repeated, issue a Sync command with an SyncKey element value of zero (0).", "Global" )
                }

class ItemOperations:
    class StoreTypes:
        DocumentLibrary = "Document Library"
        Mailbox = "Mailbox"

class MeetingResponse:
    class UserResponse:
        Accepted =  1
        Tentitive = 2
        Declined =  3

class MoveItems:
    Status = {
                "1": ( "Invalid source collection ID or invalid source Item ID.", "The source folder collection ID (CollectionId element value) is not recognized by the server, possibly because the source folder has been deleted. Or, the item with the Item ID (SrcMsgId element) has been previously moved out of the folder with the Folder ID (SrcFldId element).", "Issue a FolderSync command to get the new hierarchy. Then, issue a Sync command for the SrcFldId and reissue the MoveItems command request if the items are still present in this source collection.", "Item" ),
                "2": ( "Invalid destination collection ID.", "The destination folder collection ID (CollectionId element value) is not recognized by the server, possibly because the source folder has been deleted.", "Issue a FolderSync command to get the new hierarchy. Then, use a valid collection ID.", "Item" ),
                "3": ( "Success.", "Server successfully completed command.", "None.", "Global" ),
                "4": ( "Source and destination collection IDs are the same.", "The client supplied a destination folder that is the same as the source.", "Send only requests where the CollectionId element values for the source and destination differ.", "Item" ),
                "5": ( "One of the following failures occurred: the item cannot be moved to more than one item at a time, or the source or destination item was locked.", "More than one DstFldId element was included in the request or an item with that name already exists.", "Retry the MoveItems command request with only one DstFldId element or move the item to another location.", "Global" ),
                "7": ( "Source or destination item was locked.", "Transient server condition.", "Retry the MoveItems command request.", "Item" ),
                }

class Search:
    class Name:
        Mailbox = "Mailbox"
        DocumentLibrary = "DocumentLibrary"
        GAL = "GAL"

class Sync:
    Status = {
                "1": ( "Success.", "Server successfully completed command.", "None.", "Global" ),
                "3": ( "Invalid synchronization key.", "Invalid or mismatched synchronization key, or the synchronization state corrupted on server.", "MUST return to SyncKey element value of 0 for the collection. The client SHOULD either delete any items that were added since the last successful Sync or the client MUST add those items back to the server after completing the full resynchronization. ", "Global" ),
                "4": ( "Protocol error.", "There was a semantic error in the synchronization request. The client is issuing a request that does not comply with the specification requirements.", "Double-check the request for accuracy and retry the Sync command.", "Global or Item" ),
                "5": ( "Server error.", "Server misconfiguration, temporary system issue, or bad item. This is frequently a transient condition.", "Retry the synchronization. If continued attempts to synchronization fail, consider returning to synchronization key 0.", "Global" ),
                "6": ( "Error in client/server conversion.", "The client has sent a malformed or invalid item.", "Stop sending the item. This is not a transient condition. ", "Item" ),
                "7": ( "Conflict matching the client and server object.", "The client has changed an item for which the conflict policy indicates that the server's changes take precedence.", "If it is necessary, inform the user that the change they made to the item has been overwritten by a server change.", "Item" ),
                "8": ( "Object not found.", "The client issued a fetch or change operation that has an ItemID value that is no longer valid on the server (for example, the item was deleted).", "Issue a synchronization request and prompt the user if necessary.", "Item" ),
                "9": ( "The Sync command cannot be completed.", "User account could be out of disk space.", "Free space in the user's mailbox and retry the Sync command.", "Item" ),
                "12": ( "The folder hierarchy has changed.", "Mailbox folders are not synchronized.", "Perform a FolderSync command and then retry the Sync command.", "Global" ),
                "13": ( "The Sync command request is not complete.", "An empty or partial Sync command request is received and the cached set of notify-able collections is missing.", "Resend a full Sync command request.", "Item" ),
                "14": ( "Invalid Wait or HeartbeatInterval value.", "The Sync request was processed successfully but the wait interval (Wait element value) or heartbeat interval (HeartbeatInterval element value) that is specified by the client is outside the range set by the server administrator.\r\n\r\nIf the HeartbeatInterval element value or Wait element value included in the Sync request is larger than the maximum allowable value, the response contains a Limit element that specifies the maximum allowed value.\r\n\r\nIf the HeartbeatInterval element value or Wait value included in the Sync request is smaller than the minimum allowable value, the response contains a Limit element that specifies the minimum allowed value.", "Update the Wait element value according to the Limit element and then resend the Sync command request.", "Item" ),
                "15": ( "Invalid Sync command request.", "Too many collections are included in the Sync request.", "Notify the user and synchronize fewer folders within one request.", "Item" ),
                "16": ( "Retry", "Something on the server caused a retriable error.", "Resend the request.", "Global" ),
                }

CommonStatuses = {
                    "101": ("InvalidContent", "The body of the HTTP request sent by the client is invalid.Ensure the HTTP request is using the specified Content-Type and length, and that the request is not missing.Examples:Ping command with a text/plain body, or SendMail command with version 12.1 and a WBXML body. "),
                    "102": ("InvalidWBXML", "The request contains WBXML but it could not be decoded into XML."),
                    "103": ("InvalidXML", "The XML provided in the request does not follow the protocol requirements."),
                    "104": ("InvalidDateTime", "The request contains a timestamp that could not be parsed into a valid date and time."),
                    "105": ("InvalidCombinationOfIDs", "The request contains a combination of parameters that is invalid."),
                    "106": ("InvalidIDs", "The request contains one or more IDs that could not be parsed into valid values.That is different from specifying an ID in the proper format that does not resolve to an existing item."),
                    "107": ("InvalidMIME", "The request contains MIME that could not be parsed."),
                    "108": ("DeviceIdMissingOrInvalid", "The device ID is either missing or has an invalid format."),
                    "109": ("DeviceTypeMissingOrInvalid", "The device type is either missing or has an invalid format."),
                    "110": ("ServerError", "The server encountered an unknown error, the device SHOULD NOT retry later."),
                    "111": ("ServerErrorRetryLater", "The server encountered an unknown error, the device SHOULD retry later."),
                    "112": ("ActiveDirectoryAccessDenied", "The server does not have access to read/write to an object in the directory service."),
                    "113": ("MailboxQuotaExceeded", "The mailbox has reached its size quota."),
                    "114": ("MailboxServerOffline", "The mailbox server is offline."),
                    "115": ("SendQuotaExceeded", "The request would exceed the send quota."),
                    "116": ("MessageRecipientUnresolved", "One of the recipients could not be resolved to an email address."),
                    "117": ("MessageReplyNotAllowed", "The mailbox server will not allow a reply of this message."),
                    "118": ("Message PreviouslySent", "The message was already sent in a previous request. The server determined this by remembering the ClientId values of the last few sent messages. This request contains a ClientId that was already used in a recent message."),
                    "119": ("MessageHasNoRecipient", "The message being sent contains no recipient."),
                    "120": ("MailSubmissionFailed", "The server failed to submit the message for delivery."),
                    "121": ("MessageReplyFailed", "The server failed to create a reply message."),
                    "122": ("AttachmentIsTooLarge", "The attachment is too large to be processed by this request."),
                    "123": ("UserHasNoMailbox", "A mailbox could not be found for the user."),
                    "124": ("UserCannotBeAnonymous", "The request was sent without credentials. Anonymous requests are not allowed."),
                    "125": ("UserPrincipalCouldNotBeFound", "The user was not found in the directory service."),
                    "126": ("UserDisabledForSync", "The user object in the directory service indicates that this user is not allowed to use ActiveSync."),
                    "127": ("UserOnNewMailboxCannotSync", "The server is configured to prevent users from syncing."),
                    "128": ("UserOnLegacyMailboxCannotSync", "The server is configured to prevent users on legacy servers from syncing."),
                    "129": ("DeviceIsBlockedForThisUser", "The user is configured to allow only some devices to sync. This device is not the allowed device."),
                    "130": ("AccessDenied", "The user is not allowed to perform that request."),
                    "131": ("AccountDisabled", "The user's account is disabled."),
                    "132": ("SyncStateNotFound", "The server's data file that contains the state of the client was unexpectedly missing. It might have disappeared while the request was in progress. The next request will likely answer a sync key error and the device will be forced to do full sync."),
                    "133": ("SyncStateLocked", "The server's data file that contains the state of the client is locked, possibly because the mailbox is being moved or was recently moved."),
                    "134": ("SyncStateCorrupt", "The server's data file that contains the state of the client appears to be corrupt."),
                    "135": ("SyncStateAlreadyExists", "The server's data file that contains the state of the client already exists. This can happen with two initial syncs are executed concurrently."),
                    "136": ("SyncStateVersionInvalid", "The version of the server's data file that contains the state of the client is invalid."),
                    "137": ("CommandNotSupported", "The command is not supported by this server."),
                    "138": ("VersionNotSupported", "The command is not supported in the protocol version specified."),
                    "139": ("DeviceNotFullyProvisionable", "The device uses a protocol version that cannot send all the policy settings the admin enabled."),
                    "140": ("RemoteWipeRequested", "A remote wipe was requested. The device SHOULD provision to get the request and then do another provision to acknowledge it."),
                    "141": ("LegacyDeviceOnStrictPolicy", "A policy is in place but the device is not provisionable."),
                    "142": ("DeviceNotProvisioned", "There is a policy in place; the device needs to provision."),
                    "143": ("PolicyRefresh", "The policy is configured to be refreshed every few hours. The device needs to re-provision."),
                    "144": ("InvalidPolicyKey", "The device's policy key is invalid. The policy has probably changed on the server. The device needs to re-provision."),
                    "145": ("ExternallyManagedDevicesNotAllowed", "The device claimed to be externally managed, but the server doesn't allow externally managed devices to sync."),
                    "146": ("NoRecurrenceInCalendar", "The request tried to forward an occurrence of a meeting that has no recurrence."),
                    "147": ("UnexpectedItemClass", "The request tried to operate on a type of items unknown to the server."),
                    "148": ("RemoteServerHasNoSSL", "The request needs to be proxied to another server but that server doesn't have Secure Sockets Layer enabled. This server is configured to only proxy requests to servers with SSL enabled."),
                    "149": ("InvalidStoredRequest", "The server had stored the previous request from that device. When the device sent an empty request, the server tried to re-execute that previous request but it was found to be impossible. The device needs to send the full request again."),
                    "150": ("ItemNotFound", "The ItemId value specified in the SmartReply command or SmartForward command request could not be found in the mailbox."),
                    "151": ("TooManyFolders", "The mailbox contains too many folders. By default, the mailbox cannot contain more than 1000 folders."),
                    "152": ("NoFoldersFound", "The mailbox contains no folders."),
                    "153": ("ItemsLostAfterMove", "After moving items to the destination folder, some of those items could not be found."),
                    "154": ("FailureInMoveOperation", "The mailbox server returned an unknown error while moving items."),
                    "155": ("MoveCommandDisallowedForNonPersistentMoveAction", "An ItemOperations command request to move a conversation is missing the MoveAlways element."),
                    "156": ("MoveCommandInvalidDestinationFolder", "The destination folder for the move is invalid."),
                    "160": ("AvailabilityTooManyRecipients", "The command has reached the maximum number of recipients that it can request availability for."),
                    "161": ("AvailabilityDLLimitReached", "The size of the distribution list is larger than the availability service is configured to process."),
                    "162": ("AvailabilityTransientFailure", "Availability service request failed with a transient error."),
                    "163": ("AvailabilityFailure", "Availability service request failed with an error."),
                    "164": ("BodyPartPreferenceTypeNotSupported", "The BodyPartPreference node has an unsupported Type element value."),
                    "165": ("DeviceInformationRequired", "The required DeviceInformation element is missing in the Provision request."),
                    "166": ("InvalidAccountId", "The AccountId value is not valid."),
                    "167": ("AccountSendDisabled", "The AccountId value specified in the request does not support sending email."),
                    "168": ("IRM_FeatureDisabled", "The Information Rights Management feature is disabled."),
                    "169": ("IRM_TransientError", "Information Rights Management encountered an error."),
                    "170": ("IRM_PermanentError", "Information Rights Management encountered an error."),
                    "171": ("IRM_InvalidTemplateID", "The Template ID value is not valid."),
                    "172": ("IRM_OperationNotPermitted", "Information Rights Management does not support the specified operation."),
                    "173": ("NoPicture", "The user does not have a contact photo."),
                    "174": ("PictureTooLarge", "The contact photo exceeds the size limit set by the MaxSize element."),
                    "175": ("PictureLimitReached", "The number of contact photos returned exceeds the size limit set by the MaxPictures element."),
                    "176": ("BodyPart_ConversationTooLarge", "The conversation is too large to compute the body parts. Try requesting the body of the item again, without body parts."),
                 }

def as_status(cmd, status):
    info= None
    if cmd == "Provision":
        try:
            info = Provision.Status[status]
        except KeyError:
            try:
                info = Provision.Policy.Status[status]
            except KeyError:
                try:
                    info = CommonStatuses[status]
                except KeyError:
                    info = "Status %s for command %s not found" % (cmd, status)
    elif cmd == "FolderSync":
        try:
            info = FolderHierarchy.Status[status]
        except KeyError:
            try:
                info = FolderHierarchy.FolderSync.Status[status]
            except KeyError:
                try:
                    info = CommonStatuses[status]
                except KeyError:
                    info = "Status %s for command %s not found" % (cmd, status)
    elif cmd == "FolderCreate":
        try:
            info = FolderHierarchy.Status[status]
        except KeyError:
            try:
                info = FolderHierarchy.FolderCreate.Status[status]
            except KeyError:
                try:
                    info = CommonStatuses[status]
                except KeyError:
                    info = "Status %s for command %s not found" % (cmd, status)
    elif cmd == "GetItemEstimate":
        try:
            info = GetItemEstimate.Status[status]
        except KeyError:
            try:
                info = CommonStatuses[status]
            except KeyError:
                info = "Status %s for command %s not found" % (cmd, status)
    if info:
        if isinstance(info, tuple):
            return_str = "\r\n%s status number: %s\r\n-----------------" % (cmd, status)
            for i in range(0,len(info)):
                if i == 0:
                    return_str += "\r\nStatus message: %s" % info[i]
                elif i == 1:
                    return_str += "\r\nStatus details: %s" % info[i]
                elif i == 2:
                    return_str += "\r\nStatus suggested resolution: %s" % info[i]
                elif i == 3:
                    return_str += "\r\nStatus scope: %s" % info[i]
            return return_str
        else:
            return info
