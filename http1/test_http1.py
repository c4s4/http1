#!/usr/bin/env python
# encoding=UTF-8

#pylint: disable=W0403
import http1
import unittest

class Test(unittest.TestCase):

    def test_get_ok(self):
        response = http1.request('http://sweetohm.net')
        self.assertEquals(200, response.status)
        self.assertEquals('OK', response.message)
        self.assertTrue('Sweetohm' in response.body)

    def test_status_ko(self):
        response = http1.request('http://sweetohm.net/toto')
        self.assertEquals(404, response.status)
        self.assertEquals('Not Found', response.message)

    def test_get_https_ok(self):
        try:
            headers = {'Accept-Language': 'fr'}
            response = http1.request('https://www.google.fr',
                                     headers=headers)
            self.assertEquals(200, response.status)
            self.assertEquals('OK', response.message)
            self.assertTrue('<title>Google</title>' in response.body)
        except AttributeError:
            # if Python was not built with SSL support
            pass

    def test_redirect(self):
        response = http1.request('http://sweetohm.net/blog/index.html')
        expected = 200
        actual = response.status
        self.assertEqual(expected, actual)
        self.assertTrue('Sweetohm' in response.body)
        response = http1.request('http://sweetohm.net/arc/python-dbapi.pdf',
                                 follow_redirect=False)
        expected = 301
        actual = response.status
        self.assertEqual(expected, actual)
        try:
            http1.request('http://cafebabe.free.fr',
                          max_redirect=0)
        except http1.TooManyRedirectsException:
            pass

    def test_methods(self):
        response = http1.get('http://www.sweetohm.net')
        self.assertEqual(200,response.status)
        self.assertTrue('Sweetohm' in response.body)
        response = http1.head('http://sweetohm.net/arc/python-dbapi.pdf',
                              follow_redirect=False)
        self.assertEqual(301, response.status)
        self.assertEqual('http://sweetohm.net/pdf/python-dbapi.pdf',
                         response.headers['Location'])

    def test_relative_redirect(self):
        response = http1.get('http://httpbin.org/redirect/2')
        self.assertEqual(200, response.status)


# Run unit tests when started on command line
if __name__ == '__main__':
    unittest.main()

