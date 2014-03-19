#!/usr/bin/env python
# encoding=UTF-8

import os
import sys
import inspect
test_dir = os.path.dirname(inspect.currentframe().f_code.co_filename)
src_dir = os.path.join(test_dir, '..', '..')
sys.path.insert(0, src_dir)
import http1
import unittest

class Test(unittest.TestCase):

    def test_get_ok(self):
        headers = {'Accept-Language': 'fr'}
        response = http1.request('http://www.google.com', headers=headers)
        self.assertEquals(302, response.status)
        self.assertEquals('Found', response.message)
        location = response.headers['Location']
        response = http1.request(location)
        self.assertEquals(200, response.status)
        self.assertEquals('OK', response.message)
        self.assertTrue('<title>Google</title>' in response.body)

    def test_get_found(self):
        response = http1.request('http://www.google.com')
        self.assertEquals(302, response.status)
        self.assertEquals('Found', response.message)

    def test_get_nohttp(self):
        response = http1.request('lttp://www.google.com')
        self.assertEquals(302, response.status)
        self.assertEquals('Found', response.message)

    def test_get_https_ok(self):
        try:
            headers = {'Accept-Language': 'fr'}
            response = http1.request('https://www.google.com',
                                     headers=headers)
            self.assertEquals(302, response.status)
            self.assertEquals('Found', response.message)
            location = response.headers['Location']
            response = http1.request(location)
            self.assertEquals(200, response.status)
            self.assertEquals('OK', response.message)
            self.assertTrue('<title>Google</title>' in response.body)
        except AttributeError:
            # if Python was not built with SSL support
            pass

# Run unit tests when started on command line
if __name__ == '__main__':
    unittest.main()

