#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
从pasteboard的文本中按指定dsym做符号链接，用于查看umeng上的异常
"""

import commands
from optparse import OptionParser
import subprocess

class InvalidOptionsError(Exception):
    pass

def run(options):
    if options.pb:
        addresses = get_addresses_from_pb(options.name)
    elif options.source:
        addresses = get_addresses_from_file(options.name, options.source)
    else:
        raise InvalidOptionsError('invalid options, how could it happend?')
    if not addresses:
        print 'no address in %s' % 'pasteboard' if options.pb else options.name
        return

    r = run_atos(options.dsym, addresses)
    print r
    if options.copy:
        copy(r)

def paste():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    data = p.stdout.read()
    return data

def copy(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    #retcode = p.wait()

def get_addresses_from_pb(name):
    content = paste()
    lines = [x.strip() for x in content.split('\n')]
    return get_addresses(name, lines)

def run_atos(path, addresses):
    address_arg = ' '.join(addresses)
    r = commands.getoutput('atos -o %s -arch armv6 %s' % (path, address_arg))
    return r

def get_addresses_from_file(name, path):
    lines = [x.strip() for x in open(path)]
    return get_addresses(name, lines)

def get_addresses(name, lines):
    lines = [x for x in lines if name in x]
    addresses = [extract_address(name, x) for x in lines]
    addresses = [x for x in addresses if x]
    addresses.reverse()
    return addresses

def extract_address(name, content):
    items = content.split()
    return items[2] if len(items) >= 4 and items[1]==name else ''

if __name__ == '__main__':
    u = """%prog extract-app-address"""
    parser = OptionParser(u)
    parser.add_option('-c', '--copy',
            help='Copy result to pasteboard.',
            action='store_true')
    parser.add_option('-p', '--pb',
            help='Pick error log from pasteboard.',
            action='store_true')
    parser.add_option('-s', '--source',
            help='Error log file path.',
            default='/Users/everbird/trash/umeng-error.log')
    parser.add_option('-n', '--name',
            help='The app name.',
            default='BookNote')
    parser.add_option('-d', '--dsym',
            help='The dsym file path.',
            default='/Users/everbird/trash/Release/BookNote.app/BookNote')
    options, args = parser.parse_args()

    if not options.name:
        print 'no app name specific.'
        exit(1)
    if not options.source and not options.pb:
        print 'no error log specific.'
        exit(1)
    if not options.dsym:
        print 'no dsym file specific.'
        exit(1)

    run(options)
