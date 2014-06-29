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
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
import os.path
import re

pkg_name = 'adtm'
pkg = {}
with open(os.path.join(pkg_name,'_info.py')) as f: exec(f.read(),pkg,pkg)

reimg = re.compile("^!\[(?P<label>[^\]]*)\]\((?P<src>[^\)]*)\)$")
relink = re.compile("\[(?P<label>[^\]]*)\]\((?P<href>[^\)]*)\)")
reimglink = re.compile(
"^\[!\[(?P<label>[^\]]*)\]\((?P<src>[^\)]*)\)\]\((?P<href>[^\)]*)\)$")

def read(fname):
    """Read Markdown File And Convert to reST"""
    imgindex = 0
    lines = ""
    for line in open(os.path.join(os.path.dirname(__file__), fname),'rt'):
        m = reimg.match(line)
        if m is not None:
            g = m.groupdict()
            if g['label'] is None:
                g['label'] = 'image' + imgindex
                imgindex += 1
            lines = "|{label:s}|\n\n.. |{label:s}| image:: {src:s}\n".format(
                        **g)
            continue
        m = reimglink.match(line)
        if m is not None:
            g = m.groupdict()
            if g['label'] is None:
                g['label'] = 'image' + imgindex
                imgindex += 1
            lines += "|{label:s}|\n\n.. |{label:s}| image:: {src:s}\n"\
                "   :target: {href:s}".format(**g)
            continue
        if line[0:5] == "Note:":
            line = ".. Note::" + line[5:]
        line = relink.sub('`\g<label> <\g<href>>`_',line)
        lines += line
    return lines

def readlist(fname):
    return open(os.path.join(
        os.path.dirname(__file__),
        fname),'rt').read().split('\n')

if '__appname__' in pkg:
    console_scripts = [pkg['__appname__'] + '=' + pkg_name + ".console:run"]
else:
    console_scripts = None

entry_points = {}
if console_scripts is not None:
    entry_points['console_script'] = console_scripts

print entry_points

setup(
    name=pkg['__title__'],
    version=pkg['__version__'],
    author=pkg['__authors__'][0][0],
    author_email=pkg['__authors__'][0][1],
    license=pkg['__license__'],
    description=pkg['__desc__'],
    packages=find_packages(),
    url='https://github.com/alphaomega-technology/' + pkg['__title__'],
    long_description=read('README.md'),
    install_requires=readlist('requires.txt'),
    entry_points=entry_points,
    classifiers=readlist('caterogies.txt'),
    zip_safe=False,
    test_suite='tests',
)
