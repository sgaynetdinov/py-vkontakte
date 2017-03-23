# coding=utf-8
try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest

from .base import VKObject
from .database import City, Country
from .fetch import fetch
from .wall import Wall

__all__ = ["get_user", "get_users"]


def grouper(iterable, n):
    """
    grouper([0,1,2,3,4], 3) --> [(0,1,2), (3,4)]
    https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    args = [iter(iterable)] * n
    grouper_items = list(zip_longest(*args))

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
    user_json_items = fetch('users.get', user_ids=slug_or_user_id, fields=User.USER_FIELDS)
    return User.from_json(user_json_items[0])


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


class User(VKObject):
    """
    Docs: https://vk.com/dev/objects/user
    """
    USER_FIELDS = ('bdate', 'domain', 'sex',
                   'maiden_name', 'nickname', 'verified', 'last_seen', 'platform')

    __slots__ = ('id', 'first_name', 'last_name', 'is_deactivated', 'is_deleted', 'is_banned', 'is_hidden', 'bdate', 'domain', 'screen_name', 'sex',
                 'maiden_name', 'nickname', 'is_verified')

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

        user.domain = json_obj.get('domain')
        user.screen_name = user.domain

        user.bdate = json_obj.get('bdate')
        user.sex = cls._sex(json_obj.get('sex'))
        user.is_verified = bool(json_obj.get('verified'))
        user.last_seen = cls._last_seen(json_obj.get('last_seen'))
        user.platform = cls._platform(json_obj.get('last_seen'))

        return user

    @classmethod
    def from_json_items(cls, user_json_items):
        return (cls.from_json(user_json) for user_json in user_json_items)

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

    @classmethod
    def _last_seen(cls, last_seen):
        if last_seen:
            return last_seen.get('time')
        return None

    @classmethod
    def _platform(cls, last_seen):
        if not last_seen:
            return None
        platform_id = last_seen.get('platform')

        platform = {
            1: "m.vk.com",
            2: "iPhone app",
            3: "iPad app",
            4: "Android app",
            5: "Windows Phone app",
            6: "Windows 8 app",
            7: "web (vk.com)"
        }
        return platform.get(platform_id)

    def get_games(self):
        response = fetch("users.get", user_ids=self.id, fields="games")[0]
        return response.get('games')

    def get_followers_count(self):
        response = fetch("users.get", user_ids=self.id, fields="followers_count")[0]
        return response.get('followers_count')

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

    @property
    def is_online(self):
        response = fetch("users.get", user_ids=self.id, fields="online")[0]
        return bool(response.get('online'))

    def get_personal(self):
        raise NotImplementedError

    def get_photos(self):
        PHOTOS_FIELDS = "photo_50", "photo_100", "photo_200_orig", "photo_200", "photo_400_orig"
        response = fetch("users.get", user_ids=self.id, fields=",".join(PHOTOS_FIELDS))[0]
        return {key: value for key, value in response.items() if key in PHOTOS_FIELDS}

    def get_quotes(self):
        response = fetch("users.get", user_ids=self.id, fields="quotes")[0]
        return response.get('quotes')

    def get_relatives(self):
        response = fetch("users.get", user_ids=self.id, fields="relatives")[0]
        return response.get('relatives')

    def get_schools(self):
        response = fetch("users.get", user_ids=self.id, fields="schools")[0]
        if response.get('schools'):
            return [UserSchool.from_json(school_json) for school_json in response.get('schools')]
        return []

    def get_site(self):
        response = fetch("users.get", user_ids=self.id, fields="site")[0]
        return response.get('site')

    def get_status(self):
        response = fetch("users.get", user_ids=self.id, fields="status")[0]
        return response.get('status')

    def get_tv(self):
        response = fetch("users.get", user_ids=self.id, fields="tv")[0]
        return response.get('tv')

    def get_universities(self):
        response = fetch("users.get", user_ids=self.id, fields="universities")[0]
        if response.get('universities'):
            return [UserUniversity.from_json(university_json) for university_json in response.get('universities')]
        return []

    def get_walls(self):
        return Wall.get_walls(owner_id=self.id)

    def get_wall_by_id(self, wall_id):
        return Wall.get_wall_by_id(self.id, wall_id)

    def get_wall_count(self):
        return Wall.get_wall_count(owner_id=self.id)

    def get_groups(self, filter=None):
        from .groups import Group
        return Group.get_user_groups(self.id, filter=filter)

    def __hash__(self):
        class_name = type(self).__name__
        return hash(class_name) ^ hash(self.id)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        raise NotImplementedError


class UserCareer(VKObject):
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
            from .groups import groups
            return groups(group_id)[0]


class UserMilitary(VKObject):
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


class UserOccupation(VKObject):
    __slots__ = ('type', 'id', 'name')

    @classmethod
    def from_json(cls, occupation_json):
        occupation = cls()
        occupation.type = occupation_json.get('type')
        occupation.id = occupation_json.get('id')
        occupation.name = occupation_json.get('name')
        return occupation


class UserSchool(VKObject):
    __slots__ = ('id', 'country', 'city', 'name', 'year_start', 'year_finish', 'year_graduated', 'class_letter', 'speciality', 'type', 'type_str')

    @classmethod
    def from_json(cls, school_json):
        school = cls()
        school.id = school_json.get("id")
        school.country = Country.get_country_by_id(school_json.get("country"))
        school.city = City.get_city_by_id(school_json.get("city"))
        school.name = school_json.get("name")
        school.year_start = school_json.get("year_from")
        school.year_finish = school_json.get("year_to")
        school.year_graduated = school_json.get("year_graduated")
        school.class_letter = school_json.get('class')
        school.speciality = school_json.get("speciality")
        school.type = school_json.get("type")
        school.type_str = school_json.get("type_str")
        return school


class UserUniversity(VKObject):
    __slots__ = ('id', 'country', 'city', 'name', 'faculty', 'faculty_name', 'chair', 'chair_name', 'graduation', 'education_form', 'education_status')

    @classmethod
    def from_json(cls, university_json):
        university = cls()
        university.id = university_json.get("id")
        university.country = Country.get_country_by_id(university_json.get("country"))
        university.city = City.get_city_by_id(university_json.get("city"))
        university.name = university_json.get("name")
        university.faculty = university_json.get("faculty")
        university.faculty_name = university_json.get("faculty_name")
        university.chair = university_json.get("chair")
        university.chair_name = university_json.get("chair_name")
        university.graduation = university_json.get("graduation")
        university.education_form = university_json.get("education_form")
        university.education_status = university_json.get("education_status")
        return university


from .friends import Friends
