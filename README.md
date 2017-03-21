![N|Solid](https://img.shields.io/pypi/l/py-vkontakte.svg) ![N|Solid](https://img.shields.io/pypi/wheel/py-vkontakte.svg) ![N|Solid](https://img.shields.io/pypi/pyversions/py-vkontakte.svg)

# Install

```sh
pip install py-vkontakte
```

### Simple usage

```python
import vk
user = vk.get_user('durov')
print(user.first_name)
```

### Group

```python
>>> import vk
>>> vk.groups([1, 'devclub'])
```

### Access token

```python
>>> import vk
>>> vk.set_access_token('YOUR_ACCESS_TOKEN')
```