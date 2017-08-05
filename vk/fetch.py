# coding=utf-8
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests

from .error import VKError, VKParseJsonError


class Session(object):
    def __init__(self, access_token=None, lang='ru', version_api='5.53'):
        self.access_token = access_token
        self.lang = lang
        self.version_api = version_api

    def fetch(self, method_name, **params):
        url = "https://api.vk.com/method/{method_name}".format(method_name=method_name)
        params['v'] = self.version_api
        params['lang'] = self.lang
        params['access_token'] = self.access_token

        if params.get('fields'):
            params['fields'] = self._convert_list2str(params.get('fields'))

        params = {key: value for key, value in params.items() if value is not None}

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
                u"\nRequest: {url}"
                u"\n{error_msg}"
                u"\nError code: {error_code}"
                u"\nError page: https://vk.com/dev/errors".format(url=res.url, error_msg=error_msg, error_code=error_code)
            )

        if 'response' in data_json:
            return data_json.get('response')

    def fetch_items(self, method_name, constructor_from_json, count, **params):
        params['access_token'] = self.access_token
        offset = 0
        while True:
            res = self.fetch(method_name, count=count, offset=offset, **params)

            if isinstance(res, list) and len(res) == 1:
                res = res[0]
                if res.get('users'):
                    items = res['users']['items']
            elif isinstance(res, dict):
                items = res['items']

            if not items:
                raise StopIteration

            for i in items:
                yield constructor_from_json(self, i)

            offset += count

    def fetch_post(self, url, **kwargs):
        return requests.post(url, **kwargs)

    def _convert_list2str(self, fields):
        """
        :param fields: ('bdate', 'domain')
        :return: 'bdate,domain'
        """
        if isinstance(fields, tuple) or isinstance(fields, list):
            return ','.join(fields)
        return fields
