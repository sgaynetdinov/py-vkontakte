# coding=utf-8
from .base import VKObject
from .fetch import fetch, fetch_items, fetch_post
from .users import User
from .wall import Wall
from .photos import Photo

__all__ = ("get_groups", "get_group")


class Group(VKObject):
    """
    https://vk.com/dev/objects/groups
    """
    GROUP_FIELDS = ("id", "name", "screen_name", "is_closed", "deactivated", "type", "has_photo",
                    "photo_50", "photo_100", "photo_200", "status", "verified", "site")

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

    @classmethod
    def from_json_items(cls, group_json_items):
        return (cls.from_json(group_json) for group_json in group_json_items)

    def get_description(self):
        response = fetch("groups.getById", group_ids=self.id, fields="description")
        return response[0]['description']

    def get_members(self, sort='id_asc'):
        """
        :param: sort {id_asc, id_desc, time_asc, time_desc} string
        Docs: https://vk.com/dev/groups.getMembers
        """
        return fetch_items("groups.getMembers", User.from_json_items, 100, group_id=self.id, sort=sort, fields=User.__slots__ + User.USER_FIELDS)

    def get_members_count(self):
        response = fetch("groups.getById", group_ids=self.id, fields="members_count")
        return response[0]['members_count']

    def get_walls(self):
        gid = self.id * (-1)
        return Wall.get_walls(owner_id=gid)

    def get_wall(self, wall_id):
        gid = self.id * (-1)
        return Wall.get_wall(owner_id=gid, wall_id=wall_id)

    def get_walls_count(self):
        gid = self.id * (-1)
        return Wall.get_walls_count(owner_id=gid)

    @classmethod
    def get_user_groups(cls, user_id, filter):
        """
        https://vk.com/dev/groups.get

        :param filter: {admin, editor, moder, groups, publics, events}
        :yield: Groups
        """
        return fetch_items('groups.get', cls.from_json_items, count=1000, user_id=user_id, filter=filter, extended=1, fields=",".join(cls.GROUP_FIELDS))

    def set_cover_photo(self, file_like, width, height):
        upload_url = Photo.get_owner_cover_photo_upload_server(self.id, crop_x2=width, crop_y2=height)
        files = {'photo': file_like}
        response = fetch_post(upload_url, files=files)
        response_json = response.json()

        Photo.save_owner_cover_photo(response_json['hash'], response_json['photo'])

    def wall_post(self, message=None, attachments=None):
        return Wall.wall_post(owner_id=self.id * -1, message=message, attachments=attachments)


def get_groups(group_ids):
    group_id_items = ",".join((str(group_id) for group_id in group_ids))

    fields = ",".join(Group.GROUP_FIELDS)

    response = fetch("groups.getById", group_ids=group_id_items, fields=fields)
    return (Group.from_json(group_json) for group_json in response)


def get_group(group_id):
    fields = ",".join(Group.GROUP_FIELDS)
    response = fetch("groups.getById", group_ids=group_id, fields=fields)
    return Group.from_json(response[0])
