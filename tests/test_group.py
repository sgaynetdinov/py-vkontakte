import pytest

from vk.groups import Group


def test_detail(factory):
    group = Group.from_json(None, factory('group_detail.json'))

    assert group.id == 1
    assert group.name == "ВКонтакте API"
    assert group.screen_name == 'apiclub'
    assert group.is_closed == False
    assert group.type == 'group'
    assert group.is_trending == False

