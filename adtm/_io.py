# -*- coding: utf-8 -*-
#==============================================================================
#   Copyright 2015 AlphaOmega Technology
#
#   Licensed under the AlphaOmega Technology Open License Version 1.0
#   You may not use this file except in compliance with this License.
#   You may obtain a copy of the License at
#
#       http://www.alphaomega-technology.com.au/license/AOT-OL/1.0
#==============================================================================
"""
IO classes
"""

from adtm._core import AdtmError

from adtm._read import DecodeObject

from adtm._write import EncodeObject

import string

from itertools import izip_longest


class Reader(object):
    """
    ADTM Reader, reads from a file object
    """
    def __init__(self, adtmfile):
        self.file = adtmfile
        self.decode = DecodeObject()

    def readrow(self):
        """
        Read row from file
        """
        line = self.file.readline()
        values = []
        s = 0
        while s < len(line):
            self.decode.offset = s
            val, offset = self.decode(line[s:])
            values.append(val)
            s += offset
        return values


class Writer(object):
    """
    ADTM Writer, writes to a file object
    """
    def __init__(self, adtmfile):
        self.file = adtmfile
        self.default_sep = ','
        self.col_width = []
        self.has_header = False
        self.multiheader = False
        self.tables = []
        self.offset = 0
        self.last_seprow = 0
        self.last_headerrow = 0
        self.is_table = False
        self.headers = []
        self.encode = EncodeObject()

    def begintable(self, name, headers, width, meta=[], sep='|'):
        """
        Begin a new table or sheet in the file.
        """
        if self.has_header and not self.multiheader:
            raise AdtmError('File header dosen\'t support tables')
        if name in self.tables:
            raise AdtmError('Table "{0:s}" all ready '
                            'exists in file'.format(name))
        if sep not in [',', ';', '|', ':']:
            raise AdtmError('Invalid Row Value Seperator ("{0:s}") provided, '
                            'must be ( "," | ";" | "|" | ":" )'.format(sep))
        self.file.write(self.encode.write_header(name, True, len(meta)) + '\n')
        self.has_header = True
        self.multiheader = True
        self.tables.append(name)
        self.default_sep = sep
        self.col_width = width
        for row in meta:
            self.writemetarow(row)
        self.writerow(headers)
        self.offset = 0
        self.last_seprow = 0
        self.last_headerrow = 0
        self.is_table = True
        self.headers = headers

    def writemetarow(self, row, *args, **kwargs):
        """
        Write Meta Data row to file, expects a list of tuples
        """
        if not self.has_header:  # Write basic header for raw data
            self.file.write(self.encode.write_header() + '\n')
            self.has_header = True
        self.file.write('; '.join((self.encode.encode_meta(i) for i in row))
                        + "\n")

    def writerow(self, row, sep=None, *args, **kwargs):
        """
        Write General Data row to file
        """
        if not self.has_header:  # Write basic header for raw data
            self.file.write(self.encode.write_header() + '\n')
            self.has_header = True
        if sep is None:
            sep = self.default_sep
        if sep not in [',', ';', '|', ':']:
            raise AdtmError('Invalid Row Value Seperator ("{0:s}") provided, '
                            'must be ( "," | ";" | "|" | ":" )'.format(sep))
        self.offset += 1
        if self.offset - self.last_headerrow == 5*5:
            self.file.write("#" + sep.join((string.center(h, w) for h, w in
                                            izip_longest(self.headers,
                                                         self.col_width,
                                                         fillvalue=0)))[1:]
                            + "\n")
            self.last_headerrow = self.offset
            self.last_seprow = self.offset
            self.offset += 1
        elif self.offset - self.last_seprow == 5:
            self.file.write("#" + sep.join((string.center(" ", w) for w in
                                            self.col_width))[1:]
                            + "\n")
            self.last_seprow = self.offset
            self.offset += 1
        self.file.write(sep.join((string.center(self.encode(i), w) for i, w in
                                  izip_longest(row,
                                               self.col_width,
                                               fillvalue=0)))
                        + "\n")
