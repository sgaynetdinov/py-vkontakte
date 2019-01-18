from .attachments import get_attachments
from .base import VKBase


class Comment(VKBase):
    """
    https://vk.com/dev/objects/comment
    """

    __slots__ = ('id', 'owner_id', 'date', 'text', 'reply_to_user', 'reply_to_comment', 'attachments', 'likes_count', '_session')

    @classmethod
    def from_json(cls, session, comment_json):
        comment = cls()
        comment.id = comment_json.get('id')
        comment.owner_id = comment_json.get('from_id')
        comment.date = comment_json.get('date')
        comment.text = comment_json.get('text')
        comment.reply_to_user = comment_json.get('reply_to_user')
        comment.reply_to_comment = comment_json.get('reply_to_comment')
        comment.attachments = get_attachments(session, comment_json.get('attachments'))
        comment.likes_count = comment_json.get('likes').get('count')
        comment._session = session
        return comment

    @staticmethod
    def _get_comments(session, group_or_user_id, wall_id):
        """
        https://vk.com/dev/wall.getComments
        """
        return session.fetch_items("wall.getComments", Comment.from_json, count=100, owner_id=group_or_user_id, post_id=wall_id, need_likes=1)

    @staticmethod
    def _get_comments_count(session, group_or_user_id, wall_id):
        """
        https://vk.com/dev/wall.getComments
        """
        response = session.fetch("wall.getComments", count=100, owner_id=group_or_user_id, post_id=wall_id)
        return response.get('count')
