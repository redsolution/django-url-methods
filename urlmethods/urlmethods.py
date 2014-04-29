"""
http://www.ietf.org/rfc/rfc2396.txt
"""
import re
from threadmethod import threadmethod

SPLIT_RE = re.compile(r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?')


def urlsplit(url):
    """
    Split given ``url`` to the tuple
    (scheme, authority, path, query, fragment).
    
    >>> urlsplit('http://www.ics.uci.edu/pub/ietf/uri/?arg1=value1&arg2=value2#Related')
    ('http', 'www.ics.uci.edu', '/pub/ietf/uri/', 'arg1=value1&arg2=value2', 'Related')
    
    >>> urlsplit('http://www.ics.uci.edu')
    ('http', 'www.ics.uci.edu', '', None, None)
    
    >>> urlsplit('http://www.ics.uci.edu/')
    ('http', 'www.ics.uci.edu', '/', None, None)
    
    >>> urlsplit('http:/www.ics.uci.edu/')
    ('http', None, '/www.ics.uci.edu/', None, None)
    
    >>> urlsplit('http:www.ics.uci.edu/')
    ('http', None, 'www.ics.uci.edu/', None, None)
    
    >>> urlsplit('http/://www.ics.uci.edu/')
    (None, None, 'http/://www.ics.uci.edu/', None, None)

    >>> urlsplit('/img.png')
    (None, None, '/img.png', None, None)
    
    >>> urlsplit('')
    (None, None, '', None, None)
    """
    match = SPLIT_RE.match(url)
    return match.group(2), match.group(4), match.group(5), match.group(7), match.group(9)


def urljoin(scheme, authority, path, query, fragment):
    """
    Join url from given
    ``scheme``, ``authority``, ``path``, ``query``, ``fragment``.

    >>> url = 'http://www.ics.uci.edu/pub/ietf/uri/?arg1=value1&arg2=value2#Related'
    >>> urljoin(*urlsplit(url)) == url
    True

    >>> url = '/img.png'
    >>> urljoin(*urlsplit(url)) == url
    True

    >>> url = ''
    >>> urljoin(*urlsplit(url)) == url
    True
    """
    result = u''
    if scheme is not None:
        result += scheme + ':'
    if authority is not None:
        result += '//' + authority
    if path is not None:
        result += path
    if query is not None:
        result += '?' + query
    if fragment is not None:
        result += '#' + fragment
    return result

URL_FIX_RE = re.compile(r'%(?![0-9A-Fa-f]{2})')
URL_FIX_RELP = '%25'


def urlfix(url):
    """
    Fix quotes in uri.
    
    >>> urlfix('/img.jpg')
    '/img.jpg'

    >>> urlfix('/%69mg.jpg')
    '/%69mg.jpg'

    >>> urlfix('/%mg.jpg')
    '/%25mg.jpg'
    
    >>> urlfix('Q%WW%R%1TT%2%YYY%%34UU%a5%6A')
    'Q%25WW%25R%251TT%252%25YYY%25%34UU%a5%6A'
    """
    return URL_FIX_RE.sub(URL_FIX_RELP, url)


def remote_check(url, user_agent='Urlmethos'):
    """
    Try to fetch specified ``url``.
    Return True if success.
    
    >>> remote_check('http://example.com')
    True

    >>> remote_check('http://example.com/')
    True
    
    >>> remote_check('http://example.com/?ask#anchor')
    True
    
    >>> remote_check('http://example.com/does.not.exist.html')
    False
    
    >>> remote_check('http://does.not.exist')
    False

    >>> remote_check('unsupported://example.com')
    False

    >>> remote_check('example.com')
    False
    """
    import urllib2
    headers = {
        "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
        "Accept-Language": "en-us,en;q=0.5",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
        "Connection": "close",
        "User-Agent": user_agent,
    }
    try:
        req = urllib2.Request(url, None, headers)
        urllib2.urlopen(req)
    except:  # ValueError, urllib2.URLError, httplib.InvalidURL, etc.
        return False
    return True


def get_path(base_url, url):
    """
    Returns None or path after base url.

    >>> get_path('/media/', '/media/foo.bar')
    'foo.bar'

    >>> get_path('/media/', '/media/')
    ''

    >>> get_path('/media/', '/media') is None
    True

    >>> get_path('/media/', 'media/') is None
    True

    >>> get_path('/media/', 'baz') is None
    True

    """
    regexp = re.compile(r'^%s(?P<path>.*)$' % re.escape(base_url))
    match = regexp.match(url)
    if not match:
        return None
    return match.groupdict()['path']


def local_media_response(path, data):
    """
    Returns None or media serve response.

    >>> local_media_response('/foo/bar', {}) is None
    True

    >>> local_media_response('/media/foo', {}).status_code
    200

    >>> local_media_response('/media/does.not.exist', {}).status_code
    404
    """
    from django.conf import settings
    from django.http import Http404, HttpResponseNotFound
    from django.views.static import serve
    from django.test.client import RequestFactory
    media_path = get_path(settings.MEDIA_URL, path)
    if media_path is None:
        return None
    factory = RequestFactory()
    request = factory.get(path, data)
    try:
        return serve(request=request, path=media_path, document_root=settings.MEDIA_ROOT)
    except Http404:
        return HttpResponseNotFound()


def local_static_response(path, data):
    """
    Returns None or static serve response.

    >>> local_static_response('/foo/bar', {}) is None
    True

    >>> local_static_response('/static/admin/css/base.css', {}).status_code
    200

    >>> local_static_response('/static/does.not.exist', {}).status_code
    404
    """
    from django.conf import settings
    from django.contrib.staticfiles.views import serve
    try:
        from django.contrib.staticfiles.handlers import url2pathname
    except ImportError:
        from urllib import url2pathname
    from django.http import Http404, HttpResponseNotFound
    from django.test.client import RequestFactory
    static_path = get_path(settings.STATIC_URL, path)
    if static_path is None:
        return None
    factory = RequestFactory()
    request = factory.get(path, data)
    path_name = url2pathname(static_path)
    try:
        return serve(request=request, path=path_name, insecure=True)
    except Http404:
        return HttpResponseNotFound()


def local_response_unthreaded(path, query=None, follow_redirect=10):
    """
    Try to fetch specified ``path`` using django.test.Client.

    ``query`` is string with query.

    ``follow_redirect`` is number of redirects to be followed.

    Return response.

    You must use threaded version of this function (local_response).
    """
    from django.http import QueryDict
    from django.test.client import Client
    client = Client()
    if query:
        data = QueryDict(query)
    else:
        data = {}
    while True:
        response = local_media_response(path, data)
        if response is None:
            response = local_static_response(path, data)
        if response is None:
            response = client.get(path, data)
        if follow_redirect and follow_redirect > 0 and response.status_code in [301, 302]:
            follow_redirect -= 1
            scheme, authority, path, query, fragment = urlsplit(response['Location'])
            if scheme == 'http' and authority == 'testserver':
                continue
        break
    return response


@threadmethod()
def local_response(path, query=None, follow_redirect=10):
    """
    Try to fetch specified ``path`` using django.test.Client.

    ``query`` is string with query.

    ``follow_redirect`` is number of redirects to be followed.

    Return response.

    To prevent exceptions when local request will be called from request
    we must run it in separated thread.

    >>> local_response('/response').status_code
    200

    >>> local_response('/notfound').status_code
    404

    >>> local_response('/error').status_code
    500

    >>> local_response('/redirect_response').status_code
    200

    >>> local_response('/redirect_notfound').status_code
    404

    >>> local_response('/redirect_redirect_response').status_code
    200

    >>> local_response('/redirect_cicle').status_code
    302

    >>> local_response('/permanent_redirect_response').status_code
    200

    >>> local_response('/http404').status_code
    404

    >>> local_response('/http500')
    Traceback (most recent call last):
        ...
    Exception

    >>> local_response('/request_true_response').content
    'True'

    >>> local_response('/request_false_response').content
    'False'

    >>> local_response('/does.not.exist').status_code
    404

    >>> local_response('/media/foo').status_code
    200

    >>> local_response('/media/does.not.exist').status_code
    404

    >>> local_response('/static/admin/css/base.css').status_code
    200

    >>> local_response('/static/does.not.exist').status_code
    404
    """
    return local_response_unthreaded(path, query, follow_redirect)


def local_check(path, query=None, follow_redirect=10):
    """
    Try to fetch specified ``path`` using django.test.Client.
    ``query`` is string with query.
    Return True if success.

    >>> local_check('/response')
    True

    >>> local_check('/notfound')
    False

    >>> local_check('/error')
    False

    >>> local_check('/redirect_response')
    True

    >>> local_check('/redirect_notfound')
    False

    >>> local_check('/redirect_redirect_response')
    True

    >>> local_check('/redirect_cicle')
    False

    >>> local_check('/permanent_redirect_response')
    True

    >>> local_check('/http404')
    False

    >>> local_check('/http500')
    False

    >>> local_check('/request_true_response')
    True

    >>> local_check('/request_false_response')
    True

    >>> local_check('/does.not.exist')
    False

    >>> local_check('/media/foo')
    True

    >>> local_check('/media/does.not.exist')
    False

    >>> local_check('/static/admin/css/base.css')
    True

    >>> local_check('/static/does.not.exist')
    False
    """
    try:
        response = local_response(path, query, follow_redirect)
        return response.status_code == 200
    except:
        return False
