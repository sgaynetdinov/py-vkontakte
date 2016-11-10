# coding=utf-8
import itertools

from .database import getCitiesById, getCountriesById
from .fetch import fetch, fetch_field
from .wall import Wall

__all__ = ["get_user", "get_users"]


def grouper(iterable, n):
    """
    grouper([0,1,2,3,4], 3) --> [(0,1,2), (3,4)]
    https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    args = [iter(iterable)] * n
    grouper_items = list(itertools.izip_longest(*args))

    last_items = grouper_items[-1]
    if last_items[-1] is None:
        last_items_without_None = (i for i in last_items if i is not None)
        without_last_items = grouper_items[:-1]
        without_last_items.append(tuple(last_items_without_None))
        return without_last_items

    return grouper_items


def get_user(slug_or_user_id):
    """
    :param slug_or_user_id: str or int
    :return: User
    """
    if isinstance(slug_or_user_id, basestring) or isinstance(slug_or_user_id, int):
        user_json_items = fetch('users.get', user_ids=slug_or_user_id)
        return User(user_json_items[0])
    raise ValueError


def get_users(user_ids):
    if not user_ids:
        return []

    user_items = []
    for u_ids in grouper(user_ids, 300):
        _user_ids = ",".join([str(i) for i in u_ids])
        user_items.append(fetch('users.get', user_ids=_user_ids))
    return [User(user_json) for user_json in sum(user_items, [])]


class User(object):
    """
    Docs: https://vk.com/dev/objects/user
    """

    def __init__(self, user_json):
        self.id = user_json.get('id')
        self._data = user_json
        self.first_name = user_json.get('first_name')
        self.last_name = user_json.get('last_name')
        self.is_deactivated = True if user_json.get('deactivated') else False

    @property
    def is_hidden(self):
        """
        :return: bool
        """
        return True if self._data.get('hidden') else False

    @property
    def is_banned(self):
        """
        :return: bool
        """
        if self._data.get('deactivated') == 'banned':
            return True
        return False

    @property
    def is_deleted(self):
        """
        :return: bool
        """
        if self._data.get('deactivated') == 'deleted':
            return True
        return False

    @property
    @fetch_field('users.get')
    def about(self):
        """
        :return: string
        """
        return self._data['about']

    @property
    @fetch_field('users.get')
    def activities(self):
        """
        :return: string
        """
        return self._data['activities']

    @property
    @fetch_field('users.get')
    def bdate(self):
        """
        :return: string
        """
        return self._data['bdate']

    @property
    def blacklisted(self):
        raise NotImplementedError

    @property
    def blacklisted_by_me(self):
        raise NotImplementedError

    @property
    @fetch_field('users.get')
    def books(self):
        """
        :return: string
        """
        return self._data['books']

    @property
    def can_post(self):
        raise NotImplementedError

    @property
    def can_see_all_posts(self):
        raise NotImplementedError

    @property
    def can_see_audio(self):
        raise NotImplementedError

    @property
    def can_send_friend_request(self):
        raise NotImplementedError

    @property
    def can_write_private_message(self):
        raise NotImplementedError

    @property
    def career(self):
        raise NotImplementedError

    @property
    @fetch_field('users.get')
    def city(self):
        """
        :return: string
        """
        city_id = self._data['city']
        return getCitiesById(city_id)

    @property
    def common_count(self):
        raise NotImplementedError

    @property
    def connections(self):
        raise NotImplementedError

    @property
    def contacts(self):
        raise NotImplementedError

    @property
    def counters(self):
        raise NotImplementedError

    @property
    @fetch_field('users.get')
    def country(self):
        """
        :return: string
        """
        country_id = self._data['country']
        return getCountriesById(country_id)

    @property
    def crop_photo(self):
        raise NotImplementedError

    @property
    @fetch_field('users.get')
    def domain(self):
        """
        :return: string
        """
        return self._data['domain']

    @property
    def education(self):
        raise NotImplementedError

    @property
    def exports(self):
        raise NotImplementedError

    # first_name_{case}

    @property
    @fetch_field('users.get')
    def followers_count(self):
        """
        :return: integer
        """
        return self._data['followers_count']

    @property
    def friend_status(self):
        raise NotImplementedError

    @property
    @fetch_field('users.get')
    def games(self):
        """
        :return: string
        """
        return self._data['games']

    @property
    @fetch_field('users.get')
    def has_mobile(self):
        """
        :return: bool
        """
        return bool(self._data['has_mobile'])

    @property
    @fetch_field('users.get')
    def has_photo(self):
        """
        :return: bool
        """
        return bool(self._data['has_photo'])

    @property
    @fetch_field('users.get')
    def home_town(self):
        """
        :return: string
        """
        return self._data['home_town']

    @property
    @fetch_field('users.get')
    def interests(self):
        """
        :return: string
        """
        return self._data['interests']

    @property
    def is_favorite(self):
        raise NotImplementedError

    @property
    def is_friend(self):
        raise NotImplementedError

    @property
    def is_hidden_from_feed(self):
        raise NotImplementedError

    # last_name_{case}

    @property
    @fetch_field('users.get')
    def last_seen(self):
        """
        :return: unix-time
        """
        return self._data["last_seen"]["time"]

    @property
    @fetch_field('users.get', field_name="last_seen")
    def platform(self):
        """
        :return: {string, None}
        """
        platform = self._data["last_seen"].get("platform")
        platform_items = {
            1: 'mobile',
            2: 'iPhone',
            3: 'iPad',
            4: 'Android',
            5: 'Windows Phone',
            6: 'Windows 8',
            7: 'web'
        }

        return platform_items.get(platform, None)

    @property
    def list(self):
        raise NotImplementedError

    @property
    def maiden_name(self):
        raise NotImplementedError

    @property
    def military(self):
        raise NotImplementedError

    @property
    @fetch_field('users.get')
    def movies(self):
        """
        :return: string
        """
        return self._data['movies']

    @property
    @fetch_field('users.get')
    def music(self):
        """
        :return: string
        """
        return self._data['music']

    @property
    @fetch_field('users.get')
    def nickname(self):
        """
        :return: string
        """
        return self._data['nickname']

    @property
    def occupation(self):
        raise NotImplementedError

    @property
    @fetch_field('users.get', field_name="online")
    def is_online(self):
        """
        :return: bool
        """
        return bool(self._data['online'])

    @property
    def personal(self):
        raise NotImplementedError

    # photos fields

    @property
    @fetch_field('users.get')
    def quotes(self):
        """
        :return: string
        """
        return self._data['quotes']

    @property
    def relatives(self):
        raise NotImplementedError

    @property
    def relation(self):
        raise NotImplementedError

    @property
    def schools(self):
        raise NotImplementedError

    @property
    @fetch_field('users.get')
    def screen_name(self):
        """
        :return: string
        """
        return self._data['screen_name']

    @property
    @fetch_field('users.get')
    def sex(self):
        """
        :return: {string, None}
        """
        _sex = self._data['sex']
        sex_items = {
            1: 'female',
            2: 'male'
        }
        return sex_items.get(_sex, None)

    @property
    @fetch_field('users.get')
    def site(self):
        """
        :return: string
        """
        return self._data['site']

    @property
    def status(self):
        raise NotImplementedError

    @property
    def timezone(self):
        raise NotImplementedError

    @property
    @fetch_field('users.get')
    def tv(self):
        """
        :return: string
        """
        return self._data['tv']

    @property
    def universities(self):
        raise NotImplementedError

    @property
    @fetch_field('users.get', field_name="verified")
    def is_verified(self):
        """
        :return: bool
        """
        return bool(self._data['verified'])

    @property
    @fetch_field('users.get')
    def wall_comments(self):
        """
        :return: bool
        """
        return bool(self._data['wall_comments'])

    def get_friends(self):
        return Friends.get_friends(user_id=self.id)

    def get_friends_count(self):
        return Friends.get_friends_count(user_id=self.id)

    def get_wall(self):
        return Wall.get_wall(owner_id=self.id)

    def __repr__(self):
        if self.is_banned:
            return u"<User BANNED id{0}>".format(self.id)
        if self.is_deleted:
            return u"<User DELETED id{0}>".format(self.id)

        return u"<User id{0}>".format(self.id)


from .friends import Friends
