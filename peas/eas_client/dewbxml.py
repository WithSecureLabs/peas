#! /usr/bin/env python
#coding=utf-8

r'''Converter of Wireless Binary XML (WBXML) documents to plain-text XML.

    When invoked without arguments, DeWBXML opens one file dialog asking for an
    input WBXML file, and another for defining the path to the output plain-text
    XML file. Execution is terminated if any of those dialogs is canceled.

    Alternatively, the program can be invoked from command line with either two
    arguments (the input and output paths) or just one (in which case the output
    is written to standard output).
'''

__license__ = r'''
Copyright (c) 2010 Helio Perroni Filho <xperroni@gmail.com>

This file is part of DeWBXML.

DeWBXML is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DeWBXML is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DeWBXML. If not, see <http://www.gnu.org/licenses/>.
'''

__version__ = '2010-07-14r'

#import provisioning
#import rightsobjects
#import wml13

from base64    import b64encode
from sys       import stdout
from traceback import print_exc
from struct    import pack

# List of known charsets, indexed by their IANA numbers.
_charsets = {
      3: 'iso-ir-6',
      4: 'iso-ir-100',
      5: 'iso-ir-101',
      6: 'iso-ir-109',
      7: 'iso-ir-110',
      8: 'iso-ir-144',
      9: 'iso-ir-127',
     10: 'iso-ir-126',
    106: 'utf-8'
}

# List of known WBXML encondings for plain-text XML applications.
_applications = {
    0x01: {
            'dtd': r'activesync',
            'elements': [
                { # Page 0 - AirSync
                    "name":"AirSync",
                    0x05: ('Sync', None),
                    0x06: ('Responses', None),
                    0x07: ('Add', None),
                    0x08: ('Change', None),
                    0x09: ('Delete', None),
                    0x0a: ('Fetch', None),
                    0x0b: ('SyncKey', None),
                    0x0c: ('ClientId', None),
                    0x0d: ('ServerId', None),
                    0x0e: ('Status', None),
                    0x0f: ('Collection', None),
                    0x10: ('Class', None),
                    0x12: ('CollectionId', None),
                    0x13: ('GetChanges', None),
                    0x14: ('MoreAvailable', None),
                    0x15: ('WindowSize', None),
                    0x16: ('Commands', None),
                    0x17: ('Options', None),
                    0x18: ('FilterType', None),
                    0x1b: ('Conflict', None),
                    0x1c: ('Collections', None),
                    0x1d: ('ApplicationData', None),
                    0x1e: ('DeletesAsMoves', None),
                    0x20: ('Supported', None),
                    0x21: ('SoftDelete', None),
                    0x22: ('MIMESupport', None),
                    0x23: ('MIMETruncation', None),
                    0x24: ('Wait', None),
                    0x25: ('Limit', None),
                    0x26: ('Partial', None),
                    0x27: ('ConversationMode', None),
                    0x28: ('MaxItems', None),
                    0x29: ('HeartbeatInterval', None),
                },
                { # Page 1 - Contacts
                    "name":"Contacts",
                    0x05: ('Anniversary', None),
                    0x06: ('AssistantName', None),
                    0x07: ('AssistantPhoneNumber', None),
                    0x08: ('Birthday', None),
                    0x0c: ('Business2PhoneNumber', None),
                    0x0d: ('BusinessAddressCity', None),
                    0x0e: ('BusinessAddressCountry', None),
                    0x0f: ('BusinessAddressPostalCode', None),
                    0x10: ('BusinessAddressState', None),
                    0x11: ('BusinessAddressStreet', None),
                    0x12: ('BusinessFaxNumber', None),
                    0x13: ('BusinessPhoneNumber', None),
                    0x14: ('CarPhoneNumber', None),
                    0x15: ('Categories', None),
                    0x16: ('Category', None),
                    0x17: ('Children', None),
                    0x18: ('Child', None),
                    0x19: ('CompanyName', None),
                    0x1a: ('Department', None),
                    0x1b: ('Email1Address', None),
                    0x1c: ('Email2Address', None),
                    0x1d: ('Email3Address', None),
                    0x1e: ('FileAs', None),
                    0x1f: ('FirstName', None),
                    0x20: ('Home2PhoneNumber', None),
                    0x21: ('HomeAddressCity', None),
                    0x22: ('HomeAddressCountry', None),
                    0x23: ('HomeAddressPostalCode', None),
                    0x24: ('HomeAddressState', None),
                    0x25: ('HomeAddressStreet', None),
                    0x26: ('HomeFaxNumber', None),
                    0x27: ('HomePhoneNumber', None),
                    0x28: ('JobTitle', None),
                    0x29: ('LastName', None),
                    0x2a: ('MiddleName', None),
                    0x2b: ('MobilePhoneNumber', None),
                    0x2c: ('OfficeLocation', None),
                    0x2d: ('OtherAddressCity', None),
                    0x2e: ('OtherAddressCountry', None),
                    0x2f: ('OtherAddressPostalCode', None),
                    0x30: ('OtherAddressState', None),
                    0x31: ('OtherAddressStreet', None),
                    0x32: ('PagerNumber', None),
                    0x33: ('RadioPhoneNumber', None),
                    0x34: ('Spouse', None),
                    0x35: ('Suffix', None),
                    0x36: ('Title', None),
                    0x37: ('WebPage', None),
                    0x38: ('YomiCompanyName', None),
                    0x39: ('YomiFirstName', None),
                    0x3a: ('YomiLastName', None),
                    0x3c: ('Picture', None),
                    0x3d: ('Alias', None),
                    0x3e: ('WeightedRank', None),
                },
                { # Page 2 - Email
                    "name":"Email",
                    0x0f: ('DateReceived', None),
                    0x11: ('DisplayTo', None),
                    0x12: ('Importance', None),
                    0x13: ('MessageClass', None),
                    0x14: ('Subject', None),
                    0x15: ('Read', None),
                    0x16: ('To', None),
                    0x17: ('Cc', None),
                    0x18: ('From', None),
                    0x19: ('ReplyTo', None),
                    0x1a: ('AllDayEvent', None),
                    0x1b: ('Categories', None),
                    0x1c: ('Category', None),
                    0x1d: ('DtStamp', None),
                    0x1e: ('EndTime', None),
                    0x1f: ('InstanceType', None),
                    0x20: ('BusyStatus', None),
                    0x21: ('Location', None),
                    0x22: ('MeetingRequest', None),
                    0x23: ('Organizer', None),
                    0x24: ('RecurrenceId', None),
                    0x25: ('Reminder', None),
                    0x26: ('ResponseRequested', None),
                    0x27: ('Recurrences', None),
                    0x28: ('Recurrence', None),
                    0x29: ('Type', None),
                    0x2a: ('Until', None),
                    0x2b: ('Occurrences', None),
                    0x2c: ('Interval', None),
                    0x2d: ('DayOfWeek', None),
                    0x2e: ('DayOfMonth', None),
                    0x2f: ('WeekOfMonth', None),
                    0x30: ('MonthOfYear', None),
                    0x31: ('StartTime', None),
                    0x32: ('Sensitivity', None),
                    0x33: ('TimeZone', None),
                    0x34: ('GlobalObjId', None),
                    0x35: ('ThreadTopic', None),
                    0x39: ('InternetCPID', None),
                    0x3a: ('Flag', None),
                    0x3b: ('Status', None),
                    0x3c: ('ContentClass', None),
                    0x3d: ('FlagType', None),
                    0x3e: ('CompleteTime', None),
                    0x3f: ('DisallowNewTimeProposal', None),
                },
                { # Page 3 - AirNotify
                },
                { # Page 4 - Calendar
                },
                { # Page 5 - Move
                    "name":"Move",
                    0x05: ('MoveItems', None),
                    0x06: ('Move', None),
                    0x07: ('SrcMsgId', None),
                    0x08: ('SrcFldId', None),
                    0x09: ('DstFldId', None),
                    0x0a: ('Response', None),
                    0x0b: ('Status', None),
                    0x0c: ('DstMsgId', None),
                },
                { # Page 6 - GetItemEstimate
                },
                { # Page 7 - FolderHierarchy
                    "name":"FolderHierarchy",
                    0x07: ('DisplayName', None),
                    0x08: ('ServerId', None),
                    0x09: ('ParentId', None),
                    0x0a: ('Type', None),
                    0x0c: ('Status', None),
                    0x0e: ('Changes', None),
                    0x0f: ('Add', None),
                    0x10: ('Delete', None),
                    0x11: ('Update', None),
                    0x12: ('SyncKey', None),
                    0x13: ('FolderCreate', None),
                    0x14: ('FolderDelete', None),
                    0x15: ('FolderUpdate', None),
                    0x16: ('FolderSync', None),
                    0x17: ('Count', None),
                },
                { # Page 8 - MeetingResponse
                },
                { # Page 9 - Tasks
                    "name":"Tasks",
                    0x08: ('Categories', None),
                    0x09: ('Category', None),
                    0x0a: ('Complete', None),
                    0x0b: ('DateCompleted', None),
                    0x0c: ('DueDate', None),
                    0x0d: ('UtcDueDate', None),
                    0x0e: ('Importance', None),
                    0x0f: ('Recurrence', None),
                    0x10: ('Type', None),
                    0x11: ('Start', None),
                    0x12: ('Until', None),
                    0x13: ('Occurrences', None),
                    0x14: ('Interval', None),
                    0x15: ('DayOfMonth', None),
                    0x16: ('DayOfWeek', None),
                    0x17: ('WeekOfMonth', None),
                    0x18: ('MonthOfYear', None),
                    0x19: ('Regenerate', None),
                    0x1a: ('DeadOccur', None),
                    0x1b: ('ReminderSet', None),
                    0x1c: ('ReminderTime', None),
                    0x1d: ('Sensitivity', None),
                    0x1e: ('StartDate', None),
                    0x1f: ('UtcStartDate', None),
                    0x20: ('Subject', None),
                    0x22: ('OrdinalDate', None),
                    0x23: ('SubOrdinalDate', None),
                    0x24: ('CalendarType', None),
                    0x25: ('IsLeapMonth', None),
                    0x26: ('FirstDayOfWeek', None),
                },
                { # Page 10 - ResolveRecipients
                },
                { # Page 11 - ValidateCert
                },
                { # Page 12 - Contacts2
                },
                { # Page 13 - Ping
                },
                { # Page 14 - Provision
                    "name":"Provision",
                    0x05: ('Provision', None),
                    0x06: ('Policies', None),
                    0x07: ('Policy', None),
                    0x08: ('PolicyType', None),
                    0x09: ('PolicyKey', None),
                    0x0a: ('Data', None),
                    0x0b: ('Status', None),
                    0x0c: ('RemoteWipe', None),
                    0x0d: ('EASProvisionDoc', None),
                    0x0e: ('DevicePasswordEnabled', None),
                    0x0f: ('AlphanumericDevicePasswordRequired', None),
                    0x10: ('DeviceEncryptionEnabled', None),
                    0x11: ('PasswordRecoveryEnabled', None),
                    0x13: ('AttachmentsEnabled', None),
                    0x14: ('MinDevicePasswordLength', None),
                    0x15: ('MaxInactivityTimeDeviceLock', None),
                    0x16: ('MaxDevicePasswordFailedAttempts', None),
                    0x17: ('MaxAttachmentSize', None),
                    0x18: ('AllowSimpleDevicePassword', None),
                    0x19: ('DevicePasswordExpiration', None),
                    0x1a: ('DevicePasswordHistory', None),
                    0x1b: ('AllowStorageCard', None),
                    0x1c: ('AllowCamera', None),
                    0x1d: ('RequireDeviceEncryption', None),
                    0x1e: ('AllowUnsignedApplications', None),
                    0x1f: ('AllowUnsignedInstallationPackages', None),
                    0x20: ('MinDevicePasswordComplexCharacters', None),
                    0x21: ('AllowWiFi', None),
                    0x22: ('AllowTextMessaging', None),
                    0x23: ('AllowPOPIMAPEmail', None),
                    0x24: ('AllowBluetooth', None),
                    0x25: ('AllowIrDA', None),
                    0x26: ('RequireManualSyncWhenRoaming', None),
                    0x27: ('AllowDesktopSync', None),
                    0x28: ('MaxCalendarAgeFilter', None),
                    0x29: ('AllowHTMLEmail', None),
                    0x2a: ('MaxEmailAgeFilter', None),
                    0x2b: ('MaxEmailBodyTruncationSize', None),
                    0x2c: ('MaxEmailHTMLBodyTruncationSize', None),
                    0x2d: ('RequireSignedSMIMEMessages', None),
                    0x2e: ('RequireEncryptedSMIMEMessages', None),
                    0x2f: ('RequireSignedSMIMEAlgorithm', None),
                    0x30: ('RequireEncryptionSMIMEAlgorithm', None),
                    0x31: ('AllowSMIMEEncryptionAlgorithmNegotiation', None),
                    0x32: ('AllowSMIMESoftCerts', None),
                    0x33: ('AllowBrowser', None),
                    0x34: ('AllowConsumerEmail', None),
                    0x35: ('AllowRemoteDesktop', None),
                    0x36: ('AllowInternetSharing', None),
                    0x37: ('UnapprovedInROMApplicationList', None),
                    0x38: ('ApplicationName', None),
                    0x39: ('ApprovedApplicationList', None),
                    0x3a: ('Hash', None),
                },
                { # Page 15 - Search
                },
                { # Page 16 - GAL
                },
                { # Page 17 - AirSyncBase
                    "name":"AirSyncBase",
                    0x05: ('BodyPreference', None),
                    0x06: ('Type', None),
                    0x07: ('TruncationSize', None),
                    0x08: ('AllOrNone', None),
                    0x0a: ('Body', None),
                    0x0b: ('Data', None),
                    0x0c: ('EstimatedDataSize', None),
                    0x0d: ('Truncated', None),
                    0x0e: ('Attachments', None),
                    0x0f: ('Attachment', None),
                    0x10: ('DisplayName', None),
                    0x11: ('FileReference', None),
                    0x12: ('Method', None),
                    0x13: ('ContentId', None),
                    0x14: ('ContentLocation', None),
                    0x15: ('IsInline', None),
                    0x16: ('NativeBodyType', None),
                    0x17: ('ContentType', None),
                    0x18: ('Preview', None),
                    0x19: ('BodyPartReference', None),
                    0x1a: ('BodyPart', None),
                    0x1b: ('Status', None),
                },
                { # Page 18
                },
                { # Page 19
                    "name":"DocumentLibrary",
                    0x05: ('LinkId', None),
                    0x06: ('DisplayName', None),
                    0x07: ('IsFolder', None),
                    0x08: ('CreationDate', None),
                    0x09: ('LastModifiedDate', None),
                    0x0a: ('IsHidden', None),
                    0x0b: ('ContentLength', None),
                    0x0c: ('ContentType', None),
                },
                { # Page 20
                    "name":"ItemOperations",
                    0x05: ('ItemOperations', None),
                    0x06: ('Fetch', None),
                    0x07: ('Store', None),
                    0x08: ('Options', None),
                    0x09: ('Range', None),
                    0x0a: ('Total', None),
                    0x0b: ('Properties', None),
                    0x0c: ('Data', None),
                    0x0d: ('Status', None),
                    0x0e: ('Response', None),
                    0x0f: ('Version', None),
                    0x10: ('Schema', None),
                    0x11: ('Part', None),
                    0x12: ('EmptyFolderContents', None),
                    0x13: ('DeleteSubFolders', None),
                    0x14: ('UserName', None),
                    0x15: ('Password', None),
                    0x16: ('Move', None),
                    0x17: ('DstFldId', None),
                    0x18: ('ConversationId', None),
                    0x19: ('MoveAlways', None),
                },
                { # Page 21
                },
                { # Page 22 - Email2
                    "name":"Email2",
                    0x05: ('UmCallerID', None),
                    0x06: ('UmUserNotes', None),
                    0x07: ('UmAttDuration', None),
                    0x08: ('UmAttOrder', None),
                    0x09: ('ConversationId', None),
                    0x0a: ('ConversationIndex', None),
                    0x0b: ('LastVerbExecuted', None),
                    0x0c: ('LastVerbExecutionTime', None),
                    0x0d: ('ReceivedAsBcc', None),
                    0x0e: ('Sender', None),
                    0x0f: ('CalendarType', None),
                    0x10: ('IsLeapMonth', None),
                    0x11: ('AccountId', None),
                    0x12: ('FirstDayOfWeek', None),
                    0x13: ('MeetingMessageType', None),
                },
            ]
        }
}

# Special WBXML tokens.
SWITCH_PAGE = 0x00
END         = 0x01
STR_I       = 0x03
STR_T       = 0x83
OPAQUE      = 0xC3


class wbxmldocument(object):
    r'''Class for WBXML DOM document objects.
    '''
    def __init__(self):
        r'''Creates a new WBXML DOM document object.
        '''
        self.encoding = ''
        self.schema = ''
        self.version = ''
        self.__stringtable = []
        self.root = None

    def __str__(self):
        r'''Converts this document object (and contained element objects,
            recursively) to string.
        '''
        return \
            r'<?xml version="1.0" encoding="' + self.encoding + r'"?>' + \
            '\n\n' + \
            r'<!DOCTYPE ' + self.schema + r'>' + \
            '\n\n' + \
            r'<!-- WBXML version: ' + self.version + r' -->' + \
            '\n\n' + \
            r'<!-- Contents of string table: "' + str(self.stringtable) + r'" -->' + \
            '\n\n' + \
            str(self.root)

    def addchild(self, root):
        r'''Sets this document's root object. It's a convenience method meant
            for easing the implementation of the DOM parser.
        '''
        self.root = root
        root.parent = self

    def tobytes(self):
        version_major = int(self.version.split(".")[0])
        version_minor = int(self.version.split(".")[1])

        enc_token = 1
        for (token,enc) in _applications.iteritems():
            if enc == self.schema:
                enc_token = token
                break
        
        chars_token = 0
        for (token,enc) in _charsets.iteritems():
            if enc == self.encoding:
                chars_token = token
                break

        assert len(self.__stringtable) == 0

        return pack("BBBB", ((version_major-1)<<4)|version_minor, enc_token, chars_token, len(self.__stringtable))+self.root.tobytes(enc_token)

    @property
    def stringtable(self):
        string = ''
        table = []
        for code in self.__stringtable:
            if code != 0x00:
                string += chr(code)
            else:
                table.append(string)
                string = ''

        return table

    @stringtable.setter
    def stringtable(self, table):
        self.__stringtable = table


class wbxmlelement(object):
    r'''Class for WBXML DOM elements.
    '''
    def __init__(self, name = None, attributes = {}, page_num=None):
        r'''Creates a new WBXML DOM element object.
        '''
        self.page_num = page_num
        self.parent = None
        self.name = name
        self.attributes = dict(attributes)
        self.children = []

    def __str__(self):
        r'''Converts this element object (and contained element objects,
            recursively) to string.
        '''
        return self.tostring(0)

    def tostring(self, level):
        r'''Converts this element object (and contained element objects,
            recursively) to string, idented to the given ident level.
        '''
        ident = level * '  '
        attributes = ''
        for (name, value) in self.attributes.items():
            attributes += ' ' + name + '="' + value + '"'

        closebracket = ''
        children = ''
        closetag = ''

        start_name = self.name
        if self.page_num != None and "name" in _applications[0x1]["elements"][self.page_num]:
            start_name = _applications[0x1]["elements"][self.page_num]["name"]+":"+start_name

        if len(self.children) > 0:
            closebracket = '>\n'
            closetag = ident + '</' + start_name + '>'
            for child in self.children:
                children += child.tostring(level + 1)
        else:
            closebracket = ' />'
        return ident + '<' + start_name + attributes + closebracket + children + closetag + '\n'

    def tobytes(self, enc_token):
        tag_val = 0
        tag_pagenum = 0
        for page_num in range(len(_applications[enc_token]["elements"])):
            if self.page_num != None and page_num != self.page_num:
                continue
            for token,tokeninfo in _applications[enc_token]["elements"][page_num].iteritems():
                if tokeninfo[0] == self.name:
                    tag_val = token
                    tag_pagenum = page_num
                    break
        if len(self.attributes):
            tag_val |= 0b10000000
        if len(self.children):
            tag_val |= 0b01000000
        byte_data = pack("BBB", 0, tag_pagenum, tag_val)
        assert len(self.attributes) == 0
        for child in self.children:
            byte_data += child.tobytes(enc_token)
        byte_data += pack("B", 1)
        return byte_data

    def addchild(self, child):
        r'''Adds a child element to this element object.
        '''
        self.children.append(child)
        child.parent = self


class wbxmlstring(object):
    r'''Class for text elements.
    '''
    def __init__(self, value, opaque=False):
        r'''Creates a new text element object from a string.
        '''
        self.__value = value
        self.is_opaque = opaque

    def __str__(self):
        r'''Converts this text element to string.
        '''
        return self.tostring(0)

    def tobytes(self, enc_token):
        if self.is_opaque:
            return pack("BB", OPAQUE, len(self.__value))+self.__value
        return pack("B", STR_I)+self.__value+pack("B",0)

    def tostring(self, level):
        r'''Converts this text element to string, idented to the given ident
            level.
        '''
        if self.is_opaque:
            return level * '  ' + "OPAQUE: "+self.__value.encode("hex") + '\n'
        return level * '  ' + self.__value + '\n'


class wbxmlreader(object):
    r'''File reader for WBXML documents. Implements several conveniences for
        parsing WBXML files.
    '''
    def __init__(self, path):
        r'''Creates a new WBXML reader for the file at the given path.
        '''
        self.__bytes = open(path, 'rb')

    def __iter__(self):
        r'''Returns an iterator over this reader (actually, the object itself).
        '''
        return self

    def next(self):
        r'''Reads one binary token from the WBXML file and advances the file
            pointer one position. If the end-of-file has already been reached,
            raises the StopIteration exception.
        '''
        return self.read()

    def read(self, length = None):
        r'''Reads a sequence of one or more tokens from the underlying WBXML
            file, incrementing the file pointer accordingly.

            If the length is ommited, one token is read and returned as an
            integer; otherwise, at most (length) tokens are read and returned as
            a character string. This holds true even for length = 1, so
            reader.read(1) returns a single-character string.

            If a previous operation reached the end-of-file, this method raises
            the StopIteration exception.
        '''
        data = self.__bytes.read(1 if length == None else length)

        if len(data) == 0:
            raise StopIteration()

        return ord(data) if length == None else data

    def readopaque(self):
        r'''Reads an opaque data buffer from the WBXML file, and returns it
            as a base64 string. The file pointer is incremented until past the
            end of the buffer.
        '''
        length = self.read()
        data = self.read(length)
        return b64encode(data)

    def readstring(self):
        r'''Reads tokens from the WBXML file until the end-of-string character
            (0x00) is reached, returning the result as a string. The file
            pointer is incremented until past the end-of-string character.
        '''
        data = ''
        while True:
            char = self.read(1)
            if char == '\0':
                return data
            data += char


class wbxmlparser(object):
    r'''A DOM parser for Wireless Binary XML documents.
    '''
    def __init__(self, applications={}, charsets={}):
        r'''Creates a new parser object.
        '''
        self.__applications = dict(_applications)
        self.__applications.update(applications)
        
        self.__charsets = dict(_charsets)
        self.__charsets.update(charsets)

        self.__encoding = None
        self.__page = 0
        self.__strings = []

    def parse(self, data):
        r'''Parses a WBXML file and returns a WBXML DOM document object.

            If data is a string, it is interpreted as a path to a WBXML file;
            otherwise, it's expected to be a wbxmlreader object.
        '''
        if isinstance(data, basestring):
            data = wbxmlreader(data)

        doc = wbxmldocument()
        try:
            self.__version(data, doc)
            self.__publicid(data, doc)
            self.__charset(data, doc)
            self.__stringtable(data, doc)
            self.__body(data, doc)
        except Exception as e:
            print_exc(file=stdout)

        return doc

    def __get(self, *keys):
        r'''Walks the current WBXML token specification, returning the object
            (either leaf or subtree) at the end of the path.

            If the path is not found, raises a KeyError exception.
        '''
        data = self.__encoding['elements']
        try:
            for key in keys:
                data = data[key]
            return data
        except:
            raise KeyError('(' + ', '.join([hex(k) for k in keys]) + ')')

    def __version(self, data, doc):
        r'''Sets the version attribute of a WBXML DOM document object.
        '''
        token = data.read()
        minor = 0b1111 & token
        major = (token >> 4) + 1
        doc.version = `major` + '.' + `minor`

    def __publicid(self, data, doc):
        r'''Sets the schema attribute of a WBXML DOM document object. Also sets
            the active WBXML token specification.
        '''
        token = data.read()
        self.__encoding = self.__applications[token]
        doc.schema = self.__encoding['dtd']

    def __charset(self, data, doc):
        r'''Sets the encoding attribute of a WBXML DOM document object.
        '''
        token = data.read()
        doc.encoding = self.__charsets[token]

    def __stringtable(self, data, doc):
        r'''Sets the string table of a WBXML DOM document object.
        '''
        length = data.read()
        self.__strings = [data.read() for i in range(0, length)]
        doc.stringtable = self.__strings

    def __readstringtable(self, offset):
        table = self.__strings
        string = ''
        for i in range(offset, len(table)):
            code = table[i]
            if code != 0x00:
                string += chr(code)
            else:
                break

        return string

    def __body(self, data, doc):
        r'''Parses the body of a WBXML document, constructing the element DOM
            tree.
        '''
        self.__elements(data, doc)

    def __elements(self, data, parent):
        r'''Parses the children of a parent WBXML element, as well as their
            children recursively.
        '''
        for token in data:
            node = None
            if token == END:
                return
            elif token == STR_I:
                node = wbxmlstring(data.readstring())
            elif token == OPAQUE:
                node = wbxmlstring(data.readopaque())
            elif token == SWITCH_PAGE:
                self.__page = data.read()
                continue
            else:
                (tag, hasattributes, hascontents) = (
                    (0b00111111 & token),               # Base tag code
                    ((0b10000000 & token) >> 7) == 1,   # "Has attributes" bit
                    ((0b01000000 & token) >> 6) == 1    # "Has contents" bit
                )

                name = self.__get(self.__page, tag, 0)
                node = wbxmlelement(name)
                if hasattributes:
                    self.__attributes(data, tag, node)
                if hascontents:
                    self.__elements(data, node)
            parent.addchild(node)

    def __attributes(self, data, element, node):
        r'''Parses the attributes of a WBXML element.
        '''
        for token in data:
            if token == END:
                return
            elif token == SWITCH_PAGE:
                self.__page = data.read()
            else:
                self.__value(data, element, token, node)

    def __value(self, data, element, attribute, node):
        (name, value) = self.__get(self.__page, element, 1, attribute)
        if value != None and not (isinstance(value, dict) or callable(value)):
            node.attributes[name] = value
            return

        token = data.read()
        if token == STR_I:
            node.attributes[name] = data.readstring()
        elif token == STR_T:
            offset = data.read()
            node.attributes[name] = self.__readstringtable(offset)
        elif value == None:
            node.attributes[name] = str(token)
        elif isinstance(value, dict):
            node.attributes[name] = value[token]
        else:
            node.attributes[name] = value(node, token)


def dialog():
    r'''Opens the input and output file dialogs, then calls the parse() function.
    '''
    from Tkinter import Tk
    import tkFileDialog
    root = Tk()
    root.withdraw()
    
    from sys import stdin, stdout
    
    stdout.write('Path to the input WBXML file: ')

    binary = tkFileDialog.askopenfilename(
        master = root,
        title = 'Open WBXML File',
        filetypes = [('Wireless Binary XML', '.wbxml'), ('All Files', '*')]
    )

    if binary == '':
        root.quit()
        return

    stdout.write(binary + '\n\n')

    stdout.write('Path to the output plain-text XML file: ')

    plain = tkFileDialog.asksaveasfilename(
        master = root,
        title = "Save Plain-Text XML File",
        defaultextension = ".xml",
        filetypes = [('Plain-Text XML', '.xml'), ('All Files', '*')]
    )

    if plain == '':
        root.quit()
        return

    stdout.write(plain + '\n\n')
    
    root.quit()
    
    stdout.write('Decoding WBXML file... ')

    parse(binary, plain)
    
    stdout.write('Done.')
    stdin.read()


def parse(binary, plain = None):
    r'''Parses an input WBXML file. Results are written to a plain-text output
        file if it is given; otherwise, the standard output is used.
    '''
    wbxml = wbxmlparser().parse(binary)
    out = open(plain, 'w') if plain != None else stdout
    out.write(str(wbxml))
    if hasattr(out, 'close'):
        out.close()


def main():
    r'''Function invoked when this module is ran as a script.
    '''
    import sys
    if len(sys.argv) > 1:
        parse(*sys.argv[1:])
    else:
        dialog()


# Command-line entry point
if __name__ == '__main__':
    main()
