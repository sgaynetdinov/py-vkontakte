import datetime

from .base import VKBase
from .database import City, Country
from .friends import Friends
from .wall import Wall


class User(VKBase):
    """
    https://vk.com/dev/objects/user
    """
    USER_FIELDS = (
        'bdate',
        'connections',
        'domain',
        'sex',
        'maiden_name',
        'nickname',
        'verified',
        'last_seen',
        'platform',
        'status',
        'trending',
        'site',
        'relation',
        'is_friend'
    )

    @classmethod
    def from_json(cls, session, json_obj):
        user = cls()
        user.id = json_obj.get('id')
        user.first_name = json_obj.get('first_name')
        user.last_name = json_obj.get('last_name')
        user.maiden_name = json_obj.get('maiden_name')
        user.nickname = json_obj.get('nickname')
        user.bdate = json_obj.get('bdate')
        user.sex = cls._sex(json_obj.get('sex'))
        user.status = cls._status(json_obj)
        user.site = json_obj.get('site')
        user.relation = cls._relation(json_obj)
        user.relation_partner = cls._relation_partner(json_obj)
        user.is_friend = bool(json_obj.get('is_friend'))

        user.facebook = json_obj.get('facebook')
        user.skype = json_obj.get('skype')
        user.twitter = json_obj.get('twitter')
        user.livejournal = json_obj.get('livejournal')
        user.instagram = json_obj.get('instagram')

        user.is_verified = bool(json_obj.get('verified'))
        user.is_trending = bool(json_obj.get('trending'))
        user.domain = json_obj.get('domain')
        user.screen_name = user.domain
        user.last_seen = cls._last_seen(json_obj.get('last_seen'))
        user.platform = cls._platform(json_obj.get('last_seen'))

        user.is_deactivated = bool(json_obj.get('deactivated'))
        user.is_deleted = bool(json_obj.get('deactivated') == 'deleted')
        user.is_banned = bool(json_obj.get('deactivated') == 'banned')

        user.can_write_private_message = bool(json_obj.get('can_write_private_message'))

        user._session = session

        return user

    def get_about(self):
        response = self._fetch("about")[0]
        return response.get('about')

    def get_activities(self):
        response = self._fetch("activities")[0]
        return response.get('activities')

    def get_books(self):
        response = self._fetch("books")[0]
        return response.get('books')

    def get_career(self):
        response = self._fetch("career")[0]
        if response.get('career'):
            return [UserCareer.from_json(self._session, i) for i in response.get('career')]
        return []

    def get_city(self):
        response = self._session.fetch("users.get", user_ids=self.id, fields="city")[0]
        if response.get('city'):
            return City.from_json(self._session, response.get('city'))

    def get_country(self):
        response = self._session.fetch("users.get", user_ids=self.id, fields="country")[0]
        if response.get('country'):
            return Country.from_json(self._session, response.get('country'))

    @classmethod
    def _status(cls, user_json):
        return user_json.get('status', '')

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
        if last_seen and 'time' in last_seen:
            time = last_seen.get('time')
            return datetime.datetime.utcfromtimestamp(time)

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

    @classmethod
    def _relation(cls, user_json):
        if 'relation' not in user_json:
            return None

        index = user_json['relation']

        relation = {
            0: None,
            1: 'single',
            2: 'in a relationship',
            3: 'engaged',
            4: 'married',
            5: 'it\'s complicated',
            6: 'actively searching',
            7: 'in love',
            8: 'in a civil union'
        }

        return relation.get(index)

    @classmethod
    def _relation_partner(cls, user_json):
        if 'relation_partner' not in user_json:
            return None

        return user_json['relation_partner']['id']

    def get_games(self):
        response = self._fetch("games")[0]
        return response.get('games')

    def get_followers(self):
        """
        https://vk.com/dev/users.getFollowers
        """
        return self._session.fetch_items(
            "users.getFollowers",
            self.from_json,
            self._session,
            count=1000,
            user_id=self.id,
            fields=self.USER_FIELDS,
        )

    def get_followers_count(self):
        response = self._session.fetch("users.get", user_ids=self.id, fields="followers_count")[0]
        return response.get('followers_count')

    def get_friends(self):
        raw_user_items = Friends._get_friends(self._session, user_id=self.id)
        return User._get_users(self._session, raw_user_items)

    def get_friends_count(self):
        return Friends._get_friends_count(self._session, user_id=self.id)

    def get_military(self):
        response = self._session.fetch("users.get", user_ids=self.id, fields="military")[0]
        if response.get('military'):
            return [UserMilitary.from_json(self._session, json_military) for json_military in response.get('military')]
        return []

    def get_movies(self):
        response = self._fetch("movies")[0]
        return response.get('movies')

    def get_music(self):
        response = self._fetch("music")[0]
        return response.get('music')

    def get_occupation(self):
        response = self._session.fetch("users.get", user_ids=self.id, fields="occupation")[0]
        if response.get('occupation'):
            return UserOccupation.from_json(self._session, response.get('occupation'))
        return None

    @property
    def is_online(self):
        response = self._session.fetch("users.get", user_ids=self.id, fields="online")[0]
        return bool(response.get('online'))

    def get_personal(self):
        raise NotImplementedError

    def get_photos(self):
        PHOTOS_FIELDS = "photo_50", "photo_100", "photo_200_orig", "photo_200", "photo_400_orig"
        response = self._session.fetch("users.get", user_ids=self.id, fields=",".join(PHOTOS_FIELDS))[0]
        return {key: value for key, value in response.items() if key in PHOTOS_FIELDS}

    def get_quotes(self):
        response = self._fetch("quotes")[0]
        return response.get('quotes')

    def get_relatives(self):
        response = self._session.fetch("users.get", user_ids=self.id, fields="relatives")[0]
        return response.get('relatives')

    def get_schools(self):
        response = self._session.fetch("users.get", user_ids=self.id, fields="schools")[0]
        if response.get('schools'):
            return [UserSchool.from_json(self._session, school_json) for school_json in response.get('schools')]
        return []

    def get_tv(self):
        response = self._fetch("tv")[0]
        return response.get('tv')

    def get_universities(self):
        response = self._session.fetch("users.get", user_ids=self.id, fields="universities")[0]
        if response.get('universities'):
            return [UserUniversity.from_json(self._session, university_json) for university_json in response.get('universities')]
        return []

    def get_walls(self):
        return Wall._get_walls(self._session, owner_id=self.id)

    def get_wall(self, wall_id):
        return Wall._get_wall(self._session, self.id, wall_id)

    def get_walls_count(self):
        return Wall._get_walls_count(self._session, owner_id=self.id)

    def get_groups(self, filter=None):
        from .groups import Group
        return Group._get_user_groups(self._session, self.id, filter=filter)

    @staticmethod
    def _get_user(session, slug_or_user_id):
        """
        :param slug_or_user_id: str or int
        :return: User
        """
        user_json_items = session.fetch('users.get', user_ids=slug_or_user_id, fields=User.USER_FIELDS)
        return User.from_json(session, user_json_items[0])

    @staticmethod
    def _get_users(session, user_ids):
        if not user_ids:
            raise StopIteration

        for user_id_items in grouper(user_ids, 300):
            if not user_id_items:
                raise StopIteration

            user_id_items_str_inline = ",".join(str(i) for i in user_id_items)
            user_json_items = session.fetch('users.get', user_ids=user_id_items_str_inline, fields=User.USER_FIELDS)
            yield from [
                User.from_json(session, user_json) for user_json in user_json_items
            ]

    def _fetch(self, fields):
        return self._session.fetch("users.get", user_ids=self.id, fields=fields)


def grouper(iterable, n):
    """
    grouper([0,1,2,3,4], 3) --> [(0,1,2), (3,4)]
    """
    for i in range(0, len(iterable), n):
        yield iterable[i:i+n]


class UserCareer(VKBase):
    @classmethod
    def from_json(cls, session, json_obj):
        career = cls()
        career.group = json_obj.get("group_id")
        career.company = json_obj.get("company")
        career.country = json_obj.get("country_id")
        career.city = json_obj.get("city_id")
        career.city_name = json_obj.get("city_name")
        career.start = json_obj.get("from")
        career.end = json_obj.get("until")
        career.position = json_obj.get("position")
        career._session = session
        return career

    @property
    def id(self):
        if self.group is not None:
            return self.group
        else:
            return hash(self.company)


class UserMilitary(VKBase):
    __slots__ = ('unit', 'unit_id', 'country_id', 'start', 'finish', '_session')

    @classmethod
    def from_json(cls, session, military_json):
        military = cls()
        military.unit = military_json.get('unit')
        military.unit_id = military_json.get('unit_id')
        military.country_id = military_json.get('country_id')
        military.start = military_json.get('from')
        military.finish = military_json.get('until')
        military._session = session
        return military


class UserOccupation(VKBase):
    __slots__ = ('type', 'id', 'name', '_session')

    @classmethod
    def from_json(cls, session, occupation_json):
        occupation = cls()
        occupation.type = occupation_json.get('type')
        occupation.id = occupation_json.get('id')
        occupation.name = occupation_json.get('name')
        occupation._session = session
        return occupation


class UserSchool(VKBase):
    __slots__ = ('id', 'country', 'city', 'name', 'year_start', 'year_finish', 'year_graduated', 'class_letter', 'speciality', 'type', 'type_str', '_session')

    @classmethod
    def from_json(cls, session, school_json):
        school = cls()
        school.id = school_json.get("id")
        school.country = Country._get_country_by_id(session, school_json.get("country"))
        school.city = City._get_city_by_id(session, school_json.get("city"))
        school.name = school_json.get("name")
        school.year_start = school_json.get("year_from")
        school.year_finish = school_json.get("year_to")
        school.year_graduated = school_json.get("year_graduated")
        school.class_letter = school_json.get('class')
        school.speciality = school_json.get("speciality")
        school.type = school_json.get("type")
        school.type_str = school_json.get("type_str")
        school._session = session
        return school


class UserUniversity(VKBase):
    __slots__ = ('id', 'country', 'city', 'name', 'faculty', 'faculty_name', 'chair', 'chair_name', 'graduation', 'education_form', 'education_status', '_session')

    @classmethod
    def from_json(cls, session, university_json):
        university = cls()
        university.id = university_json.get("id")
        university.country = Country._get_country_by_id(session, university_json.get("country"))
        university.city = City._get_city_by_id(session, university_json.get("city"))
        university.name = university_json.get("name")
        university.faculty = university_json.get("faculty")
        university.faculty_name = university_json.get("faculty_name")
        university.chair = university_json.get("chair")
        university.chair_name = university_json.get("chair_name")
        university.graduation = university_json.get("graduation")
        university.education_form = university_json.get("education_form")
        university.education_status = university_json.get("education_status")
        university._session = session
        return university
