Install
=======

::

    pip install py-vkontakte

Usage
=====

.. code-block:: python

    from vk.users import get_users

    user = get_users('durov')[0]
    print(user.first)

Create and use ACCESS_TOKEN
===============================

.. code-block:: python

    import vk

    client_id = <YOUR_CLIENT_ID>
    redirect_uri = <REDIRECT_URI>
    vk.create_url_get_code(client_id, redirect_uri)  # `code`

    client_secret = <YOUR_CLIENT_SECRET>
    code = <YOUR_CODE>
    access_token = vk.create_access_token(client_id, client_secret, redirect_uri, code)
    vk.set_access_token(access_token)
