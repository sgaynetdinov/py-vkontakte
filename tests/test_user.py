import datetime
from unittest.mock import patch

import pytest

from vk.users import User


def test_user(factory):
    user = User.from_json(None, factory('user.json'))

    assert user.id == 1
    assert user.first_name == 'Павел'
    assert user.last_name == 'Дуров'
    assert not user.maiden_name
    assert user.sex == 'male'
    assert user.nickname == ''
    assert user.screen_name == 'durov'
    assert user.domain == 'durov'
    assert user.bdate == '10.10.1984'
    assert user.status == '道德經';
    assert not user.is_deactivated
    assert not user.is_deleted
    assert not user.is_banned
    assert user.is_verified
    assert user.last_seen == datetime.datetime.utcfromtimestamp(1535548834)
    assert user.platform == 'web (vk.com)'
    assert not user.is_trending
    assert user.facebook == '501012028'
    assert user.skype is None
    assert user.twitter == 'durov'
    assert user.livejournal is None
    assert user.instagram == 'durov'
    assert user.site == 'http://t.me/durov'


def test_user_is_deleted(factory):
    user = User.from_json(None, factory('user_is_deleted.json'))

    assert user.is_deactivated
    assert user.is_deleted
    assert not user.is_banned

def test_user_is_banned(factory):
    user_json = factory('user_is_deleted.json')
    user_json['deactivated'] = 'banned'
    user = User.from_json(None, user_json)

    assert user.is_deactivated
    assert not user.is_deleted
    assert user.is_banned

@pytest.mark.parametrize('index, name', [
    (1, 'female'),
    (2, 'male'),
    (4, None),
    (None, None),
])
def test_sex(index, name, factory):
    user_json = factory('user.json')
    user_json['sex'] = index
    user = User.from_json(None, user_json)

    assert user.sex == name


@pytest.mark.parametrize('index, name', [
    (1, "m.vk.com"),
    (2, "iPhone app"),
    (3, "iPad app"),
    (4, "Android app"),
    (5, "Windows Phone app"),
    (6, "Windows 8 app"),
    (7, "web (vk.com)")
])
def test_platform(index, name, factory):
    user_json = factory('user.json')
    user_json['last_seen']['platform'] = index 
    user = User.from_json(None, user_json)

    assert user.platform == name


def test_without_status(factory):
    user_json = factory('user.json')
    assert 'status' in user_json
    del user_json['status']

    user = User.from_json(None, user_json)

    assert user.status == ''


def test_maiden_name(factory):
    user_json = factory('user.json')
    assert 'maiden' not in user_json

    user_json['maiden_name'] = 'Maiden'
    user = User.from_json(None, user_json)
    
    assert user.maiden_name == 'Maiden'

def test_without_last_seen(factory):
    user_json = factory('user.json')
    del user_json['last_seen']

    user = User.from_json(None, user_json)

    assert user.last_seen is None


def test_not_time_in_last_seen(factory):
    user_json = factory('user.json')
    del user_json['last_seen']['time']

    user = User.from_json(None, user_json)

    assert user.last_seen is None


def test_if_not_field_site(factory):
    user_json = factory('user.json')
    del user_json['site']

    user = User.from_json(None, user_json)

    assert user.site is None


@patch('vk.User._fetch')
@pytest.mark.parametrize('expected', ['About', ''])
def test_get_about(mock, expected):
    user = User.from_json(None, {})
    mock.return_value = [{'about': expected}]

    assert user.get_about() == expected 


@patch('vk.User._fetch')
@pytest.mark.parametrize('expected', ['Activities', ''])
def test_get_about(mock, expected):
    user = User.from_json(None, {})
    mock.return_value = [{'activities': expected}]

    assert user.get_activities() == expected 


@patch('vk.User._fetch')
@pytest.mark.parametrize('expected', ['Books', ''])
def test_get_about(mock, expected):
    user = User.from_json(None, {})
    mock.return_value = [{'books': expected}]

    assert user.get_books() == expected 
