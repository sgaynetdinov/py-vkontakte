# coding=utf-8
import itertools

from .database import City, Country
from .fetch import fetch, fetch_field
from .wall import Wall

__all__ = ["get_user"]


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
        user_json_items = fetch('users.get', user_ids=slug_or_user_id, fields=User.USER_FIELDS)
        return User.from_json(user_json_items[0])
    raise ValueError


def get_users(user_ids):
    if not user_ids:
        return []

    user_items = []
    for u_ids in grouper(user_ids, 300):
        _user_ids = ",".join([str(i) for i in u_ids])
        user_items.append(fetch('users.get', user_ids=_user_ids, fields=User.USER_FIELDS))
    return [User.from_json(user_json) for user_json in sum(user_items, [])]


class User(object):
    """
    Docs: https://vk.com/dev/objects/user
    """
    USER_FIELDS = ('id', 'first_name', 'last_name', 'is_deactivated', 'is_deleted', 'is_banned', 'is_hidden', 'bdate')
    __slots__ = USER_FIELDS

    @classmethod
    def from_json(cls, json_obj):
        user = cls()
        user.id = json_obj.get('id')
        user.first_name = json_obj.get('first_name')
        user.last_name = json_obj.get('last_name')

        user.is_deactivated = bool(json_obj.get('deactivated'))
        user.is_deleted = bool(json_obj.get('deactivated') == 'deleted')
        user.is_banned = bool(json_obj.get('deactivated') == 'banned')
        user.is_hidden = bool(json_obj.get('hidden'))

        user.bdate = json_obj.get('bdate')

        return user

    def get_about(self):
        response = fetch("users.get", user_ids=self.id, fields="about")[0]
        return response.get('about')

    def get_activities(self):
        response = fetch("users.get", user_ids=self.id, fields="activities")[0]
        return response.get('activities')

    def get_books(self):
        response = fetch("users.get", user_ids=self.id, fields="books")[0]
        return response.get('books')

    def get_career(self):
        response = fetch("users.get", user_ids=self.id, fields="career")[0]
        if response.get('career'):
            return [UserCareer.from_json(i) for i in response.get('career')]
        return []

    def get_city(self):
        """
        :return: City or None
        """
        response = fetch("users.get", user_ids=self.id, fields="city")[0]
        if response.get('city'):
            return City.from_json(response.get('city'))

    def get_country(self):
        """
        :return: Country or None
        """
        response = fetch("users.get", user_ids=self.id, fields="country")[0]
        if response.get('country'):
            return Country.from_json(response.get('country'))

    # @property
    # @fetch_field('users.get')
    # def domain(self):
    #     """
    #     :return: string
    #     """
    #     return self._data['domain']

    @property
    def education(self):
        raise NotImplementedError

    @property
    def exports(self):
        raise NotImplementedError

    # first_name_{case}

    # @property
    # @fetch_field('users.get')
    # def followers_count(self):
    #     """
    #     :return: integer
    #     """
    #     return self._data['followers_count']

    @property
    def friend_status(self):
        raise NotImplementedError

    # @property
    # @fetch_field('users.get')
    # def games(self):
    #     """
    #     :return: string
    #     """
    #     return self._data['games']

    # @property
    # @fetch_field('users.get')
    # def has_mobile(self):
    #     """
    #     :return: bool
    #     """
    #     return bool(self._data['has_mobile'])

    # @property
    # @fetch_field('users.get')
    # def has_photo(self):
    #     """
    #     :return: bool
    #     """
    #     return bool(self._data['has_photo'])

    # @property
    # @fetch_field('users.get')
    # def home_town(self):
    #     """
    #     :return: string
    #     """
    #     return self._data['home_town']
    #
    # @property
    # @fetch_field('users.get')
    # def interests(self):
    #     """
    #     :return: string
    #     """
    #     return self._data['interests']

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

    # @property
    # @fetch_field('users.get')
    # def last_seen(self):
    #     """
    #     :return: unix-time
    #     """
    #     return self._data["last_seen"]["time"]
    #
    # @property
    # @fetch_field('users.get', field_name="last_seen")
    # def platform(self):
    #     """
    #     :return: {string, None}
    #     """
    #     platform = self._data["last_seen"].get("platform")
    #     platform_items = {
    #         1: 'mobile',
    #         2: 'iPhone',
    #         3: 'iPad',
    #         4: 'Android',
    #         5: 'Windows Phone',
    #         6: 'Windows 8',
    #         7: 'web'
    #     }
    #
    #     return platform_items.get(platform, None)

    @property
    def list(self):
        raise NotImplementedError

    @property
    def maiden_name(self):
        raise NotImplementedError

    @property
    def military(self):
        raise NotImplementedError

    # @property
    # @fetch_field('users.get')
    # def movies(self):
    #     """
    #     :return: string
    #     """
    #     return self._data['movies']
    #
    # @property
    # @fetch_field('users.get')
    # def music(self):
    #     """
    #     :return: string
    #     """
    #     return self._data['music']
    #
    # @property
    # @fetch_field('users.get')
    # def nickname(self):
    #     """
    #     :return: string
    #     """
    #     return self._data['nickname']
    #
    # @property
    # def occupation(self):
    #     raise NotImplementedError
    #
    # @property
    # @fetch_field('users.get', field_name="online")
    # def is_online(self):
    #     """
    #     :return: bool
    #     """
    #     return bool(self._data['online'])

    @property
    def personal(self):
        raise NotImplementedError

    # photos fields

    # @property
    # @fetch_field('users.get')
    # def quotes(self):
    #     """
    #     :return: string
    #     """
    #     return self._data['quotes']

    @property
    def relatives(self):
        raise NotImplementedError

    @property
    def relation(self):
        raise NotImplementedError

    @property
    def schools(self):
        raise NotImplementedError
    #
    # @property
    # @fetch_field('users.get')
    # def screen_name(self):
    #     """
    #     :return: string
    #     """
    #     return self._data['screen_name']
    #
    # @property
    # @fetch_field('users.get')
    # def sex(self):
    #     """
    #     :return: {string, None}
    #     """
    #     _sex = self._data['sex']
    #     sex_items = {
    #         1: 'female',
    #         2: 'male'
    #     }
    #     return sex_items.get(_sex, None)

    # @property
    # @fetch_field('users.get')
    # def site(self):
    #     """
    #     :return: string
    #     """
    #     return self._data['site']
    #
    # @property
    # def status(self):
    #     raise NotImplementedError
    #
    # @property
    # def timezone(self):
    #     raise NotImplementedError
    #
    # @property
    # @fetch_field('users.get')
    # def tv(self):
    #     """
    #     :return: string
    #     """
    #     return self._data['tv']
    #
    # @property
    # def universities(self):
    #     raise NotImplementedError
    #
    # @property
    # @fetch_field('users.get', field_name="verified")
    # def is_verified(self):
    #     """
    #     :return: bool
    #     """
    #     return bool(self._data['verified'])
    #
    # @property
    # @fetch_field('users.get')
    # def wall_comments(self):
    #     """
    #     :return: bool
    #     """
    #     return bool(self._data['wall_comments'])
    #
    # def get_friends(self):
    #     return Friends.get_friends(user_id=self.id)
    #
    # def get_friends_count(self):
    #     return Friends.get_friends_count(user_id=self.id)
    #
    # def get_wall(self):
    #     return Wall.get_wall(owner_id=self.id)

    def __repr__(self):
        if self.is_banned:
            return u"<User BANNED id{0}>".format(self.id)
        if self.is_deleted:
            return u"<User DELETED id{0}>".format(self.id)

        return u"<User id{0}>".format(self.id)


class UserCareer(object):
    __slots__ = ('group', 'company', 'country', 'city', 'start', 'end', 'position')

    @classmethod
    def from_json(cls, json_obj):
        career = cls()
        career.group = cls._get_group(json_obj.get("group_id"))
        career.company = json_obj.get("company")
        career.country = Country.get_country_by_id(json_obj.get("country_id"))
        career.city = City.get_city_by_id(json_obj.get("city_id"))
        career.start = json_obj.get("from")
        career.end = json_obj.get("until")
        career.position = json_obj.get("position")
        return career

    @classmethod
    def _get_group(cls, group_id):
        if group_id:
            return groups(group_id)[0]

    def __repr__(self):
        career_name = self.company or self.group.screen_name
        return u"<Career: {0}>".format(career_name)


from .groups import groups
from .friends import Friends
