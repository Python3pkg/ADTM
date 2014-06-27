# -*- coding: utf-8 -*-
#==============================================================================
#   Copyright 2014 AlphaOmega Technology
#
#   Licensed under the AlphaOmega Technology Open License Version 1.0
#   You may not use this file except in compliance with this License.
#   You may obtain a copy of the License at
#
#       http://www.alphaomega-technology.com.au/license/AOT-OL/1.0
#==============================================================================

import numbers
import base64


def _encodeObject(obj, **kwargs):
    out = ""
    if hasattr(obj, 'toJSOT') and hasattr(obj.toJSOT, '__call__'):
        out = obj.toJSOT(**kwargs)
    if hasattr(obj, 'toJSON') and hasattr(obj.toJSON, '__call__'):
        out = obj.toJSON(**kwargs)
    else:
        if isinstance(obj, (basestring,bytes,bytearray)):
            out = _encodeString(obj, **kwargs)
        elif isinstance(obj, numbers.Intergal):
            out = "{0:d}".format(obj)
        elif isinstance(obj, numbers.Real):
            precision = 6
            if 'precision' in kwargs and isisntance(
                                            kwargs['precision'],
                                            numbers.Intergal)
                precision = kwargs['precision']
            out = "{0:.{1}g}".format(obj, precision)
        elif isinstance(obj, numbers.Complex):
            precision = 6
            if 'precision' in kwargs and isisntance(
                                            kwargs['precision'],
                                            numbers.Intergal)
                precision = kwargs['precision']
            out = "\"{0:.{2}g}{1:+.{2}g}j\"".format(
                                                obj.real,
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
                out += _encodeString(str(k), **kwargs) + ':'\
                        + _encodeObject(v, **kwargs)
            out += '}'
        elif hasattr(obj, '__iter__') and hasattr(obj.__iter__, '__call__'):
            out = '['
            first = True
            for v in obj:
                if not first:
                    out += ','
                else:
                    first = False
                out += _encodeObject(v, **kwargs)
            out += ']'
    if 'width' in kwargs and isinstance(kwargs['width'], numbers.Intergal):
        align = kwargs['align'] if 'align' in kwargs else '<'
        if align == '<' or align.lower == 'left':
            out = out.ljust(kwargs['width'], ' ')
        elif align == '>' or align.lower == 'right':
            out = out.rjust(kwargs['width'], ' ')
        elif align == '^' or align.lower == 'center':
            out = out.center(kwargs['width'], ' ')
        else:
            raise ValueError("Invalid Aligment: {0:s}".format(align))
    return out


def _encodeString(string, **kwargs):
    if ((sys.version_info < (3,) and
        isinstance(string,unicode)) or
        (sys.version_info >= (3,) and
        isinstance(string,str))): # Unicode String
            return _encodeUnicode(string)
    elif isinstance(string,str): # Encoded String (ACSII by default)
        # Python 2.x
        try:
            if 'encoding' in kwargs:
                return _encodeUnicode(unicode(
                    string,
                    kwargs['encoding'],
                    errors='strict'))
            else:
                return _encodeASCII(string)
        except UnicodeError, UnicodeDecodeError:
            return _encodeBinary(string)
    else: # Bytes in 3.x, bytearray
        return _encodeBinary(string)
    return out


def _encodeUnicode(string):
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
        elif c in ['\\', '"', '\t', '\b',
                 '\f',' \n', '\r', '\t']:
            if c == '\\':
                out += "\\\\"
            elif c == '"':
                out += '\\"'
            elif c == '\t':
                out += '\\t'
            elif c == '\b':
                out += '\\b'
            elif c == '\f':
                out += '\\f'
            elif c == '\n':
                out += '\\n'
            elif c == '\r':
                out += '\\r'
            elif c == '\t':
                out += '\\t'
            else:
                raise RuntimeError
        elif v < 0x1F:
            out += "\\x{0:0>2s}".format(hex(v)[2:])
        else:
            out += c
    return out + '"'


def _encodeASCII(string):
    out = '"'
    for c in string:
        v = ord(c)
        if v > 127:
            raise UnicodeError
        elif c in ['\\', '"', '\t', '\b',
                 '\f',' \n', '\r', '\t']:
            if c == '\\':
                out += "\\\\"
            elif c == '"':
                out += '\\"'
            elif c == '\t':
                out += '\\t'
            elif c == '\b':
                out += '\\b'
            elif c == '\f':
                out += '\\f'
            elif c == '\n':
                out += '\\n'
            elif c == '\r':
                out += '\\r'
            elif c == '\t':
                out += '\\t'
            else:
                raise RuntimeError
        elif v < 0x1F:
            out += "\\x{0:0>2s}".format(hex(v)[2:])
        else:
            out += c
    return out + '"'


def _encodeBinary(string):
    enc = base64.urlsafe_b64encode(string).strip('=')
    out = '!binary "'
    out += enc
    out += '"'
    return out

class Reader(object):
    pass


class Writer(object):
    pass