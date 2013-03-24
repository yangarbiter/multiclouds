import urllib
import urlparse
 
def mk_header_no_token(app_info):
    s = 'OAuth oauth_version="1.0", oauth_signature_method="PLAINTEXT"'
    s += ', oauth_consumer_key="%s"' % (urllib.quote_plus(app_info.key),)
    s += ', oauth_signature="%s&"' % (urllib.quote_plus(app_info.secret),)
    return s


def mk_header_with_token(app_info, token):
    s = 'OAuth oauth_version="1.0", oauth_signature_method="PLAINTEXT"'
    s += ', oauth_consumer_key="%s"' % (urllib.quote_plus(app_info.key),)
    s += ', oauth_token="%s"' % (urllib.quote_plus(token.key),)
    s += ', oauth_signature="%s&%s"' % (urllib.quote_plus(app_info.secret), urllib.quote_plus(token.secret))
    return s


def parse_token(body):
    params = urlparse.parse_qs(body, strict_parsing=True)
    key = expect_exactly_one(params, 'oauth_token')
    secret = expect_exactly_one(params, 'oauth_token_secret')
    return Token(key, secret)


def expect_exactly_one(params, param_name):
    l = params.get(param_name)
    if l is None: raise ValueError("missing %r parameter" % (param_name,))
    if len(l) != 1: raise ValueError("more than one %r parameter" % (param_name,))
    return l[0]


class AppInfo(object):
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
    def __str__(self):
        return "%r %r" % (self.key, self.secret,)


class Token(object):
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
    def __str__(self):
        return "%r %r" % (self.key, self.secret,)