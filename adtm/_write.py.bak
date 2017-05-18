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
Low Level Output Encoding
"""

import numbers
import base64
import sys
import collections
import types

from adtm._core import AdtmError

_adtm_dumper = {
}


class EncodeObject(object):
    """
    Object Encoding into ADTM format objects
    """
    def __init__(self):
        self.state = {}

    def set_state(self, **kwargs):
        """
        Set Encoding State
        """
        self.state = kwargs

    def clear_state(self):
        """
        Clear Encoding State, Reset to Default
        """
        self.state = {}

    def __call__(self, obj, fmt=None):
        """
        Encode an Object
        """
        out = ""
        if fmt is None:
            fmt = {}
        if isinstance(obj, tuple(_adtm_dumper.keys())):
            if type(obj) is not types.InstanceType:  # New style inspect mro
                mro = obj.__class__.__mro__
                for adtmtype in mro:
                    if adtmtype in _adtm_dumper.keys():
                        break
            else:  # old style class, only check __class__
                adtmtype = obj.__class__
            out = "!" + _adtm_dumper[adtmtype][0] + " "
            out += _adtm_dumper[adtmtype][1](self, obj)
        elif isinstance(obj, (basestring, bytes, bytearray)):
            out = self._encode_string(obj)
        elif isinstance(obj, numbers.Integral):
            out = "{0:d}".format(obj)
        elif isinstance(obj, numbers.Real):
            precision = 6
            if 'precision' in fmt and isinstance(fmt['precision'],
                                                 numbers.Integral):
                precision = fmt['precision']
            out = "{0:.{1}g}".format(obj, precision)
        elif isinstance(obj, numbers.Complex):
            precision = 6
            if 'precision' in fmt and isinstance(fmt['precision'],
                                                 numbers.Integral):
                precision = fmt['precision']
            out = "{0:.{2}g}{1:+.{2}g}j".format(obj.real,
                                                obj.imag,
                                                precision)
        elif hasattr(obj, 'items') and hasattr(obj.items, '__call__'):
            out = '{'
            first = True
            for k, v in obj.items():
                if not first:
                    out += ','
                else:
                    first = False
                out += self._encode_string(str(k)) + ':'\
                    + self(v)
            out += '}'
        elif hasattr(obj, '__iter__') and hasattr(obj.__iter__, '__call__'):
            out = '['
            first = True
            for v in obj:
                if not first:
                    out += ','
                else:
                    first = False
                out += self(v)
            out += ']'
        if 'width' in fmt and isinstance(fmt['width'], numbers.Integral):
            align = fmt['align'] if 'align' in fmt else '^'
            if align == '<' or align.lower == 'left':
                out = out.ljust(fmt['width'], ' ')
            elif align == '>' or align.lower == 'right':
                out = out.rjust(fmt['width'], ' ')
            elif align == '^' or align.lower == 'center':
                out = out.center(fmt['width'], ' ')
            else:
                raise AdtmError("Invalid Aligment: {0:s}".format(align))
        return out

    def _encode_string(self, string):
        if ((sys.version_info < (3,) and
             isinstance(string, unicode)) or
            (sys.version_info >= (3,) and
             isinstance(string, str))):  # Unicode String
            return self._encode_unicode(string)
        elif isinstance(string, str):  # Encoded String (ACSII by default)
            # Python 2.x
            try:
                if 'encoding' in self.state:
                    return self._encode_unicode(unicode(
                        string,
                        self.state['encoding'],
                        errors='strict'))
                else:
                    return self._encode_ascii(string)
            except (UnicodeError, UnicodeDecodeError):
                return self._encode_binary(string)
        else:  # Bytes in 3.x, bytearray
            return self._encode_binary(string)

    _string_escape = {'\\': "\\\\", '"': '\\"',
                      '\t': '\\t', '\b': '\\b',
                      '\f': '\\f', '\n': '\\n',
                      '\r': '\\r'}

    def _encode_unicode(self, string):
        """
        Encode Unicode String
        """
        out = '"'
        for c in string:
            v = ord(c)
            if v > 127:
                U = hex(v)[2:]
                if len(U) < 3:
                    out += "\\x{0:0>2s}".format(U)
                elif len(U) < 5:
                    out += "\\u{0:0>4s}".format(U)
                else:
                    out += "\\U{0:0>8s}".format(U)
            elif c in self._string_escape.keys():
                out += self._string_escape[c]
            elif v < 0x1F:
                out += "\\x{0:0>2s}".format(hex(v)[2:])
            else:
                out += c
        return out + '"'

    def _encode_ascii(self, string):
        """
        Encode ASCII String
        """
        out = ''
        force_quote = False
        for c in string:
            v = ord(c)
            if v > 127:
                raise UnicodeError
            elif c in self._string_escape.keys():
                out += self._string_escape[c]
            elif v < 0x1F:
                out += "\\x{0:0>2s}".format(hex(v)[2:])
            else:
                out += c
        quote = True
        if (not force_quote and
           'use_unquoted' in self.state and self.state['use_unquoted']):
            from adtm._read import _uqstring
            if _uqstring.match(out):
                quote = False
                out = out.strip()
        if quote:
            out = '"' + out + '"'
        return out

    def _encode_binary(self, string):
        """
        Encode Binary String
        """
        enc = base64.urlsafe_b64encode(string).strip('=')
        quote = True
        if 'use_unquoted' in self.state and self.state['use_unquoted']:
            from adtm._read import _uqstring
            if _uqstring.match(enc):
                quote = False
                enc = enc.strip()
        if quote:
            enc = '"' + enc + '"'
        return '!binary ' + enc

    def write_header(self,
                     name=None,
                     header=False,
                     offset=0,
                     typed=False,
                     version=1.0,
                     ext=None):
        """
        Write Header Line
        """
        fields = collections.OrderedDict()
        if version is not None:
            fields['version'] = version
        fields['header'] = header
        fields['typed'] = typed
        if offset > 0:
            fields['offset'] = offset
        if name is not None:
            fields['name'] = name
        if ext is not None and isinstance(ext, collections.Mapping):
            for k, v in ext.items():
                if k not in fields and '/' in k:
                    fields[k] = v
        out = '='
        first = True
        for k, v in fields.items():
            if not first:
                out += ';'
            else:
                first = False
            out += self._encode_string(str(k)) + ':'\
                + self(v)
        return out

    def encode_meta(self, item):
        """
        Encode Meta Item
        """
        out = ""
        if isinstance(item, tuple) and len(item) > 1:
            if isinstance(item[0], (basestring, bytes, bytearray)):
                out = self._encode_string(item[0])
                out += ": "
                out += ', '.join((self(i) for i in item[1:]))
            else:
                raise AdtmError("Meta tuples must have a string "
                                "type first element")
        else:
            raise AdtmError("Meta items must be tuples of length 2 or more")
        return out
