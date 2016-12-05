# coding=utf-8
from .fetch import fetch, fetch_field


class Wall(object):
    """
    Docs: https://vk.com/dev/objects/post
    """
    def __init__(self, data_json):
        self._data = data_json

    @property
    def id(self):
        return self._data.get('id')

    @property
    def owner_id(self):
        return self._data.get('owner_id')

    @property
    def from_id(self):
        return self._data.get('from_id')

    @property
    def date(self):
        return self._data.get('date')

    @property
    def text(self):
        return self._data.get('text')

    @property
    def reply_owner_id(self):
        return self._data.get('reply_owner_id')

    @property
    def reply_post_id(self):
        return self._data.get('reply_post_id')

    @property
    def friends_only(self):
        return self._data.get('friends_only')

    @property
    def comments_count(self):
        return self._data.get('comments')['count']

    @property
    def likes_count(self):
        return self._data.get('likes')['count']

    @property
    def reposts_count(self):
        return self._data.get('reposts')['count']

    @property
    def post_type(self):
        return self._data.get('post_type')

    @property
    def attachments(self):
        raise NotImplementedError

    @property
    def geo(self):
        raise NotImplementedError

    @property
    def signer_id(self):
        raise NotImplementedError

    @property
    def copy_history(self):
        raise NotImplementedError

    @property
    def is_pinned(self):
        return bool(self._data.get('is_pinned'))

    def get_url(self):
        return 'https://vk.com/wall{0}_{1}'.format(self.owner_id, self.id)

    @staticmethod
    def get_wall(owner_id):
        response = fetch("wall.get", owner_id=owner_id)
        wall_items = response['items']
        return [Wall(wall_json) for wall_json in wall_items]

    @staticmethod
    def get_wall_count(owner_id):
        response = fetch("wall.get", owner_id=owner_id, count=1)
        wall_count = response.get('count')
        return wall_count

    def __repr__(self):
        return u"<Wall id{0}>".format(self.id)
