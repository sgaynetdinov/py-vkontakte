from .fetch import Session
from .groups import Group
from .users import User


class Api:
    def __init__(self, access_token=None):
        self.session = Session(access_token)

    def get_user(self, user_id):
        return User._get_user(self.session, user_id)

    def get_users(self, user_ids):
        return User._get_users(self.session, user_ids)

    def get_group(self, group_id):
        return Group._get_group(self.session, group_id)

    def get_groups(self, group_ids):
        return Group._get_groups(self.session, group_ids)

    def __repr__(self):
        return "Api(access_token={0}***{1})".format(self.session.access_token[:5], self.session.access_token[-3:])
