import pytest

from vk.users import UserCareer


def test_user_career(factory):
    career_json = factory('user_career.json')['career'][0]
    career = UserCareer.from_json(None, career_json)

    assert isinstance(career, UserCareer)
    assert career.group == 22822305
    assert career.company is None
    assert career.country == 1
    assert career.city == 2
    assert career.city_name is None
    assert career.start == 2006
    assert career.end == 2014
    assert career.position == 'Генеральный директор'


def test_without_group_id(factory):
    career_json = factory('user_career.json')['career'][1]
    career = UserCareer.from_json(None, career_json)

    assert 'group_id' not in career_json
    assert career.group is None
    assert career.company == 'Telegram'


def test_without_city_id(factory):
    career_json = factory('user_career.json')['career'][0]
    del career_json['city_id']
    career_json['city_name'] = 'Moscow'

    career = UserCareer.from_json(None, career_json)

    assert 'city_id' not in career_json
    assert career.city is None
    assert career.city_name == 'Moscow'

