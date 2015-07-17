======
HTTP 1
======

HTTP1 is a wrapper around httplib to perform HTTP requests in a single call. For instance, to get PyPI index of packages, you might write::

    import http1
    
    print http1.request('http://pypi.python.org/simple/').body

request() method
================

This method performs an HTTP request. The signature of the request method is the following::

    request(url, params={}, method='GET', body=None, headers={},
            content_type=None, content_length=True, username=None,
            password=None, capitalize_headers=True,
            follow_redirect=True, max_redirect=3)

The parameters are the following:

- url: the URL call, including protocol and parameters (such as 'http://www.google.com?foo=1&bar=2').
- params: URL parameters as a map, so that {'foo': 1, 'bar': 2} will result in an URL ending with '?foo=1&bar=2'.
- method: the HTTP method (such as 'GET' or 'POST'). Defaults to 'GET'.
- body: the body of the request as a string. Defaults to None.
- headers: request headers as a dictionnary. Defaults to '{}'.
- content_type: the content type header of the request. Defauls to None.
- content_length: tells if we should add content length headers to the request. Defaults to true.
- username: username while performing basic authentication, must be set with password.
- password: password while performing basic authentication, must be set with username.
- capitalize_headers: tells if headers should be capitalized (so that their names are all like 'Content-Type' for instance).
- follow_redirect: tells if http1 should follow redirections (status codes 3xx). Defaults to *True*.
- max_redirect: maximum number of redirections to follow. If there are too many redirects, a TooManyRedirectsException is raised. Defaults to *3*.

This method returns the response as a Response object described hereafter.

May raise a *TooManyRedirectsException*.

*NOTE*: to call HTTPS URLs, Python must have been built with SSL support.

There are dedicated functions for HTTP methods (*GET*, *HEAD*, *POST*, *PUT*, *DELETE*, *CONNECT*, *OPTIONS* and *TRACE*). Thus, to perform a head call for instance, you may write::

  response = http1.head('http://www.example.com')

Which is the same as::

  response = http1.request('http://www.example.com', method='HEAD')

Response object
===============

This object encapsulates status code (200, 404, as an integer), message (such as 'OK', 'Not Found', as a string), headers (as a dictionnary), and body (as a string).

TooManyRedirectsException
=========================

This exception is thrown when there have been too many redirects (that is a number of refirects greater than *max_redirect*).

Enjoy!

