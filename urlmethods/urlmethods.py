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
    return (match.group(2), match.group(4), match.group(5), match.group(7), match.group(9))

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
    
    >>> remote_check('http://example.com/doesnotexists.html')
    False
    
    >>> remote_check('http://doesnotexists.com')
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
    except: # ValueError, urllib2.URLError, httplib.InvalidURL, etc.
        return False
    return True

# To prevent exceptions when local request will be called from request
# we will run it in separated thread.  
@threadmethod()
def local_response(path, query=None, follow_redirect=10):
    """
    Try to fetch specified ``path`` using django.test.Client.
    
    ``query`` is string with query.

    ``follow_redirect`` is number of redirects to be followed.
     
    Return response.
    """
    from django.http import QueryDict
    from django.test.client import Client
    client = Client()
    if query:
        data = QueryDict(query)
    else:
        data = {}
    while True:
        response = client.get(path, data)
        if follow_redirect and follow_redirect > 0 and response.status_code in [301, 302]:
            follow_redirect -= 1
            scheme, authority, path, query, fragment = urlsplit(response['Location'])
            if scheme == 'http' and authority == 'testserver':
                continue
        break
    return response

def local_check(path, query=None, follow_redirect=10):
    """
    Try to fetch specified ``path`` using django.test.Client.
    ``query`` is string with query. 
    Return True if success.
    """
    try:
        response = local_response(path, query, follow_redirect)
        return response.status_code == 200
    except:
        return False
