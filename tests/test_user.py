import datetime

import pytest

from vk.users import User


def test_user(factory):
    user = User.from_json(None, factory('user.json'))

    assert user.id == 1
    assert user.first_name == 'Павел'
    assert user.last_name == 'Дуров'
    assert user.sex == 'male'
    assert user.nickname == ''
    assert user.screen_name == 'durov'
    assert user.domain == 'durov'
    assert user.bdate == '10.10.1984'
    assert user.status == '&#36947;&#24503;&#32147;'
    assert not user.is_deactivated
    assert not user.is_deleted
    assert not user.is_banned
    assert not user.is_hidden
    assert user.is_verified
    assert user.last_seen == datetime.datetime.utcfromtimestamp(1535548834)
    assert user.platform == 'web (vk.com)'
    assert not user.is_trending


def test_user_is_deleted(factory):
    user = User.from_json(None, factory('user_is_deleted.json'))

    assert user.id == 3
    assert user.is_deactivated
    assert user.is_deleted
    assert not user.is_banned
    assert not user.is_hidden


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
