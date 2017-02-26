# coding=utf-8
from datetime import datetime

from .attachments import get_attachments
from .base import VKObject
from .fetch import fetch, fetch_items


class Wall(VKObject):
    """
    Docs: https://vk.com/dev/objects/post
    """
    __slots__ = ('id', 'owner_id', 'from_id', 'unixtime', 'date', 'text', 'reply_owner_id', 'reply_post_id', 'friends_only', 'comments_count',
                 'likes_count', 'reposts_count', 'post_type', 'is_pinned', 'is_ads', 'attachments', 'signer_id')

    @classmethod
    def from_json(cls, wall_json):
        wall = cls()
        wall.id = wall_json.get("id")
        wall.owner_id = wall_json.get("owner_id")
        wall.from_id = wall_json.get("from_id")
        wall.unixtime = wall_json.get("date")
        wall.date = datetime.utcfromtimestamp(wall.unixtime)
        wall.text = wall_json.get("text")
        wall.reply_owner_id = wall_json.get("reply_owner_id")
        wall.reply_post_id = wall_json.get("reply_post_id")
        wall.friends_only = wall_json.get("friends_only")
        wall.comments_count = wall_json.get('comments')['count']
        wall.likes_count = wall_json.get('likes')['count']
        wall.reposts_count = wall_json.get('reposts')['count']
        wall.post_type = wall_json.get("post_type")
        wall.is_pinned = bool(wall_json.get("is_pinned"))
        wall.is_ads = bool(wall_json.get("marked_as_ads"))
        wall.attachments = get_attachments(wall_json.get("attachments"))
        wall.signer_id = wall_json.get("signer_id")
        return wall

    def pin(self):
        response = fetch("wall.pin", owner_id=self.owner_id, post_id=self.id)
        return bool(response)

    def unpin(self):
        response = fetch("wall.unpin", owner_id=self.owner_id, post_id=self.id)
        return bool(response)

    @property
    def geo(self):
        raise NotImplementedError

    @property
    def copy_history(self):
        raise NotImplementedError

    def get_url(self):
        return 'https://vk.com/wall{0}_{1}'.format(self.owner_id, self.id)

    @staticmethod
    def get_wall(owner_id):
        return fetch_items("wall.get", Wall.get_walls, 100, owner_id=owner_id)

    @staticmethod
    def get_wall_by_id(owner_id, wall_id):
        posts = "{0}_{1}".format(owner_id, wall_id)
        response = fetch("wall.getById", posts=posts)
        if not response:
            return None
        return Wall.from_json(response[0])

    @staticmethod
    def get_wall_count(owner_id):
        response = fetch("wall.get", owner_id=owner_id, count=1)
        wall_count = response.get('count')
        return wall_count

    @classmethod
    def get_walls(cls, wall_items):
        return (cls.from_json(wall_json) for wall_json in wall_items)
