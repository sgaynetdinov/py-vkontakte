# coding=utf-8
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests

from .auth import get_access_token
from .error import VKError, VKParseJsonError


VERSION_API = '5.53'


def fetch(method_name, **params):
    url = "https://api.vk.com/method/{method_name}".format(method_name=method_name)
    params['v'] = VERSION_API

    if get_access_token():
        params['access_token'] = get_access_token()

    if params.get('fields'):
        params['fields'] = convert_list2str(params.get('fields'))

    res = requests.post(url + "?" + urlencode(params))

    try:
        data_json = res.json()
    except ValueError:
        raise VKParseJsonError

    if 'error' in data_json:
        error = data_json['error']
        error_msg = error['error_msg']
        error_code = error['error_code']
        if error.get('redirect_uri'):
            error_msg += "\n{redirect_uri}".format(redirect_uri=error.get('redirect_uri'))
        raise VKError(
            u"{error_msg}"
            u"\nError code: {error_code}"
            u"\nError page: https://vk.com/dev/errors".format(error_msg=error_msg, error_code=error_code)
        )

    if 'response' in data_json:
        return data_json.get('response')


def fetch_items(method_name, constructor_vkobject, count, **params):
    offset = 0
    while True:
        res = fetch(method_name, count=count, offset=offset, **params)

        if isinstance(res, list) and len(res) == 1:
            res = res[0]
            if res.get('users'):
                items = res['users']['items']
        elif isinstance(res, dict):
            items = res['items']

        if not items:
            raise StopIteration

        for obj in constructor_vkobject(items):
            yield obj

        offset += count


def convert_list2str(fields):
    """
    :param fields: ('bdate', 'domain')
    :return: 'bdate,domain'
    """
    if isinstance(fields, tuple) or isinstance(fields, list):
        return ','.join(fields)
    return fields
