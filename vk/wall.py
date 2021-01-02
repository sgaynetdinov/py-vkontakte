from datetime import datetime

from .attachments import get_attachments
from .base import VKBase
from .comment import Comment


class Wall(VKBase):
    """
    https://vk.com/dev/objects/post
    """

    __slots__ = ('attachments', 'date', 'friends_only', 'from_id', 'id', 'is_ads', 'is_pinned', 'owner_id',
                 'post_type', 'reply_owner_id', 'reply_post_id', 'signer_id', 'text', 'unixtime', 'views', '_session')

    @classmethod
    def from_json(cls, session, wall_json):
        wall = cls()
        wall.attachments = get_attachments(session, wall_json.get("attachments"))
        wall.date = datetime.utcfromtimestamp(wall_json.get("date"))
        wall.friends_only = bool(wall_json.get("friends_only"))
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
        wall.views = cls._views(wall_json.get("views"))
        wall._session = session
        return wall

    def get_comments(self):
        return Comment._get_comments(self._session, group_or_user_id=self.owner_id, wall_id=self.id)

    def get_comments_count(self):
        return Comment._get_comments_count(self._session, group_or_user_id=self.owner_id, wall_id=self.id)

    def get_likes(self):
        """
        https://vk.com/dev/likes.getList
        """
        from .users import User
        return self._session.fetch_items('likes.getList', User._get_user, count=100, type='post', owner_id=self.from_id, item_id=self.id)

    def get_likes_count(self):
        """
        https://vk.com/dev/likes.getList
        """
        response = self._session.fetch('likes.getList', count=1, type='post', owner_id=self.from_id, item_id=self.id)
        return response.get('count')

    def get_reposts(self):
        """
        https://vk.com/dev/wall.getReposts
        """
        return self._session.fetch_items('wall.getReposts', self.from_json, count=1000, owner_id=self.from_id, post_id=self.id)

    def get_reposts_count(self):
        posts = "{0}_{1}".format(self.from_id, self.id)
        response = self._session.fetch("wall.getById", posts=posts)
        return response[0].get('reposts')['count']

    def get_url(self):
        return 'https://vk.com/wall{0}_{1}'.format(self.owner_id, self.id)

    def pin(self):
        response = self._session.fetch("wall.pin", owner_id=self.owner_id, post_id=self.id)
        return bool(response)

    def unpin(self):
        response = self._session.fetch("wall.unpin", owner_id=self.owner_id, post_id=self.id)
        return bool(response)

    @staticmethod
    def _get_wall(session, owner_id, wall_id):
        posts = "{0}_{1}".format(owner_id, wall_id)
        response = session.fetch("wall.getById", posts=posts)
        if not response:
            return None
        return Wall.from_json(session, response[0])

    @classmethod
    def _views(cls, views):
        if views:
            return views['count']

    @staticmethod
    def _get_walls(session, owner_id):
        """
        https://vk.com/dev/wall.get
        """
        return session.fetch_items("wall.get", Wall.from_json, 100, owner_id=owner_id)

    @staticmethod
    def _get_walls_count(session, owner_id):
        response = session.fetch("wall.get", owner_id=owner_id, count=1)
        return response.get('count')

    @staticmethod
    def _wall_post(session, owner_id, message=None, attachments=None, from_group=True):
        """
        https://vk.com/dev/wall.post
        attachments: "photo100172_166443618,photo-1_265827614"
        """
        return session.fetch(
            "wall.post",
            owner_id=owner_id,
            message=message,
            attachments=attachments,
            from_group=from_group,
        )
