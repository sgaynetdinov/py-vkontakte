![N|Solid](https://img.shields.io/pypi/l/py-vkontakte.svg) ![N|Solid](https://img.shields.io/pypi/wheel/py-vkontakte.svg) ![N|Solid](https://img.shields.io/pypi/pyversions/py-vkontakte.svg)

# Install

```sh
pip install py-vkontakte
```

# User

```python
>>> import vk
>>> vk.get_user('durov')  # return single User object
<User: durov>
>>> user_items = vk.get_users([1, 's.gaynetdinov'])  # yield one or many User objects
>>> [user.id for user in user_items]
[1, 23768217]
```

| User object | - |
| ----------- | - |
| `User.id` | id |
| `User.first_name` | First name |
| `User.last_name` | Last name |
| `User.maiden_name` | Maiden name |
| `User.nickname` | Nickname |
| `User.is_deactivated` | *True* or *False* |
| `User.is_deleted` | *True* or *False* |
| `User.is_banned` | *True* or *False* |
| `User.is_hidden` | *True* or *False* |
| `User.domain` | domain |
| `User.screen_name` | screen_name |
| `User.bdate` | bdate |
| `User.sex` | *female*, *male* or *None* |
| `User.is_verified` | is_verified |
| `User.last_seen` | last_seen |
| `User.platform` | platform |
| `User.get_about()` | get_about |
| `User.get_activities()` | get_activities |
| `User.get_books()` | get_books |
| `User.get_career()` | get_career |
| `User.get_city()` | get_city |
| `User.get_country()` | get_country |
| `User.get_games()` | get_games |
| `User.get_followers_count()` | get_followers_count |
| `User.get_friends()` | get_friends |
| `User.get_friends_count()` | get_friends_count |
| `User.get_military()` | get_military |
| `User.get_movies()` | get_movies |
| `User.get_music()` | get_music |
| `User.get_occupation()` | get_occupation |
| `User.is_online` | is_online |
| `User.get_personal()` | get_personal |
| `User.get_photos()` | get_photos |
| `User.get_quotes()` | get_quotes |
| `User.get_relatives()` | get_relatives |
| `User.get_schools()` | get_schools |
| `User.get_site()` | get_site |
| `User.get_status()` | get_status |
| `User.get_tv()` | get_tv |
| `User.get_universities()` | get_universities |
| `User.get_walls()` | yield `Wall` object |
| `User.get_wall(wall_id)` | return `Wall` object |
| `User.get_wall_count()` | return count `Wall` in current user |
| `User.get_groups()` | yield `Group` |

# Group

```python
>>> import vk
>>> groups_items = vk.groups([1, 'devclub'])  # return generator
>>> [group for group in groups_items]
[<Group apiclub>, <Group devclub>]
```

# Access token

```python
>>> import vk
>>> vk.set_access_token('YOUR_ACCESS_TOKEN')
```


# Update PyPi

```sh
python3 setup.py sdist
python3 setup.py bdist_wheel --universal
twine upload dist/*
```