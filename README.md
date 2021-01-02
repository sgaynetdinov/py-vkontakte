# py-vkontakte — Python client for API vk.com

**Build** | ![](https://github.com/sgaynetdinov/py-vkontakte/workflows/unittest/badge.svg) [![codecov](https://codecov.io/gh/sgaynetdinov/py-vkontakte/branch/master/graph/badge.svg)](https://codecov.io/gh/sgaynetdinov/py-vkontakte) [![Total alerts](https://img.shields.io/lgtm/alerts/g/sgaynetdinov/py-vkontakte.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/sgaynetdinov/py-vkontakte/alerts/)
:---   | :---  
**Package** | ![GitHub release](https://img.shields.io/github/release/sgaynetdinov/py-vkontakte.svg) ![Solid](https://img.shields.io/pypi/pyversions/py-vkontakte.svg) ![Solid](https://img.shields.io/pypi/wheel/py-vkontakte.svg)


### Table of contents

- [Install](#install)
- [First start](#first-start)
- [Method](#method)
  - [User](#user)
  - [UserCareer](#usercareer)
  - [Group](#group)
- [Examples](#examples)
- [Run tests](#run-tests)


### Install

```sh
pip install py-vkontakte
```

### First start

```python
>>> import vk
>>> api = vk.Api('YOUR_TOKEN')
```

### Method

#### User
```python
# Single user
>>> user = api.get_user('durov')

# Many user
>>> user_items = api.get_users([1, 'sgaynetdinov'])  # Return generator
>>> [user.id for user in user_items]
[1, 23768217]

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
>>> user.can_write_private_message  # False
>>> user.is_friend  # False

>>> user.get_about()
>>> user.get_activities()
>>> user.get_books()
>>> user.get_career()
>>> user.get_games()
>>> user.get_movies()
>>> user.get_music()
>>> user.get_quotes()
>>> user.get_tv()
```


#### UserCareer
```python
# Get user career data
>>> career = user.get_career()

# Career object
>>> career[0].group
>>> career[0].company
>>> career[0].country
>>> career[0].city
>>> career[0].city_name
>>> career[0].start
>>> career[0].end
>>> career[0].position
```


#### Group

```python
# Single group
>>> group = api.get_group('devclub')

# Checking a user is a member of a current group
>>> user = api.get_user('durov')
>>> user in group  # or user.id in group

>>> user_items = [user for user in group.get_members()] # Get group members
>>> user_id_items = [user_id for user_id in group.get_members_only_id()] # Get only group members ID

# Many group
>>> groups_items = api.get_groups([1, 'devclub'])  # Return generator
>>> [group for group in groups_items]
[<Group: apiclub>, <Group: devclub>]
```

### Examples

```python
>>> import vk
>>> api = vk.Api('YOUR_TOKEN')
>>> group = api.get_group('devclub')
>>> user_id_items = []
>>> for user in group.get_members():
...     if user.is_friend and user.is_online:
...     	user_id_items.append(user.id)
```

### Run tests

```
pip install -r requirements-dev.txt
pytest
```
