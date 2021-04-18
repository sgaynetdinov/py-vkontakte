import io
import json
import uuid

from .error import VKError, VKParseJsonError

try:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
except ImportError:
    from urllib import urlencode, urlopen


class Session:
    def __init__(self, access_token=None, lang='ru', version_api='5.70'):
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

        request = Request(url, data=urlencode(params).encode())
        res = urlopen(request)

        try:
            data_json = json.load(res)
        except ValueError:
            raise VKParseJsonError

        if 'error' in data_json:
            error = data_json['error']
            error_msg = error['error_msg']
            error_code = error['error_code']
            if error.get('redirect_uri'):
                error_msg += "\n{redirect_uri}".format(redirect_uri=error.get('redirect_uri'))
            raise VKError(message=u"\nError message: {0}"
                                  u"\nError code: {1}"
                                  u"\nError page: https://vk.com/dev/errors".format(error_msg, error_code),
                          code="{0}".format(error_code)
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
                return None

            for i in items:
                yield constructor_from_json(self, i)

            offset += count

    def fetch_photo(self, url, file_obj):
        data, boundary = self._file_upload(file_obj)

        req = Request(url, data=data)
        req.add_header('Content-type', 'multipart/form-data; boundary={0}'.format(boundary))
        req.add_header('Content-length', len(data))

        res = urlopen(req)

        try:
            return json.load(res)
        except ValueError:
            raise VKParseJsonError

    def _convert_list2str(self, fields):
        """
        :param fields: ('bdate', 'domain')
        :return: 'bdate,domain'
        """
        if isinstance(fields, (tuple, list)):
            return ','.join(fields)
        return fields

    def _file_upload(self, file_obj):
        boundary = uuid.uuid4().hex

        buffer = io.BytesIO()
        buffer.write('--{0}\r\n'.format(boundary).encode())
        buffer.write('Content-Disposition: file; name="photo"; filename="photo.jpg"\r\n'.encode())
        buffer.write('Content-Type: application/octet-stream\r\n'.encode())
        buffer.write(b'\r\n')
        buffer.write(file_obj.read())
        buffer.write(b'\r\n')
        buffer.write('--{0}--\r\n'.format(boundary).encode())

        return buffer.getvalue(), boundary
