# coding=utf-8
import urllib


def create_url_get_code(client_id, redirect_uri, display="page", scope=None, response_type="code", version=None, state=None):
    url = "https://oauth.vk.com/authorize"
    params = {
            "client_id":client_id,
            "redirect_uri": redirect_uri,
            "display": display,
            "response_type": response_type
    }

    if scope:
        params['scope'] = scope

    if version:
        params['v'] = version

    if state:
        params['state'] = state

    return u"{url}?{params}".format(url=url, params=urllib.urlencode(params))


def get_access_token(client_id, client_secret, redirect_uri, code):
    pass


