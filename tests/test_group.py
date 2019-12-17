from unittest.mock import patch

import pytest

from vk.groups import Group
from vk.users import User


def test_detail(factory):
    group = Group.from_json(None, factory('group_detail.json'))

    assert group.id == 1
    assert group.name == "ВКонтакте API"
    assert group.screen_name == 'apiclub'
    assert group.is_closed == False
    assert group.type == 'group'
    assert group.is_trending == False


@pytest.mark.parametrize("user", [
    "100500",
    100500.0,
])
def test_contains_fail(factory, user):
    group = Group.from_json(None, factory('group_detail.json'))

    with pytest.raises(TypeError, match="is not `User`"):
        user in group


@pytest.mark.parametrize("user", [
    User.from_json(None, {"id": 100500}),
    100500,
])
def test_contains(factory, user):
    session = type("", (object,), {"fetch": lambda *args, **kw: True})
    group = Group.from_json(session, factory('group_detail.json'))

    assert user in group
