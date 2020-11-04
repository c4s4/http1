#!/usr/bin/env python
# encoding: UTF-8

from distutils.core import setup

setup(
    name = 'http1',
    version = '0.0.0',
    author = 'Michel Casabianca',
    author_email = 'casa@sweetohm.net',
    packages = ['http1'],
    url = 'https://github.com/c4s4/http1',
    license = 'Apache Software License',
    description = 'http1 is an API to perform HTTP requests in a single call',
    long_description=open('README.rst', encoding='UTF-8').read(),
)
