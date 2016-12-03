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
        raise StopIteration

    for user_id_items in grouper(user_ids, 300):
        if not user_id_items:
            raise StopIteration

        user_id_items_str_inline = ",".join([str(i) for i in user_id_items])
        user_json_items = fetch('users.get', user_ids=user_id_items_str_inline, fields=User.USER_FIELDS)
        for user in [User.from_json(user_json) for user_json in user_json_items]:
            yield user


class User(object):
    """
    Docs: https://vk.com/dev/objects/user
    """
    USER_FIELDS = ('bdate', 'domain', 'sex',
                   'maiden_name', 'nickname', 'online')
    __slots__ = ('id', 'first_name', 'last_name', 'is_deactivated', 'is_deleted', 'is_banned', 'is_hidden', 'bdate', 'domain', 'sex',
                 'maiden_name', 'nickname', 'is_online')

    @classmethod
    def from_json(cls, json_obj):
        user = cls()
        user.id = json_obj.get('id')
        user.first_name = json_obj.get('first_name')
        user.last_name = json_obj.get('last_name')
        user.maiden_name = json_obj.get('maiden_name')
        user.nickname = json_obj.get('nickname')

        user.is_deactivated = bool(json_obj.get('deactivated'))
        user.is_deleted = bool(json_obj.get('deactivated') == 'deleted')
        user.is_banned = bool(json_obj.get('deactivated') == 'banned')
        user.is_hidden = bool(json_obj.get('hidden'))

        user.bdate = json_obj.get('bdate')
        user.domain = json_obj.get('domain')
        user.sex = cls._sex(json_obj.get('sex'))
        user.is_online = bool(json_obj.get('online'))

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

    @classmethod
    def _sex(cls, sex):
        """
        :param sex: {integer}
        :return: {string, None}
        """
        sex_items = {
            1: 'female',
            2: 'male'
        }
        return sex_items.get(sex)

    def get_friends(self):
        return Friends.get_friends(user_id=self.id)

    def get_friends_count(self):
        return Friends.get_friends_count(user_id=self.id)

    def get_military(self):
        response = fetch("users.get", user_ids=self.id, fields="military")[0]
        if response.get('military'):
            return [UserMilitary.from_json(json_military) for json_military in response.get('military')]
        return []

    def get_movies(self):
        response = fetch("users.get", user_ids=self.id, fields="movies")[0]
        return response.get('movies')

    def get_music(self):
        response = fetch("users.get", user_ids=self.id, fields="music")[0]
        return response.get('music')

    def get_occupation(self):
        response = fetch("users.get", user_ids=self.id, fields="occupation")[0]
        if response.get('occupation'):
            return UserOccupation.from_json(response.get('occupation'))
        return None

    def get_photos(self):
        PHOTOS_FIELDS = "photo_50", "photo_100", "photo_200_orig", "photo_200", "photo_400_orig"
        response = fetch("users.get", user_ids=self.id, fields=",".join(PHOTOS_FIELDS))[0]
        return {key: value for key, value in response.items() if key in PHOTOS_FIELDS}

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


class UserMilitary(object):
    __slots__ = ('unit', 'unit_id', 'country_id', 'start', 'finish')

    @classmethod
    def from_json(cls, military_json):
        military = cls()
        military.unit = military_json.get('unit')
        military.unit_id = military_json.get('unit_id')
        military.country_id = military_json.get('country_id')
        military.start = military_json.get('from')
        military.finish = military_json.get('until')
        return military

    def __repr__(self):
        return u"<Military: {0}>".format(self.unit_id)


class UserOccupation(object):
    __slots__ = ('type', 'id', 'name')

    @classmethod
    def from_json(cls, occupation_json):
        occupation = cls()
        occupation.type = occupation_json.get('type')
        occupation.id = occupation_json.get('id')
        occupation.name = occupation_json.get('name')
        return occupation

    def __repr__(self):
        return u"<Occupation: {0}>".format(self.type)


from .groups import groups
from .friends import Friends
