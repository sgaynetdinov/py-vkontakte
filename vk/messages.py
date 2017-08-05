# coding=utf-8
import random

from .base import VKBase


class Message(VKBase):
    """
    https://vk.com/dev/objects/message
    """
    __slots__ = ('id', 'user_id', 'from_id', 'date', 'read_state', 'out', 'title', 'body', 'geo', 'attachments', 'fwd_messages', 'emoji', 'important',
                 'deleted', 'random_id', '_session')

    @classmethod
    def from_json(cls, session, message_json):
        message = cls()
        message.id = message_json.get('id')
        message.user_id = message_json.get('user_id')
        message.from_id = message_json.get('from_id')
        message.date = message_json.get('date')
        message.read_state = message_json.get('read_state')
        message.out = message_json.get('out')
        message.title = message_json.get('title')
        message.body = message_json.get('body')
        message.geo = message_json.get('geo')
        message.attachments = message_json.get('attachments')
        message.fwd_messages = message_json.get('fwd_messages')
        message.emoji = message_json.get('emoji')
        message.important = message_json.get('important')
        message.deleted = message_json.get('deleted')
        message.random_id = message_json.get('random_id')
        message._session = session
        return message

    @staticmethod
    def get_messages(session, unread=True):
        """
        https://vk.com/dev/messages.getDialogs
        """
        response = session.fetch("messages.getDialogs", unread=unread)
        dialog_json_items = response["items"]
        return (Message.from_json(session, dialog_json["message"]) for dialog_json in dialog_json_items)

    @staticmethod
    def send_message(session, user_id, message):
        """
        https://vk.com/dev/messages.send
        """
        message_id = session.fetch("messages.send", user_id=user_id, message=message, random_id=random.randint(1, 10**6))
        return message_id
