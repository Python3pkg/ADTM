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


def _encodeObject(obj, **kwargs):
    out = ""
    if hasattr(obj, 'toJSON') and hasattr(obj.toJSON, '__call__'):
        out = obj.toJSON(**kwargs)
    else:
        if isinstance(obj, basestring):
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
        isinstance(string,str)): # Unicode String
            return _encodeUnicode
    elif isinstance(string,str): # Encoded String (ACSII by default)
        if 'encoding' in kwargs:
            return _encodeUnicode(unicode(
                string,
                kwargs['encoding'],
                errors='strict'))
        else:
            return _encodeASCII(string)
    return out


def _encodeUnicode(string):
    out = '"'
    for c in string:
        v = ord(c)
        if v > 127:
            out += "\\u{0:0>4s}".format(hex(ord(c))[2:])
        else:
            if c in ['\\', '"', '\t', '\b',
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
            else:
                out += c
    return out + '"'


def _encodeASCII(string):
    out = '"'
    for c in string:
        v = ord(c)
        if v > 127:
            raise UnicodeError
        if c in ['\\', '"', '\t', '\b',
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
        else:
            out += c
    return out + '"'


class Reader(object):
    pass


class Writer(object):
    pass