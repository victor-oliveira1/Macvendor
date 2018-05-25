#!/bin/python3
#Copyright © 2018 Victor Oliveira <victor.oliveira@gmx.com>
#This work is free. You can redistribute it and/or modify it under the
#terms of the Do What The Fuck You Want To Public License, Version 2,
#as published by Sam Hocevar. See the COPYING file for more details.

import argparse
from urllib import request
from os import path

OUI_URL = 'http://standards-oui.ieee.org/oui.txt'
OUI_FILE = path.expanduser('~/.oui.txt')
MAC_SEPARATORS = [':', '-']

def Vendor(mac):
    m = MAC(mac)
    vendor = m.vendor
    return m.mac_formatted, vendor

class MAC:
    def __init__(self, mac, force=False):
        self.mac = mac
        self._Format()
        self._DownloadOUI(force)
        self._Search()

    def _DownloadOUI(self, force):
        if not path.isfile(OUI_FILE) or force:
            print('Downloading OUI file...')
            req = request.urlopen(OUI_URL)
            text = req.read().decode()
            with open(OUI_FILE, 'w') as file:
                file.write(text)
            print('Download OK!')

    def _Format(self):
        #Remove separators
        for mac_separator in MAC_SEPARATORS:
            self.mac = self.mac.replace(mac_separator, str())
        self.mac_raw = self.mac

        #Check len size
        len_mac = len(self.mac)
        if len_mac < 6 or len_mac > 12:
            raise ValueError('Invalid MAC address')

        #Check HEX
        int(self.mac, 16)

        #Format MAC
        self.mac_formatted = ':'.join(
            self.mac[i:i+2] for i in range(0,12,2)
            ).upper()

    def _Search(self):
        self.mac_split = self.mac_raw[:6]
        with open(OUI_FILE) as file:
            while True:
                line = file.readline()
                if line:
                    if self.mac_split.upper() in line:
                        self.mac_prefix = line.split()[0]
                        self.vendor = line.split('\t')[-1]
                        self.vendor = self.vendor.strip('\n')
                else:
                    break

        if not hasattr(self, 'vendor'):
            self.vendor = None

######################################################################
if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('MAC',
                      help='MAC address or file')
    args.add_argument('-r',
                      '--repair',
                      help='Repair OUI file',
                      action='store_true')
    args = args.parse_args()

    if path.isfile(args.MAC):
        with open(args.MAC) as file:
            for line in file.readlines():
                mac = ''.join(line.split())
                try:
                    mac_formatted, vendor = Vendor(mac)
                    print('{} - {}'.format(mac_formatted, vendor))
                except ValueError:
                    print('Invalid MAC:', mac)
    else:
        try:
            mac, vendor = Vendor(args.MAC)
            print('{} - {}'.format(mac, vendor))
        except ValueError:
            print('Invalid MAC:', args.MAC)
