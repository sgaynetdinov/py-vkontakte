# coding=utf-8
import functools
import urllib
import requests

from .error import VKError, VKParseJsonError
from .auth import get_access_token


def fetch_field(method_name, field_name=None):

    def decorate(func):

        @functools.wraps(func)
        def f(self):
            _field_name = field_name if field_name else func.__name__
            try:
                return func(self)
            except KeyError:
                users_json = fetch(method_name, user_ids=self.id, fields=_field_name)
                user = self.__class__(users_json[0])
                try:
                    self._data.update({
                        _field_name: user._data[_field_name]
                    })
                    return getattr(self, func.__name__)
                except KeyError:
                    raise AttributeError("object '{0}' has no attribute '{1}'".format(self.__class__.__name__, _field_name))

        return f

    return decorate


def fetch(method_name, **params):
    url = "https://api.vk.com/method/{method_name}".format(method_name=method_name)
    params['v'] = '5.53'

    if get_access_token():
        params['access_token'] = get_access_token()

    if params.get('fields'):
        params['fields'] = convert_list2str(params.get('fields'))

    params = urllib.urlencode(params)
    res = requests.post(url + "?" + params)

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


def convert_list2str(fields):
    """
    :param fields: ('bdate', 'domain')
    :return: 'bdate,domain'
    """
    if isinstance(fields, tuple) or isinstance(fields, list):
        return ','.join(fields)
    return fields
