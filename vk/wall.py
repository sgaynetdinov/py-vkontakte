# coding=utf-8
from datetime import datetime

from .attachments import get_attachments
from .base import VKObject
from .comment import Comment
from .fetch import fetch, fetch_items


class Wall(VKObject):
    """
    https://vk.com/dev/objects/post
    """

    __slots__ = ('attachments', 'date', 'friends_only', 'from_id', 'id', 'is_ads', 'is_pinned', 'owner_id',
                 'post_type', 'reply_owner_id', 'reply_post_id', 'signer_id', 'text', 'unixtime')

    @classmethod
    def from_json(cls, wall_json):
        wall = cls()
        wall.attachments = get_attachments(wall_json.get("attachments"))
        wall.date = datetime.utcfromtimestamp(wall_json.get("date"))
        wall.friends_only = wall_json.get("friends_only")
        wall.from_id = wall_json.get("from_id")
        wall.id = wall_json.get("id")
        wall.is_ads = bool(wall_json.get("marked_as_ads"))
        wall.is_pinned = bool(wall_json.get("is_pinned"))
        wall.owner_id = wall_json.get("owner_id")
        wall.post_type = wall_json.get("post_type")
        wall.reply_owner_id = wall_json.get("reply_owner_id")
        wall.reply_post_id = wall_json.get("reply_post_id")
        wall.signer_id = wall_json.get("signer_id")
        wall.text = wall_json.get("text")
        wall.unixtime = wall_json.get("date")
        return wall

    @classmethod
    def from_json_items(cls, wall_json_items):
        return (cls.from_json(wall_json) for wall_json in wall_json_items)

    def get_comments(self):
        return Comment.get_comments(group_or_user_id=self.owner_id, wall_id=self.id)

    def get_comments_count(self):
        return Comment.get_comments_count(group_or_user_id=self.owner_id, wall_id=self.id)

    def get_likes(self):
        """
        https://vk.com/dev/likes.getList
        """
        from .users import get_users
        return fetch_items('likes.getList', get_users, count=100, type='post', owner_id=self.from_id, item_id=self.id)

    def get_likes_count(self):
        """
        https://vk.com/dev/likes.getList
        """
        response = fetch('likes.getList', count=1, type='post', owner_id=self.from_id, item_id=self.id)
        likes_count = response.get('count')
        return likes_count

    def get_reposts(self):
        """
        https://vk.com/dev/wall.getReposts
        """
        return fetch_items('wall.getReposts', self.from_json_items, count=1000, owner_id=self.from_id, post_id=self.id)

    def get_reposts_count(self):
        posts = "{0}_{1}".format(self.from_id, self.id)
        response = fetch("wall.getById", posts=posts)
        return response[0].get('reposts')['count']

    def get_url(self):
        return 'https://vk.com/wall{0}_{1}'.format(self.owner_id, self.id)

    @staticmethod
    def get_wall(owner_id, wall_id):
        posts = "{0}_{1}".format(owner_id, wall_id)
        response = fetch("wall.getById", posts=posts)
        if not response:
            return None
        return Wall.from_json(response[0])

    @staticmethod
    def get_walls(owner_id):
        return fetch_items("wall.get", Wall.from_json_items, 100, owner_id=owner_id)

    @staticmethod
    def get_walls_count(owner_id):
        response = fetch("wall.get", owner_id=owner_id, count=1)
        wall_count = response.get('count')
        return wall_count

    def pin(self):
        response = fetch("wall.pin", owner_id=self.owner_id, post_id=self.id)
        return bool(response)

    def unpin(self):
        response = fetch("wall.unpin", owner_id=self.owner_id, post_id=self.id)
        return bool(response)

    @classmethod
    def wall_post(cls, owner_id, message=None, attachments=None, from_group=True):
        """
        https://vk.com/dev/wall.post
        attachments: "photo100172_166443618,photo-1_265827614"
        """
        response = fetch("wall.post", owner_id=owner_id, message=message, attachments=attachments, from_group=from_group)
        return response
