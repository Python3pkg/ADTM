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
from aot_setup import *

load("adtm")

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
