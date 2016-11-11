# coding=utf-8
from .fetch import fetch


def getCountriesById(country_id):
    """
    https://vk.com/dev/database.getCountriesById
    """
    country_items_json = fetch('database.getCountriesById', country_ids=country_id)
    country_json = country_items_json[0]
    return country_json['title']


def getCitiesById(city_id):
    """
    https://vk.com/dev/database.getCities
    """
    city_json = fetch('database.getCitiesById', city_ids=city_id)[0]
    return city_json['title']
