# coding=utf-8
from .fetch import fetch
from .users import get_users

__all__ = ("groups",)


class Group(object):
    """
    Docs: https://vk.com/dev/objects/groups
    """
    __slots__ = ("id", "name", "screen_name", "is_closed", "is_deactivated", "type", "has_photo",
                 "photo_50", "photo_100", "photo_200", "status", "is_verified", "site")

    @classmethod
    def from_json(cls, group_json):
        group = cls()
        group.id = group_json.get("id")
        group.name = group_json.get("name")
        group.screen_name = group_json.get("screen_name")
        group.is_closed = True if group_json.get("is_closed") else False
        group.is_deactivated = True if group_json.get("deactivated") else False
        group.type = group_json.get("type")
        group.has_photo = bool(group_json.get("has_photo"))
        group.photo_50 = group_json.get("photo_50")
        group.photo_100 = group_json.get("photo_100")
        group.photo_200 = group_json.get("photo_200")
        group.status = group_json.get("status")
        group.is_verified = bool(group_json.get("verified"))
        group.site = group_json.get("site")
        return group

    def get_description(self):
        response = fetch("groups.getById", group_ids=self.id, fields="description")
        return response[0]['description']

    def get_members(self):
        """
        Docs: https://vk.com/dev/groups.getMembers
        """
        MAX_COUNT = 1000

        offset = 0
        while True:
            res = fetch("groups.getMembers", group_id=self.id, count=MAX_COUNT, offset=offset)
            user_ids = res['items']
            if not user_ids:
                raise StopIteration
            for user in get_users(user_ids):
                yield user
            offset += MAX_COUNT

    def get_members_count(self):
        response = fetch("groups.getById", group_ids=self.id, fields="members_count")
        return response[0]['members_count']

    def __repr__(self):
        return u"<Group: {0}>".format(self.screen_name)


def groups(*group_ids):
    group_ids = ",".join((str(i) for i in group_ids))

    fields = ("id", "name", "screen_name", "is_closed", "deactivated", "type", "has_photo",
              "photo_50", "photo_100", "photo_200", "status", "verified", "site")
    response = fetch("groups.getById", group_ids=group_ids, fields=",".join(fields))
    return [Group.from_json(group_json) for group_json in response]
