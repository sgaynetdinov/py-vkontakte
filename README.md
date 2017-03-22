![N|Solid](https://img.shields.io/pypi/l/py-vkontakte.svg) ![N|Solid](https://img.shields.io/pypi/wheel/py-vkontakte.svg) ![N|Solid](https://img.shields.io/pypi/pyversions/py-vkontakte.svg)

# Install

```sh
pip install py-vkontakte
```

# Simple usage

```python
import vk
user = vk.get_user('durov')
print(user.first_name)
```

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