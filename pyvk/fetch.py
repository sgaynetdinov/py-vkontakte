# coding=utf-8
import functools
import urllib
import requests

from .error import VKError, VKParseJsonError


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
    params = urllib.urlencode(params)
    url = "https://api.vk.com/method/{method_name}".format(method_name=method_name)
    res = requests.post(url + "?" + params)

    try:
        data_json = res.json()
    except ValueError:
        raise VKParseJsonError

    if 'error' in data_json:
        raise VKError

    if 'response' in data_json:
        return data_json.get('response')
