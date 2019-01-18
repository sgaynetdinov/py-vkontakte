import json

from .error import VKError

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode, urlopen


def get_url_implicit_flow_user(client_id, scope,
                               redirect_uri='https://oauth.vk.com/blank.html', display='page',
                               response_type='token', version=None, state=None, revoke=1):
    """
    https://vk.com/dev/implicit_flow_user

    :return: url
    """
    url = "https://oauth.vk.com/authorize"
    params = {
        "client_id": client_id,
        "scope": scope,
        "redirect_uri": redirect_uri,
        "display": display,
        "response_type": response_type,
        "version": version,
        "state": state,
        "revoke": revoke
    }

    params = {key: value for key, value in params.items() if value is not None}
    return u"{url}?{params}".format(url=url, params=urlencode(params))


def get_url_authcode_flow_user(client_id, redirect_uri, display="page", scope=None, state=None):
    """Authorization Code Flow for User Access Token

    Use Authorization Code Flow to run VK API methods from the server side of an application.
    Access token received this way is not bound to an ip address but set of permissions that can be granted is limited for security reasons.

    Args:
        client_id (int): Application id.
        redirect_uri (str): Address to redirect user after authorization.
        display (str): Sets authorization page appearance.
            Sets: {`page`, `popup`, `mobile`}
            Defaults to `page`
        scope (:obj:`str`, optional): Permissions bit mask, to check on authorization and request if necessary.
            More scope: https://vk.com/dev/permissions
        state (:obj:`str`, optional): An arbitrary string that will be returned together with authorization result.

    Returns:
        str: Url

    Examples:
        >>> vk.get_url_authcode_flow_user(1, 'http://example.com/', scope="wall,email")
        'https://oauth.vk.com/authorize?client_id=1&display=page&redirect_uri=http://example.com/&scope=wall,email&response_type=code

    .. _Docs:
        https://vk.com/dev/authcode_flow_user

    """
    url = "https://oauth.vk.com/authorize"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "display": display,
        "response_type": "code"
    }

    if scope:
        params['scope'] = scope

    if state:
        params['state'] = state

    return u"{url}?{params}".format(url=url, params=urlencode(params))


def create_access_token_from_code(client_id, client_secret, redirect_uri, code):
    url = "https://oauth.vk.com/access_token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code
    }
    res = urlopen(url, data=params)
    res_json = json.loads(res.read())

    if 'access_token' not in res_json:
        raise VKError()

    return res_json['access_token']
