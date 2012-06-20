#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import commands
import requests
from optparse import OptionParser

LINUXMANPAGES_SEARCH = "http://www.linuxmanpages.com/search.php"
READABILITY_EMAIL = 'everbird+stowe@inbox.readability.com'

def run(options):
    url = LINUXMANPAGES_SEARCH
    payload = {
            'submitted': '1',
            'section': '-1',
            'term': options.name,
            }
    r = requests.post(url, data=payload)
    result = r.url
    print 'man page found:', result
    sendmail(options.name, result)

    print 'all done.'

def sendmail(name, url):
    print 'sending %s to readability' % url
    r = commands.getoutput("echo %s | mutt -s '%s' -- %s" % \
            (name, url, READABILITY_EMAIL))
    print 'result', r or 'ok'

if __name__ == '__main__':
    u = """%prog rman"""
    parser = OptionParser(u)
    parser.add_option('-n', '--name',
            help='Command name to search.',
            default='BookNote')
    options, args = parser.parse_args()

    if not options.name:
        print 'no command name specified'
        exit(1)

    run(options)
