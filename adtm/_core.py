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

import numbers
import base64
import sys
import collections
import string
import re
import types


class AdtmError(Exception):
    def __init__(self, msg, value=None, adtm=None):
        self.msg = msg
        self.value = value
        self.adtm = adtm

    def __str__(self):
        msg = self.msg
        if self.adtm is not None:
            msg += "\n  Near: {0:s}".format(self.adtm)
        if self.value is not None:
            msg += "\n  Value: {0:s}".format(self.value)
        return msg

_rowsep = re.compile("[,;|:]")
