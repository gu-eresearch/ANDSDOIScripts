import os.path
from ConfigParser import SafeConfigParser

# read config file here and populate dictionary


# TODO: ands.ini is read from current working directory...
#       make this configurable? or do a better search for it?
def readIniFile(ininame=None):
    if ininame is None:
        ininame = os.path.abspath('ands.ini')
    parser = SafeConfigParser()
    parser.read(ininame)
    if not parser.has_section('gu.ands.handle'):
        return {'url': u'http://example.com/pids',
                'appid': u'abcd1234efgh5678',
                'identifier': u'id',
                'authdomain': u'domain'}
    return dict(parser.items('gu.ands.handle'))


CONFIG = readIniFile()
