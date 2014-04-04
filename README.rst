======
HTTP 1
======

HTTP1 is a wrapper around httplib to perform HTTP requests in a single call.
For instance, to get PyPI index of packages, you might write::

    import http1
    
    print http1.request('http://pypi.python.org/simple/').body

request() method
================

This method performs an HTTP request. The signature of the request method is
the following::

    request(url, params={}, method='GET', body=None, headers={},
            content_type=None, content_length=True, username=None,
            password=None, capitalize_headers=True)

The parameters are the following:

- url: the URL call, including protocol and parameters (such as
  'http://www.google.com?foo=1&bar=2').
- params: URL parameters as a map, so that {'foo': 1, 'bar': 2} will result
  in an URL ending with '?foo=1&bar=2'.
- method: the HTTP method (such as 'GET' or 'POST'). Defaults to 'GET'.
- body: the body of the request as a string. Defaults to None.
- headers: request headers as a dictionnary. Defaults to '{}'.
- content_type: the content type header of the request. Defauls to None.
- content_length: tells if we should add content length headers to the
  request. Defaults to true.
- username: username while performing basic authentication, must be set
  with password.
- password: password while performing basic authentication, must be set
  with username.
- capitalize_headers: tells if headers should be capitalized (so that their
  names are all like 'Content-Type' for instance).
- follow_redirect: tells if http1 should follow redirections (status codes 3xx).
- max_redirect: maximum number of redirections to follow.

This method returns the response as a Response object described hereafter.

*NOTE*: to call HTTPS URLs, Python must have been built with SSL support.

Response object
===============

This object encapsulates status code (200, 404, as an integer), message (such
as 'OK', 'Not Found', as a string), headers (as a dictionnary), and body (as a
string).

Releases
========

- **0.2.0** (*2014-04-05*): Added option follow_redirect.
- **0.1.4** (*2014-04-04*): Project structure refactoring, included license in
  the archive.
- **0.1.3** (*2013-07-05*): Fixed bug regarding matrix params.
- **0.1.2** (*2012-03-30*): More documentation fixes.
- **0.1.1** (*2012-03-30*): Documentation fixes.
- **0.1.0** (*2012-03-29*): First public release.

Enjoy!

