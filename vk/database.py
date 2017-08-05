# coding=utf-8
from .base import VKBase


class Country(VKBase):
    """
    https://vk.com/dev/database.getCountriesById
    """
    __slots__ = ('id', 'title', '_session')

    @classmethod
    def from_json(cls, session, json_obj):
        country = cls()
        country.id = json_obj.get('id')
        country.title = json_obj.get('title')
        country._session = session
        return country

    @staticmethod
    def _get_country_by_id(session, country_id):
        country_json = session.fetch('database.getCountriesById', country_ids=country_id)[0]
        return Country.from_json(session, country_json)


class City(VKBase):
    """
    https://vk.com/dev/database.getCitiesById
    """
    __slots__ = ('id', 'title', '_session')

    @classmethod
    def from_json(cls, session, json_obj):
        city = cls()
        city.id = json_obj.get('id')
        city.title = json_obj.get('title')
        city._session = session
        return city

    @staticmethod
    def _get_city_by_id(session, city_id):
        city_json = session.fetch('database.getCitiesById', city_ids=city_id)[0]
        return City.from_json(session, city_json)
