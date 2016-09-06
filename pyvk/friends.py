# coding=utf-8
from .fetch import fetch
from .users import get_users


class Friends(object):
    @staticmethod
    def get_friends(user_id):
        user_id_items = fetch('friends.get', user_id=user_id)
        return get_users(*user_id_items)

    @staticmethod
    def get_friends_count(user_id):
        user_id_items = fetch('friends.get', user_id=user_id)
        return len(user_id_items)
