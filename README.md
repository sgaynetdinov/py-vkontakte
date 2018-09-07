[![Build Status](https://travis-ci.org/sgaynetdinov/py-vkontakte.svg?branch=master)](https://travis-ci.org/sgaynetdinov/py-vkontakte) [![Coverage Status](https://coveralls.io/repos/github/sgaynetdinov/py-vkontakte/badge.svg?branch=master)](https://coveralls.io/github/sgaynetdinov/py-vkontakte?branch=master) ![N|Solid](https://img.shields.io/pypi/l/py-vkontakte.svg) ![N|Solid](https://img.shields.io/pypi/wheel/py-vkontakte.svg) ![N|Solid](https://img.shields.io/pypi/pyversions/py-vkontakte.svg)

# Table of contents

- [Install](#install)
- [Method](#method)
  - [User](#user)
  - [Group](#group)



# Install

```sh
pip install py-vkontakte
```

# First start

```python
>>> import vk
>>> api = vk.Api('YOUR_TOKEN')
```

# User

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

# Group

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

# Update PyPi

```sh
python3 setup.py sdist
python3 setup.py bdist_wheel --universal
twine upload dist/*
```