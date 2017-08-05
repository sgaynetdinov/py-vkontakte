# coding=utf-8
from .fetch import fetch


class Friends(object):
    @staticmethod
    def get_friends(user_id):
        """
        https://vk.com/dev/friends.get
        """
        response = fetch('friends.get', user_id=user_id)
        return response["items"]

    @staticmethod
    def get_friends_count(user_id):
        """
        https://vk.com/dev/friends.get
        """
        response = fetch('friends.get', user_id=user_id, count=1)
        return response["count"]
