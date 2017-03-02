# coding=utf-8
from .base import VKObject
from .fetch import fetch, fetch_items
from .users import get_users
from .wall import Wall

__all__ = ("groups",)


class Group(VKObject):
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

    def get_members(self, sort='id_asc'):
        """
        :param: sort {id_asc, id_desc, time_asc, time_desc} string
        Docs: https://vk.com/dev/groups.getMembers
        """
        return fetch_items("groups.getMembers", get_users, 100, group_id=self.id, sort=sort)

    def get_members_count(self):
        response = fetch("groups.getById", group_ids=self.id, fields="members_count")
        return response[0]['members_count']

    def get_wall(self):
        gid = self.id * (-1)
        return Wall.get_wall(owner_id=gid)

    def get_wall_by_id(self, wall_id):
        gid = self.id * (-1)
        return Wall.get_wall_by_id(owner_id=gid, wall_id=wall_id)

    def get_wall_count(self):
        gid = self.id * (-1)
        return Wall.get_wall_count(owner_id=gid)

    def __hash__(self):
        class_name = type(self).__name__
        return hash(class_name) ^ hash(self.id)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        raise NotImplementedError


def groups(*group_ids):
    group_ids = ",".join((str(i) for i in group_ids))

    fields = ("id", "name", "screen_name", "is_closed", "deactivated", "type", "has_photo",
              "photo_50", "photo_100", "photo_200", "status", "verified", "site")
    response = fetch("groups.getById", group_ids=group_ids, fields=",".join(fields))
    return [Group.from_json(group_json) for group_json in response]
