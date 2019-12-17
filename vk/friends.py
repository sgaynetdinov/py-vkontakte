class Friends:
    @staticmethod
    def _get_friends(session, user_id):
        """
        https://vk.com/dev/friends.get
        """
        response = session.fetch('friends.get', user_id=user_id)
        return response["items"]

    @staticmethod
    def _get_friends_count(session, user_id):
        """
        https://vk.com/dev/friends.get
        """
        response = session.fetch('friends.get', user_id=user_id, count=1)
        return response["count"]
