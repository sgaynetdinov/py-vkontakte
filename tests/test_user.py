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
    assert user.relation is None
    assert user.relation_partner is None


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
@pytest.mark.parametrize('method, field, expected', [
    ('get_activities', 'activities', 'Activities'),
    ('get_activities', 'activities', ''),
    
    ('get_about', 'about', 'About'),
    ('get_about', 'about', ''),

    ('get_books', 'books', 'Book'),
    ('get_books', 'books', ''),

    ('get_games', 'games', 'Games'),
    ('get_games', 'games', ''),

    ('get_movies', 'movies', 'Movies'),
    ('get_movies', 'movies', ''),

    ('get_music', 'music', 'Music'),
    ('get_music', 'music', ''),

    ('get_quotes', 'quotes', 'Quotes'),
    ('get_quotes', 'quotes', ''),

    ('get_tv', 'tv', 'TV'),
    ('get_tv', 'tv', ''),
])
def test_get(mock, method, field, expected):
    user = User.from_json(None, {})
    mock.return_value = [{field: expected}]

    assert getattr(user, method)() == expected 


def test_not_relation(factory):
    user_json = factory('user.json')
    del user_json['relation']

    user = User.from_json(None, user_json)

    assert user.relation is None


@pytest.mark.parametrize('index, expected', [
    (0, None),
    (1, 'single'),
    (2, 'in a relationship'),
    (3, 'engaged'),
    (4, 'married'),
    (5, 'it\'s complicated'),
    (6, 'actively searching'),
    (7, 'in love'),
    (8, 'in a civil union'),
    (9, None),
])
def test_relation(factory, index, expected):
    user_json = factory('user.json')
    user_json['relation'] = index

    user = User.from_json(None, user_json)

    assert user.relation == expected


def test_relation_partner(factory):
    user_json = factory('user.json')
    user_json['relation_partner'] = {'id': 100500, 'first_name': 'Abc', 'last_name': 'Def'}

    user = User.from_json(None, user_json)

    assert user.relation_partner == 100500
