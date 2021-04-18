from .base import VKBase
from .messages import Message
from .photos import Photo
from .users import User
from .wall import Wall


class Group(VKBase):
    """
    https://vk.com/dev/objects/group
    """
    GROUP_FIELDS = ("id", "name", "screen_name", "is_closed", "deactivated", "type", "has_photo",
                    "photo_50", "photo_100", "photo_200", "status", "verified", "site", "trending")

    __slots__ = ("id", "name", "screen_name", "is_closed", "is_deactivated", "type", "has_photo",
                 "photo_50", "photo_100", "photo_200", "status", "is_verified", "site", "is_trending", "_session")

    @classmethod
    def from_json(cls, session, group_json):
        group = cls()
        group.id = group_json.get("id")
        group.name = group_json.get("name")
        group.screen_name = group_json.get("screen_name")
        group.is_closed = bool(group_json.get("is_closed"))
        group.is_deactivated = bool(group_json.get("deactivated"))
        group.type = group_json.get("type")
        group.has_photo = bool(group_json.get("has_photo"))
        group.photo_50 = group_json.get("photo_50")
        group.photo_100 = group_json.get("photo_100")
        group.photo_200 = group_json.get("photo_200")
        group.status = group_json.get("status")
        group.is_verified = bool(group_json.get("verified"))
        group.is_trending = bool(group_json.get("trending"))
        group.site = group_json.get("site")
        group._session = session
        return group

    def get_description(self):
        response = self._session.fetch("groups.getById", group_ids=self.id, fields="description")
        return response[0]['description']

    def get_members(self, sort='id_asc'):
        """
        :param: sort {id_asc, id_desc, time_asc, time_desc} string
        Docs: https://vk.com/dev/groups.getMembers
        """
        return self._session.fetch_items("groups.getMembers", User.from_json, 1000, group_id=self.id, sort=sort, fields=User.USER_FIELDS)

    def get_members_only_id(self):
        return self._session.fetch_items("groups.getMembers", lambda _, user_id: user_id, 1000, group_id=self.id)

    def get_members_count(self):
        response = self._session.fetch("groups.getById", group_ids=self.id, fields="members_count")
        return response[0]['members_count']

    def get_walls(self):
        gid = self.id * (-1)
        return Wall._get_walls(self._session, owner_id=gid)

    def get_wall(self, wall_id):
        gid = self.id * (-1)
        return Wall._get_wall(self._session, owner_id=gid, wall_id=wall_id)

    def get_walls_count(self):
        gid = self.id * (-1)
        return Wall._get_walls_count(self._session, owner_id=gid)

    def set_cover_photo(self, file_like, width, height):
        upload_url = Photo._get_owner_cover_photo_upload_server(self._session, self.id, crop_x2=width, crop_y2=height)
        response_json = self._session.fetch_photo(upload_url, file_like)

        Photo._save_owner_cover_photo(self._session, response_json['hash'], response_json['photo'])

    def wall_post(self, message=None, attachments=None):
        return Wall._wall_post(self._session, owner_id=self.id * -1, message=message, attachments=attachments)

    def send_messages(self, user_id, message=None, image_files=None):
        return Message._send_message(self._session, user_id, message, image_files)

    def messages_set_typing(self, user_id):
        Message.set_typing(self._session, user_id=user_id)

    def get_dialog(self, unread=False, important=False, unanswered=False):
        return Message.get_dialog(self._session, unread=unread, important=important, unanswered=unanswered)

    @staticmethod
    def _get_user_groups(session, user_id, filter):
        """
        https://vk.com/dev/groups.get

        :param filter: {admin, editor, moder, groups, publics, events}
        :yield: Groups
        """
        return session.fetch_items('groups.get', Group.from_json, count=1000, user_id=user_id, filter=filter, extended=1, fields=",".join(Group.GROUP_FIELDS))

    @staticmethod
    def _get_groups(session, group_ids):
        group_id_items = ",".join((str(group_id) for group_id in group_ids))

        fields = ",".join(Group.GROUP_FIELDS)

        response = session.fetch("groups.getById", group_ids=group_id_items, fields=fields)
        return (Group.from_json(session, group_json) for group_json in response)

    @staticmethod
    def _get_group(session, group_id):
        fields = ",".join(Group.GROUP_FIELDS)
        response = session.fetch("groups.getById", group_ids=group_id, fields=fields)
        return Group.from_json(session, response[0])

    def __contains__(self, user_instance):
        """
        https://vk.com/dev/groups.isMember
        """
        if not isinstance(user_instance, (int, User)):
            raise TypeError("object {0} is not `User`".format(user_instance))

        user_id = user_instance.id if hasattr(user_instance, "id") else user_instance

        return bool(self._session.fetch("groups.isMember", group_id=self.id, user_id=user_id))
