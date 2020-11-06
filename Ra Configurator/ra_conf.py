#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import array
import binascii
import configparser
import crcmod
import math
import numpy as np
import os
import signal
import string
import struct



# Handler to allow a graceful exit in case of Ctrl-C
def sigint_handler (signal, frame):
    print(" Good bye!")
    os._exit(0)



class ConfigBlob:
    def __init__(self, number):
        self.param = {}
        self.param['version'] = 1
        self.param['serialnumber'] = number

        # Set defaults
        self.param['usbvid'] = 0x169C
        self.param['usbpid'] = 0x05DC
        self.param['usbversion'] = 0x0100

        self.param['referencefrequency'] = 12.8e6
        self.param['rssicorrectionlnaon'] = -16.0
        self.param['rssicorrectionlnaoff'] = 13.0
        self.param['baudrate'] = 115200

        self.param['namebluetooth'] = "LAIRD BL652"  # Used by loader 3 or higher
        self.param['usbvendorstring'] = u"ra.leckasemmel.de"
        self.param['usbproductstring'] = u"Sondengott Ra"

        return

    def getBlob(self):
        b = bytearray(1024)
        struct.pack_into('hh', b, 0,
            int(self.param['version']),
            int(self.param['serialnumber']))

        struct.pack_into('hhh', b, 4,
            int(self.param['usbvid'], 16),
            int(self.param['usbpid'], 16),
            int(self.param['usbversion'], 16))

        struct.pack_into('fff', b, 12,
            float(self.param['referencefrequency']),
            float(self.param['rssicorrectionlnaon']),
            float(self.param['rssicorrectionlnaoff']))

        # Fill reserved float's with NAN
        for n in range(25):
            struct.pack_into('f', b, 24+4*n, math.nan)

        struct.pack_into('i', b, 124,
            self.param['baudrate'])

        name = self.param['namebluetooth'].encode('utf-8')
        b[128:128+len(name)] = name

        wchar = self.param['usbvendorstring'].encode('utf-16-le')
        if (len(wchar) > 64):
            print("Zu lang: ", wchar)
        else:
            b[176:176+len(wchar)] = wchar
        wchar = self.param['usbproductstring'].encode('utf-16-le')
        b[304:304+len(wchar)] = wchar

        # Calculate CRC
        crc32_func = crcmod.mkCrcFun(0x104c11db7, rev=False, initCrc=0xFFFFFFFF, xorOut=0)
        crc = crc32_func(b[0:1020])
        struct.pack_into('I', b, 1020, crc)

        return b


if __name__ == "__main__":

    # Install Ctrl-C handler
    signal.signal(signal.SIGINT, sigint_handler)

    parser = argparse.ArgumentParser(description = 'Ra configuration file generator')
    parser.add_argument('--test', help='XXX', action='store_true')
    args = parser.parse_args()

    cp = configparser.ConfigParser()
    cp.read('config.ini')

    # Generate one config file per section in config.ini
    for ra in cp.sections():
        # Create binary blob and fill with defaults
        conf = ConfigBlob(ra)

        # Overwrite with settings from DEFAULT config file section
        for key in cp['DEFAULT']:
            conf.param[key] = cp['DEFAULT'][key]

        # Overwrite with settings from device specific config file section
        for key in cp[ra]:
            conf.param[key] = cp[ra][key]

        basefilename = "conf_{:d}".format(int(ra))
        with open(basefilename + ".bin", "wb") as blobfile:
            blobfile.write(conf.getBlob())
            blobfile.close()


