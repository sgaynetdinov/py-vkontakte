# py-vkontakte — Python client for API vk.com

**Build** | [![Build Status](https://travis-ci.org/sgaynetdinov/py-vkontakte.svg?branch=master)](https://travis-ci.org/sgaynetdinov/py-vkontakte) [![codecov](https://codecov.io/gh/sgaynetdinov/py-vkontakte/branch/master/graph/badge.svg)](https://codecov.io/gh/sgaynetdinov/py-vkontakte)
:---   | :---  
**Package** | ![GitHub release](https://img.shields.io/github/release/sgaynetdinov/py-vkontakte.svg) ![Solid](https://img.shields.io/pypi/pyversions/py-vkontakte.svg) ![Solid](https://img.shields.io/pypi/wheel/py-vkontakte.svg)


### Table of contents

- [Install](#install)
- [First start](#first-start)
- [Method](#method)
  - [User](#user)
  - [UserCareer](#usercareer)
  - [Group](#group)



### Install

```sh
pip install py-vkontakte
```

### First start

```python
>>> import vk
>>> api = vk.Api('YOUR_TOKEN')
```

### User
```python
>>> user = api.get_user('durov')  # single user
>>> user_items = api.get_users([1, 's.gaynetdinov'])  # many user
>>> [user.id for user in user_items]
[1, 23768217]
```

```python
# User object
>>> user.id  # 1
>>> user.first_name  # 'Павел'
>>> user.last_name  # 'Дуров'
>>> user.maiden_name  # None
>>> user.nickname  # ''
>>> user.bdate  # '10.10.1984'
>>> user.sex  # 'male'
>>> user.status  # '道德經'
>>> user.site  # 'http://t.me/durov'
>>> user.relation  # None
>>> user.relation_partner  # None
>>> user.facebook  # '501012028'
>>> user.skype  # None
>>> user.twitter  # 'durov'
>>> user.livejournal  # None
>>> user.instagram  # 'durov'
>>> user.is_verified  # True
>>> user.is_trending  # False
>>> user.domain  # 'durov'
>>> user.screen_name  # 'durov'
>>> user.last_seen  # datetime.datetime
>>> user.platform  # 'web (vk.com)'
>>> user.is_deactivated  # False
>>> user.is_deleted  # False
>>> user.is_banned  # False

>>> user.get_about()
>>> user.get_activities()
>>> user.get_books()
>>> user.get_career()  # UserCareer
>>> user.get_games()
>>> user.get_movies()
>>> user.get_music()
>>> user.get_quotes()
>>> user.get_tv()
```


### UserCareer
```python
>>> career = user.get_career()
>>> career.group
>>> career.company
>>> career.country
>>> career.city
>>> career.city_name
>>> career.start
>>> career.end
>>> career.position
```


### Group

```python
>>> groups_items = api.get_groups([1, 'devclub'])  # return generator
>>> [group for group in groups_items]
[<Group: apiclub>, <Group: devclub>]
```

```python
# checking a user is a member of a current group
>>> user = api.get_user('durov')
>>> group = api.get_group('telegram')
>>> user in group
```
