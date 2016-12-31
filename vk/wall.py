# coding=utf-8
from datetime import datetime

from .fetch import fetch
from .attachments import get_attachments


class Wall(object):
    """
    Docs: https://vk.com/dev/objects/post
    """
    __slots__ = ('id', 'owner_id', 'from_id', 'unixtime', 'date', 'text', 'reply_owner_id', 'reply_post_id', 'friends_only', 'comments_count', 'likes_count',
                 'reposts_count', 'post_type', 'is_pinned', 'is_ads', 'attachments', 'signer_id')

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
        MAX_COUNT = 100

        offset = 0
        while True:
            res = fetch("wall.get", owner_id=owner_id, count=MAX_COUNT, offset=offset)
            wall_items = res['items']
            if not wall_items:
                raise StopIteration
            for user in (Wall.from_json(wall_json) for wall_json in wall_items):
                yield user
            offset += MAX_COUNT

    @staticmethod
    def get_wall_count(owner_id):
        response = fetch("wall.get", owner_id=owner_id, count=1)
        wall_count = response.get('count')
        return wall_count

    def __repr__(self):
        return u"<Wall id{0}>".format(self.id)
