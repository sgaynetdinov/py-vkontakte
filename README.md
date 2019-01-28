# py-vkontakte — Python client for API vk.com

**Build** | [![Build Status](https://travis-ci.org/sgaynetdinov/py-vkontakte.svg?branch=master)](https://travis-ci.org/sgaynetdinov/py-vkontakte) [![codecov](https://codecov.io/gh/sgaynetdinov/py-vkontakte/branch/master/graph/badge.svg)](https://codecov.io/gh/sgaynetdinov/py-vkontakte)
:---   | :---  
**Package** | ![GitHub release](https://img.shields.io/github/release/sgaynetdinov/py-vkontakte.svg) ![Solid](https://img.shields.io/pypi/pyversions/py-vkontakte.svg) ![Solid](https://img.shields.io/pypi/wheel/py-vkontakte.svg)


### Table of contents

- [Install](#install)
- [First start](#first-start)
- [Method](#method)
  - [User](#user)
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
# return single User object
>>> api.get_user('durov')
<User: durov>
```

```python
# yield one or many User objects
>>> user_items = api.get_users([1, 's.gaynetdinov'])
>>> [user.id for user in user_items]
[1, 23768217]
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
