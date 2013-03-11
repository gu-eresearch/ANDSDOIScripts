
import urllib2
import urllib
import urlparse
from string import Template
from xml.dom.minidom import parse

PIDREQUEST = Template(u'''<?xml version="1.0" encoding="UTF-8"?>
<request name="${name}">
  <properties>
    <property name="appId" value="${appid}" />
    <property name="identifier" value="${identifier}" />
    <property name="authDomain" value="${authdomain}" />
  </properties>
</request>''')


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


class Identifier(object):

    def __init__(self, idstring):
        self.id = idstring
        self.properties = {}


class AndsPidResponse(object):

    def __init__(self, xml):
        doc = parse(xml)
        respelem = doc.documentElement
        self.success = respelem.getAttribute("type") == u"success"
        for idelem in respelem.getElementsByTagName(u"identifier"):
            self.identifier = Identifier(idelem.getAttribute("handle"))
            for prop in idelem.getElementsByTagName(u"property"):
                self.identifier.properties[int(prop.getAttribute("index"))] = (prop.getAttribute("type"),
                                                                          prop.getAttribute("value"))
        for timeelem in respelem.getElementsByTagName(u"timestamp"):
            self.timestamp = getText(timeelem.childNodes)
        for msgelem in respelem.getElementsByTagName(u"message"):
            self.message = getText(msgelem.childNodes)
        for idselem in respelem.getElementsByTagName(u"identifiers"):
            self.identifiers = []
            for idelem in idselem.getElementsByTagName(u"identifier"):
                self.identifiers.append(idelem.getAttribute(u"handle"))

    def __str__(self):
        if self.success:
            ret = [u"Request success"]
            if hasattr(self, "identifiers"):
                for ident in self.identifiers:
                    ret.append(ident)
            else:
                ret.append(self.identifier.id)
                for key in sorted(self.identifier.properties.keys()):
                    props = self.identifier.properties[key]
                    ret.append("%d - %s - %s" % (key, props[0], props[1]))
        else:
            ret = [u"Request Failed",
                   self.message]
        return "\n".join(ret)


class AndsPidService(object):

    def __init__(self, url, appid, identifier, authdomain):
        """
        url ... service endpoint
        appid ... service issued key identifying PIDS trusted client
        identifier ... handle owner
        authDomain ... authdomain user is operating
        """
        self.url = url
        if not url.endswith("/"):
            self.url += "/"
        self.appid = appid
        self.identifier = identifier
        self.authdomain = authdomain
        self.requesttmpl = Template(PIDREQUEST.safe_substitute(appid=appid,
                                                        identifier=identifier,
                                                        authdomain=authdomain))

    def post(self, params, method):
        params = urllib.urlencode(params)
        url = urlparse.urljoin(self.url, "%s?%s" % (method, params))
        data = self.requesttmpl.substitute(name=method)
        headers = {"Content-Type": 'text/xml; charset="UTF-8"',
                   "Content-Encoding": "UTF-8"}
        req = urllib2.Request(url, data, headers)
        resp = urllib2.urlopen(req)
        # check for a tleast 501 errors.....
        return AndsPidResponse(resp)

    def mint(self, type, value, index=None):
        """
        type ... empty, 'DESC' or 'URL'
        value ... empty, brief description, or URL
        index .. optional
        """
        params = {"type": type,
                  "value": value}
        if index:
            params["index"] = index
        return self.post(params, u"mint")

    def addValue(self, handle, type, value):
        params = {"handle": handle,
                  "type": type,
                  "value": value}
        return self.post(params, u"addValue")

    def addValueByIndex(self, handle, type, value, index):
        params = {"handle": handle,
                  "type": type,
                  "value": value,
                  "index": index}
        return self.post(params, u"addValueByIndex")

    def modifyValueByIndex(self, handle, index, value):
        params = {"handle": handle,
                  "index": index,
                  "value": value}
        return self.post(params, u"modifyValueByIndex")

    def deleteValueByIndex(self, handle, index):
        params = {"handle": handle,
                  "index": index}
        return self.post(params, u"deletValueByIndex")

    def listHandles(self, starthandle=None):
        if starthandle:
            params = {"startHandle": starthandle}
        else:
            params = {}
        return self.post(params, u"listHandles")

    def getHandle(self, handle):
        params = {"handle": handle}
        return self.post(params, u"getHandle")
