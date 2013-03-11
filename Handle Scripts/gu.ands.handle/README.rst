
ANDS Handle management command line tool
========================================

Installation
------------

 * run python bootstrap.py
 * run ./bin/buildout

create a config file name 'ands.ini' with following content and replace values 
according to your environment.

[gu.ands.handle]
url = http://example.com/pids
appid = abcd1234efgh5678
identifier = id
authdomain = domain


Usage:
------

Currently the cammand line tool tries to find the ini file in the current worknig directory.

Run ./bin/pid without any options to see all available actions.
