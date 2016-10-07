from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from xml.dom.minidom import getDOMImplementation
from zope.interface import implements
from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer

version = "1.0"

class AutoDiscoveryProducer(object):
	implements(IBodyProducer)
	def __init__(self, email_address):
		impl = getDOMImplementation()
		newdoc = impl.createDocument(None, "Autodiscover", None)		
		top_element = newdoc.documentElement
		top_element.setAttribute("xmlns", "http://schemas.microsoft.com/exchange/autodiscover/mobilesync/requestschema/2006")
		req_elem = newdoc.createElement('Request')
		top_element.appendChild(req_elem)
		email_elem = newdoc.createElement('EMailAddress')
		req_elem.appendChild(email_elem)
		email_elem.appendChild(newdoc.createTextNode(email_address))
		resp_schema = newdoc.createElement('AcceptableResponseSchema')
		req_elem.appendChild(resp_schema)
		resp_schema.appendChild(newdoc.createTextNode("http://schemas.microsoft.com/exchange/autodiscover/mobilesync/responseschema/2006"))
		self.body = newdoc.toxml("utf-8")
		self.length = len(self.body)

	def startProducing(self, consumer):
		consumer.write(self.body)
		return succeed(None)

	def pauseProducing(self):
		pass

	def stopProducing(self):
		pass

class AutoDiscover:
	"""The AutoDiscover class is used to find EAS servers using only an email address"""
	STATE_INIT = 0
	STATE_XML_REQUEST = 1
	STATE_XML_AUTODISCOVER_REQUEST = 2
	STATE_INSECURE = 3
	STATE_SRV = 4
	STATE_REDIRECT = 5
	LAST_STATE = 6
	AD_REQUESTS = {STATE_XML_REQUEST:"https://%s/autodiscover/autodiscover.xml", 
					STATE_XML_AUTODISCOVER_REQUEST:"https://autodiscover.%s/autodiscover/autodiscover.xml",
					STATE_INSECURE:"http://autodiscover.%s/autodiscover/autodiscover.xml"}

	def __init__(self, email):
		self.email = email
		self.email_domain = email.split("@")[1]
		self.agent = Agent(reactor)
		self.state = AutoDiscover.STATE_INIT
		self.redirect_urls = []
	def handle_redirect(self, new_url):
		if new_url in self.redirect_urls:
			raise Exception("AutoDiscover", "Circular redirection")
		self.redirect_urls.append(new_url)
		self.state = AutoDiscover.STATE_REDIRECT
		print "Making request to",new_url
		d = self.agent.request(
		    'GET',
		    new_url,
		    Headers({'User-Agent': ['python-EAS-Client %s'%version]}),
		    AutoDiscoveryProducer(self.email))
		d.addCallback(self.autodiscover_response)
		d.addErrback(self.autodiscover_error)
		return d
	def autodiscover_response(self, result):
		print "RESPONSE",result,result.code
		if result.code == 302:
			# TODO: "Redirect responses" validation
			return self.handle_redirect(result.headers.getRawHeaders("location")[0])
		return result
	def autodiscover_error(self, error):
		print "ERROR",error,error.value.reasons[0]
		if self.state < AutoDiscover.LAST_STATE:
			return self.autodiscover()
		raise error
	def autodiscover(self):
		self.state += 1
		if self.state in AutoDiscover.AD_REQUESTS:
			print "Making request to",AutoDiscover.AD_REQUESTS[self.state]%self.email_domain
			body = AutoDiscoveryProducer(self.email)
			d = self.agent.request(
			    'GET',
			    AutoDiscover.AD_REQUESTS[self.state]%self.email_domain,
			    Headers({'User-Agent': ['python-EAS-Client %s'%version]}),
			    body)
			d.addCallback(self.autodiscover_response)
			d.addErrback(self.autodiscover_error)
			return d
		else:
			raise Exception("Unsupported state",str(self.state))