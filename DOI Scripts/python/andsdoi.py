from urllib2 import urlopen, Request
from urllib import urlencode


class AndsDoiData(object):
    def __init__(self):
        # Some templates for making our XML
        self.xml_xmlWrapper = "<resource xmlns=\"http://datacite.org/schema/kernel-2.1\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://datacite.org/schema/kernel-2.1 http://schema.datacite.org/meta/kernel-2.1/metadata.xsd\">\n%s</resource>"
        self.xml_id = "<identifier identifierType=\"DOI\">%s</identifier>\n"
        self.xml_title = "<titles><title>%s</title></titles>\n"
        self.xml_publisher = "<publisher>%s</publisher>\n"
        self.xml_pubYear = "<publicationYear>%s</publicationYear>\n"
        self.xml_creator = "<creator><creatorName>%s</creatorName></creator>\n"
        self.xml_creatorWrapper = "<creators>\n%s</creators>\n"

    doiConfig = {'apiKey': '<Your Api Key Here>',
                 'apiBaseUrl': 'https://services.ands.org.au/doi/1.1'}

    def getApiUrl(self, page):
        baseUrl = self.doiConfig["apiBaseUrl"]
        apiKey = self.doiConfig["apiKey"]

        #https://services.ands.org.au/doi/1.1/mint.{response_type}/?app_id={app_id}&url={url}
        # Create = https://test.ands.org.au/home/dois/doi_mint.php?app_id=$app_id&url=$url
        if page == "create":
            return baseUrl + "/mint.xml/?debug=true&app_id=" + apiKey + "&url="

        # Update = https://test.ands.org.au/home/dois/doi_update.php?app_id=$app_id&DOI=$DOI_id[&url=$url]
        if page == "update":
            return baseUrl + "/update.xml/?app_id=" + apiKey + "&doi="

        # Activate = https://test.ands.org.au/home/dois/doi_activate.php?app_id=$app_id&DOI=$DOI_id
        if page == "activate":
            return baseUrl + "/activate.xml/?app_id=" + apiKey + "&doi="

        # Deactivate = https://test.ands.org.au/home/dois/doi_deactivate.php?app_id=$app_id&DOI=$DOI_id
        if page == "deactivate":
            return baseUrl + "/activate.xml/?app_id=" + apiKey + "&doi="

        # Get = https://test.ands.org.au/home/dois/doi_xml.php?DOI=$DOI_id
        if page == "get":
            return baseUrl + "/xml.xml/?doi="

    def buildXml(self, data, doi):
        xmlString = ""

        ## Check metadata validity along the way
        if not doi:
            ## During DOI creation a URL is mandatory,
            ##   but not part of the XML, so...
            ## 1) Skip this is we have a DOI
            ## 2) Make sure it exists otherwise
            ## 3) But don't add into the XML
            url = data.get('url', None)
            if not url:
                return None
            # We have to fake a DOI to get through the validator
            # FIXME: do we really have to fake this?
            #xmlString += self.xml_id % '10.1000/182'
        else:
            ## Once we have a DOI it needs to go in the XML.
            ## URL is optional in this case, and still not in XML
            xmlString += self.xml_id % (doi)

        creators = data.get("creators", None)
        if not creators:
            return None
        else:
            creatorString = ""
            for creator in creators:
                creatorString += self.xml_creator % (creator)
            xmlString += self.xml_creatorWrapper % (creatorString)

        title = data.get("title", None)
        if not title:
            return None
        else:
            xmlString += self.xml_title % (title)

        publisher = data.get("publisher", None)
        if not publisher:
            return None
        else:
            xmlString += self.xml_publisher % (publisher)

        pubYear = data.get("pubYear", None)
        if not pubYear:
            return None
        else:
            xmlString += self.xml_pubYear % (pubYear)

        return self.xml_xmlWrapper % (xmlString)

    def urlGet(self, url):
        try:
            resp = urlopen(url)
            return str(resp.code), resp.read()
        except Exception, e:
            print "ERROR", e
        return None, None

    def urlPost(self, url, postBody):
        try:
            headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Accept": "text/plain"}
            params = {'xml': postBody}
            h = Request(url, urlencode(params), headers)
            res = urlopen(h)
            return str(res.code), res.read()
        except Exception, e:
            print "ERROR in POST", e
        return None, None

    def createDoi(self, data):
        if not data:
            return

        xmlString = self.buildXml(data, None)
        if xmlString is None:
            self.throwError("Error during XML creation")
            return
        else:
            print "XML:\n", xmlString

        andsUrl = self.getApiUrl("create") + data['url']
        print "About to create DOI via URL: '{}'", andsUrl
        (code, body) = self.urlPost(andsUrl, xmlString)
        print "Response Code: '{}'", code
        print "Response Body: '{}'", body
        if code != "200":
            print "Invalid response from ANDS server, code "+code+ ": "+body
            return

        # Grab the DOI from their repsonse string
        words = body.split()
        if len(words) != 6:
            print "We received a SUCCESS response from ANDS, but the format was not as expected. Response body: '"+body+"'"
            return
        doi = words[2]
        print "MINTED DOI:", doi

    def process(self, action, data):
        switch = {
            "createDoi": self.createDoi,
            # "updateDoi": self.updateDoi,
            # "activateDoi": self.activateDoi,
            # "deactivateDoi": self.deactivateDoi,
            # "getXml": self.getXml
        }
        switch.get(action, self.unknownAction)(data)

    def unknownAction(self, data):
        print "Unknown Action"



if __name__ == '__main__':
    ob = AndsDoiData()
    data = {'title': '<Title goes here>',
            'creators': ['<Author, One>', '<Author, Two>'],
            'publisher': '<Publisher>',
            'url': '<The url to point back to>',
            'pubYear': '<a year>'}
    ob.process("createDoi", data)
