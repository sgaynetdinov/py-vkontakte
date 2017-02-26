# coding=utf-8
from .attachments import get_attachments
from .base import VKObject
from .fetch import fetch, fetch_items


class Comment(VKObject):
    """
    https://vk.com/dev/objects/comment
    """

    __slots__ = ('id', 'owner_id', 'date', 'text', 'reply_to_user', 'reply_to_comment', 'attachments')

    @classmethod
    def from_json(cls, comment_json):
        comment = cls()
        comment.id = comment_json.get('id')
        comment.owner_id = comment_json.get('from_id')
        comment.date = comment_json.get('date')
        comment.text = comment_json.get('text')
        comment.reply_to_user = comment_json.get('reply_to_user')
        comment.reply_to_comment = comment_json.get('reply_to_comment')
        comment.attachments = get_attachments(comment_json.get('attachments'))
        return comment

    @classmethod
    def from_json_items(cls, comment_json_items):
        return (cls.from_json(comment_json) for comment_json in comment_json_items)

    @classmethod
    def get_comments(cls, group_or_user_id, wall_id):
        """
        https://vk.com/dev/wall.getComments
        """
        return fetch_items("wall.getComments", cls.from_json_items, count=100, owner_id=group_or_user_id, post_id=wall_id)

    @classmethod
    def get_comments_count(cls, group_or_user_id, wall_id):
        """
        https://vk.com/dev/wall.getComments
        """
        response = fetch("wall.getComments", count=100, owner_id=group_or_user_id, post_id=wall_id)
        return response.get('count')
