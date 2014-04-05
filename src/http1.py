# encoding=UTF-8

"""
Module to perform HTTP requests. To do so:

  import http

  response = http.request('www.google.com')
  print 'Status: %s (%s)' % (response.status, response.message)
  print 'Headers: %s' % response.headers
  print 'Body: %s' % response.body.strip()

"""

import urllib
import httplib
import urlparse
import base64

class Response(object):
    """HTTP response to encapsulates status code (200, 404, as an integer),
    message (such as 'OK', 'Not Found', as a string), headers (as a
    dictionnary), and body (as a string)."""

    def __init__(self, status, message, headers={}, body=None):
        self.status = status
        self.message = message
        self.headers = headers
        self.body = body

    def __str__(self):
        if self.body:
            _body = str(self.body).strip().replace('\n', '\\n')
            if len(_body) > 100:
                _body = _body[:97]+'...'
        else:
            _body = ''
        return "Response(status=%s, message='%s', headers=%s, body='%s')" %\
            (self.status, self.message, self.headers, _body)


class TooManyRedirectsException(Exception):

    pass


def request(url, params={}, method='GET', body=None, headers={},
            content_type=None, content_length=True,
            username=None, password=None, capitalize_headers=True,
            follow_redirect=True, max_redirect=3):
    """Perform a http_request:
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
    Returns the response as a Response object.
    NOTE: to call HTTPS URLs, Python must have been built with SSL support."""
    _urlparts = urlparse.urlparse(url)
    _host = _urlparts.netloc
    _matrix_params = _urlparts.params
    _params = ''
    if len(_urlparts.query) > 0:
        _params = _urlparts.query
    if len(params) > 0:
        if len(_params) > 0:
            _params += '&'
        _params += urllib.urlencode(params)
    _path = _urlparts.path
    if _matrix_params:
        _path += ';%s' % _matrix_params
    if len(_params) > 0:
        _path += '?'
        _path += _params
    _https = (_urlparts.scheme == 'https')
    _headers = {}
    for _name in headers:
        _headers[str(_name)] = str(headers[_name])
    if content_type:
        _headers['Content-Type'] = str(content_type)
    if content_length:
        if body:
            _headers['Content-Length'] = str(len(body))
        else:
            _headers['Content-Length'] = '0'
    if username and password:
        authorization = "Basic %s" % base64.b64encode(("%s:%s" % (username, password)))
        _headers['Authorization'] = authorization
    _capitalized_headers = {}
    if capitalize_headers:
        for _name in _headers:
            _capitalized = '-'.join([s.capitalize() for s in _name.split('-')])
            _capitalized_headers[_capitalized] =_headers[_name]
        _headers = _capitalized_headers
    if _https:
        connection = httplib.HTTPSConnection(_host)
    else:
        connection = httplib.HTTPConnection(_host)
    connection.request(method, _path, body, _headers)
    _response = connection.getresponse()
    # method getheaders() not available in Python 2.2.1
    _response_headers = {}
    _pairs = _response.msg.items()
    if _pairs:
        for _pair in _pairs:
            _name = _pair[0]
            _value = _pair[1]
            if capitalize_headers:
                _name = '-'.join([s.capitalize() for s in _name.split('-')])
            _response_headers[_name] = _value
    if _response.status >= 300 and _response.status < 400 and \
        follow_redirect:
        if max_redirect <= 0:
            raise TooManyRedirectsException
        location = _response_headers['Location']
        return request(url=location, params=params, method=method,
                       body=body, headers=headers,
                       content_type=content_type,
                       content_length=content_length,
                       username=username, password=password,
                       capitalize_headers=capitalize_headers,
                       follow_redirect=True,
                       max_redirect=max_redirect-1)
    return Response(status=_response.status,
                    message=_response.reason,
                    headers=_response_headers,
                    body=_response.read())
