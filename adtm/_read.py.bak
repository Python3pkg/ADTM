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

import re
from adtm._core import AdtmError

_sep = [re.compile(r"(?:[,;|:]|$)"),
        re.compile(r"(?:[,;]|(?=\]))"),
        re.compile(r"(?:[,;]|(?=\}))")]

_T0 = "\s*(?:[,;|:]|$)"
_T1 = "\s*(?:[,;]|(?=\]))"  #  (?=\]) is end of list
_T2 = "\s*(?:[,;]|(?=\}))"  #  (?=\}) is end of dict
_T3 = "\s*(?:[,;]|(?=\)))"  #  (?=\) is end of arglist
_T4 = "\s*[:]"  #  Dict key seperator

ROW_LEVEL = 0
LIST_LEVEL = 1
DICT_LEVEL = 2
KEY_LEVEL = 4
ARGLIST_LEVEL = 3

# SpecialValue = BoolValue | NoneValue | SpecialNumber ;
# BoolValue = (* Case Insenstive *) ( "true" | "yes" | "on" | "false" |
#                                     "no" | "off" ) ;
# NoneValue = (* Case Insenstive *) ( "none" | "null" ) ;
# SpecialNumber = (* Case Insenstive *) ( "nan" | "inf" | "infinity" | "-inf" |
#                                        "-infinity" | "+inf" | "+infinity" ) ;
_pspvalue = r"""(?ix)^\s*(?:                      # Start of String
                (true|yes|on)|                    # True
                (false|no|off)|                   # False
                (none|null)|                      # None
                (nan)|                            # Not A Number
                (infinity|inf|\+infinity|\+inf)|  # Postive Infinity
                (-infinity|-inf)                  # Negative Infinity
                )"""
_spvalue = [re.compile(_pspvalue + _T0),
            re.compile(_pspvalue + _T1),
            re.compile(_pspvalue + _T2),
            re.compile(_pspvalue + _T3)]
_spresult = (True, False, None, float('nan'), float('+inf'), float('-inf'))

# UnquotedString = ( SafeCharacter, { '.' | '-' | '0'..'9' | SafeCharacter } )
#                  - SpecialValue ;
# SafeCharacter = '\' | '/' | '_' | 'a'..'f' | 'A'..'F' ;
_puqstring = r"([/\\_a-zA-Z][/\\_a-zA-Z0-9.-]*)"
_uqstring = [re.compile(r"^\s*" + _puqstring + _T0),
             re.compile(r"^\s*" + _puqstring + _T1),
             re.compile(r"^\s*" + _puqstring + _T2),
             re.compile(r"^\s*" + _puqstring + _T3),
             re.compile(r"^\s*" + _puqstring + _T4)]

_pqstring = r'^\s*"([^"\\]*(?:\\.[^"\\]*)*)"'
_qstring = [re.compile(_pqstring + _T0),
            re.compile(_pqstring + _T1),
            re.compile(_pqstring + _T2),
            re.compile(_pqstring + _T3),
            re.compile(_pqstring + _T4)]

# Integral = [ "-" | "+" ], { "0".."9" }+ ;
_pintergal = r"^\s*([+-]?\d+)"
_intergal = [re.compile(_pintergal + _T0),
             re.compile(_pintergal + _T1),
             re.compile(_pintergal + _T2),
             re.compile(_pintergal + _T3)]

# Real = [ "-" | "+" ], ( ( { "0".."9" }+, ".", { "0".."9" } ) |
#                         ( ".", { "0".."9" }+ ) ), [ Exponent ] ;
# Exponent = ( "e" | "E" ), [ "-" | "+" ], { "0".."9" }+ ;
_pexpoent = r"[eE]([+-]?\d+)"
_pfloat = r"(?:\d+(?=[eEij])|\d+\.\d*|\.\d+)"
_preal = "\s*(([+-]?" + _pfloat + ")(?:" + _pexpoent + ")?)"
_real = [re.compile(r"^" + _preal + _T0),
         re.compile(r"^" + _preal + _T1),
         re.compile(r"^" + _preal + _T2),
         re.compile(r"^" + _preal + _T3)]

# Complex = [ Real ],
#           ( Real (* MUST have sign if **OPTIONAL** real, is used *) ),
#           ( "i" | "j" ) ;
_pcomplex = r"^\s*(?:" + _preal + "(?=\s*[+-]))?" + _preal + "\s*[ij]"
_complex = [re.compile(_pcomplex + _T0),
            re.compile(_pcomplex + _T1),
            re.compile(_pcomplex + _T2),
            re.compile(_pcomplex + _T3)]

_liststart = re.compile(r"^\s*\[")

_dictstart = re.compile(r"^\s*\{")

_argliststart = re.compile(r"^\s*\(")

_tag = re.compile(r"^\s*!" + _puqstring)

class AdtmReaderError(AdtmError):
    def __init__(self, line=0, offset=0, *args, **kwargs):
        super(AdtmReaderError, self).__init__(*args, **kwargs)
        self.line = line
        self.offset = offset

    def __str__(self):
        msg = super(AdtmReaderError,self).__str__()
        msg += "\n  Line {0:d}, character {1:d}".format(self.line, self.offset)
        return msg


class AdtmTagError(AdtmReaderError):
    """
    Special Error for invalid tags, contains tag name and args
    """
    def __init__(self, tag, tagargs, *args, **kwargs):
        from _write import EncodeObject
        enc = EncodeObject()
        eargs = (enc(arg) for arg in tagargs)
        kwargs['value'] = "!{0:s}({1:s})".format(tag, ', '.join(eargs))
        super(AdtmTagError, self).__init__(*args, **kwargs)
        self.tag = tag
        self.tagargs = tagargs

class NotBasicValue(Exception):
    pass


class _StringTester(object):
    def __init__(self, string):
        self.str = string
        self.match = None

    def test(self, regex):
        self.match = regex.match(self.str)
        return bool(self.match)

    def groups(self):
        if self.match is None:
            raise RuntimeError("Run test() First")
        return self.match.groups()

    def group(self, i):
        if self.match is None:
            raise RuntimeError("Run test() First")
        return self.match.group(i)

    def end(self):
        if self.match is None:
            raise RuntimeError("Run test() First")
        return self.match.end()


class DecodeObject(object):
    """
    Object Encoding into ADTM format objects
    """
    def __init__(self):
        self.state = {}
        self.line = 0
        self.offset = 0

    def Error(self, offset, msg, **kwarg):
        return AdtmReaderError(self.line, self.offset + offset, msg, **kwarg)

    def __call__(self, string, levels=None, **kwargs):
        if levels is None:
            levels = [0]
        try:
            val, end = self._basic_value(string, levels)
        except NotBasicValue:
            end = 0
            tester = _StringTester(string)
            if tester.test(_tag):
                tag = tester.group(1)
                s = tester.end()
                val, offset = self._tag(tag, string[s:], levels)
                end = s + offset
            else:
                m = _sep[levels[-1]].search(string)
                e = len(string)
                if m is not None:
                    e = m.end()
                raise self.Error(0, "Unknown Value", value=string[:e])
        return val, end

    def _basic_value(self, string, levels):
        end = 0
        tester = _StringTester(string)
        if tester.test(_spvalue[levels[-1]]):
            val = _spresult[[bool(x) for x in tester.groups()].index(True)]
            end = tester.end()
        elif tester.test(_qstring[levels[-1]]):
            val = self._parse_string(tester.group(1))
            end = tester.end()
        elif tester.test(_uqstring[levels[-1]]):
            val = tester.group(1)
            end = tester.end()
        elif tester.test(_intergal[levels[-1]]):
            val = int(tester.group(1))
            end = tester.end()
        elif tester.test(_real[levels[-1]]):
            val = float(tester.group(1))
            end = tester.end()
        elif tester.test(_complex[levels[-1]]):
            real = tester.group(1)
            if real is None:
                real = 0
            imag = tester.group(4)
            if imag is None:
                imag = 0
            val = complex(float(real), float(imag))
            end = tester.end()
        elif tester.test(_liststart):
            # List = "[", { Value / ( "," | ";" ) }, "]" ;
            s = tester.end()
            val = []
            levels.append(LIST_LEVEL)  # 1 means List
            while string[s] is not ']':
                # Value / ( "," | ";" )
                value, offset = self(string[s:], levels)
                val.append(value)
                s += offset
            s += 1  # Teriminator
            levels.pop()
            # Match Seperator
            m = _sep[levels[-1]].search(string[s:])
            end = s + m.end()
        elif tester.test(_dictstart):
            # Dictionary = "{", { String, ":", Value / ( "," | ";" ) }, "}" ;
            s = tester.end()
            val = {}
            levels.append(DICT_LEVEL)  # 2 means Dict
            while string[s] is not '}':
                # String, ":", Value / ( "," | ";" )
                # key = fetch string, delimited by ":"
                keytester = _StringTester(string[s:])
                offset = 0
                if keytester.test(_uqstring[KEY_LEVEL]):  # Dict Key Sep
                    key = keytester.group(1)
                    offset = keytester.end()
                s += offset
                if key is None:
                    raise self.Error(s, "Invalid Key",
                                     adtm=string[min(0, s-5):10])
                if key in val:
                    raise self.Error(s, "Dictionary has dupliate keys",
                                     value=key)
                value, offset = self(string[s:], levels)
                val[key] = value
                s += offset
            s += 1  # Teriminator
            levels.pop()
            # Match Seperator
            m = _sep[levels[-1]].search(string[s:])
            end = s + m.end()
        else:
            raise NotBasicValue()
        return val, end

    def _tag(self, tag, string, levels):
        try:
            arg, end = self._basic_value(string, levels)
            val = self._handle_tag(tag, arg)
        except NotBasicValue:
            end = 0
            tester = _StringTester(string)
            if tester.test(_argliststart):
                # "(", { Value / ( "," | ";" ) }, ")" ;
                s = tester.end()
                args = []
                levels.append(ARGLIST_LEVEL)  # 1 means List
                while string[s] is not ')':
                    # Value / ( "," | ";" )
                    value, offset = self(string[s:], levels)
                    args.append(value)
                    s += offset
                s += 1  # Teriminator
                levels.pop()
                # Match Seperator
                m = _sep[levels[-1]].search(string[s:])
                end = s + m.end()
                val = self._handle_tag(tag, *args)
            else:
                m = _sep[levels[-1]].search(string)
                e = len(string)
                if m is not None:
                    e = m.end()
                raise self.Error(0, "Unknown Value", value=string[:e])
        return val, end

    def _handle_tag(self, tag, *args):
        val = None
        if (tag.lower() == 'binary'):
            val = self._tag_binary(*args)
        else:
            raise AdtmTagError(tag,
                               args,
                               self.line,
                               self.offset,
                               "Unknown Tag")
        return val

    def _tag_binary(self, *args):
        import base64
        if len(args) != 1 or not isinstance(args[0], basestring):
            raise AdtmTagError('binary',
                               args,
                               self.line,
                               self.offset,
                               "Invalid Argruments, expects 1 string")
        enc = args[0].strip('=')
        enc += '=' * (-len(enc) % 4)
        return base64.urlsafe_b64decode(enc)

    def _parse_string(self, string):
        return string
