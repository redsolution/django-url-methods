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
    """
    match = SPLIT_RE.match(url)
    return (match.group(2), match.group(4), match.group(5), match.group(7), match.group(9))

def urljoin(scheme, authority, path, query, fragment):
    """
    Join url from given
    ``scheme``, ``authority``, ``path``, ``query``, ``fragment``.
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
    """
    return URL_FIX_RE.sub(URL_FIX_RELP, url)

def urlcheck(url, user_agent='Urlmethos'):
    """
    Try to fetch specified ``url``.
    Return True if success.
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
def urllocal_response(path, query=None, follow_redirect=10):
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
        data = None
    while True:
        response = client.get(path, data)
        if follow_redirect and response.status_code in [301, 302]:
            follow_redirect -= 1
            scheme, authority, path, query, fragment = urlsplit(response['Location'])
            if scheme is None and authority is None:
                continue
        break
        redirects += 1

def urllocal(path, query=None, follow_redirect=10):
    """
    Try to fetch specified ``path`` using django.test.Client.
    ``query`` is string with query. 
    Return True if success.
    """
    try:
        response = urllocal_response(path, query, follow_redirect)
        return response.status_code == 200
    except:
        return False
