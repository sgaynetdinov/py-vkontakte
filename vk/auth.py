# coding=utf-8
__all__ = ["set_access_token", "get_access_token", "create_access_token", "create_url_get_code"]

import urllib
import requests

from .error import VKError


_ACCESS_TOKEN = None


def set_access_token(access_token):
    global _ACCESS_TOKEN
    _ACCESS_TOKEN = access_token


def get_access_token():
    return _ACCESS_TOKEN


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


def create_access_token(client_id, client_secret, redirect_uri, code):
    url = "https://oauth.vk.com/access_token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code
    }
    res = requests.post(url, params=params)
    res_json = res.json()

    if 'access_token' not in res_json:
        raise VKError()

    return res_json['access_token']
