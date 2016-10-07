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

import httplib, urllib

class ASHTTPConnector(object):
    """ActiveSync HTTP object"""
    USER_AGENT = "Python"
    POST_URL_TEMPLATE = "/Microsoft-Server-ActiveSync?Cmd=%s&User=%s&DeviceId=123456&DeviceType=Python"
    POST_GETATTACHMENT_URL_TEMPLATE = "/Microsoft-Server-ActiveSync?Cmd=%s&AttachmentName=%s&User=%s&DeviceId=123456&DeviceType=Python"

    def __init__(self, server, port=443, ssl=True):
        
        self.server = server
        self.port = port
        self.ssl = ssl
        self.policykey = 0
        self.headers = {
                        "Content-Type": "application/vnd.ms-sync.wbxml",
                        "User-Agent" : self.USER_AGENT,
                        "MS-ASProtocolVersion" : "14.1",
                        "Accept-Language" : "en_us"
                        }
        return

    def set_credential(self, username, password):
        import base64
        self.username = username
        self.credential = base64.b64encode(username+":"+password)
        self.headers.update({"Authorization" : "Basic " + self.credential})

    def do_post(self, url, body, headers, redirected=False):
        if self.ssl:
            conn = httplib.HTTPSConnection(self.server, self.port)
            conn.request("POST", url, body, headers)
        else:
            conn = httplib.HTTPConnection(self.server, self.port)
            conn.request("POST", url, body, headers)
        res = conn.getresponse()
        if res.status == 451:
            self.server = res.getheader("X-MS-Location").split()[2]
            if not redirected:
                return self.do_post(url, body, headers, False)
            else:
                raise Exception("Redirect loop encountered. Stopping request.")
        else:
            return res


    def post(self, cmd, body):
        url = self.POST_URL_TEMPLATE % (cmd, self.username)
        res = self.do_post(url, body, self.headers)
        #print res.status, res.reason, res.getheaders()
        return res.read()

    def fetch_multipart(self, body, filename="fetched_file.tmp"):
        """http://msdn.microsoft.com/en-us/library/ee159875(v=exchg.80).aspx"""
        headers = self.headers
        headers.update({"MS-ASAcceptMultiPart":"T"})
        url = self.POST_URL_TEMPLATE % ("ItemOperations", self.username)
        res = self.do_post(url, body, headers)
        if res.getheaders()["Content-Type"] == "application/vnd.ms-sync.multipart":
            PartCount = int(res.read(4))
            PartMetaData = []
            for partindex in range(0, PartCount):
                PartMetaData.append((int(res.read(4))), (int(res.read(4))))
            wbxml_part = res.read(PartMetaData[0][1])
            fetched_file = open(filename, "wb")
            for partindex in range(1, PartCount):
                fetched_file.write(res.read(PartMetaData[0][partindex]))
            fetched_file.close()
            return wbxml, filename
        else:
            raise TypeError("Client requested MultiPart response, but server responsed with inline.")

    def get_attachment(self, attachment_name): #attachment_name = DisplayName of attachment from an MSASAIRS.Attachment object
        url = self.POST_GETATTACHMENT_URL_TEMPLATE  % ("GetAttachment", attachment_name, self.username)
        res = self.do_post(url, "", self.headers)
        try:
            content_type = res.getheader("Content-Type")
        except:
            content_type = "text/plain"
        res.status
        return res.read(), res.status, content_type

    def get_options(self):
        conn = httplib.HTTPSConnection(self.server, self.port)
        conn.request("OPTIONS", "/Microsoft-Server-ActiveSync", None, self.headers)
        res = conn.getresponse()
        return res

    def options(self):
        res = self.get_options()
        if res.status is 200:
            self._server_protocol_versions = res.getheader("ms-asprotocolversions")
            self._server_protocol_commands = res.getheader("ms-asprotocolcommands")
            self._server_version = res.getheader("ms-server-activesync")
            return True
        else:
            print "Connection Error!:"
            print res.status, res.reason
            for header in res.getheaders():
                print header[0]+":",header[1]
            return False

    def get_policykey(self):
        return self.policykey

    def set_policykey(self, policykey):
        self.policykey = policykey
        self.headers.update({ "X-MS-PolicyKey" : self.policykey })