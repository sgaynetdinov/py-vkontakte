Install
=======

::

    pip install py-vkontakte

Usage
=====

.. code-block:: python

    import vk

    user = vk.get_user('durov')
    print(user.first_name)

Create and use ACCESS_TOKEN
===============================

.. code-block:: python

    import vk
    vk.create_url_get_code(<YOUR_CLIENT_ID>, <REDIRECT_URI>)  # `code`

    access_token = vk.create_access_token(<YOUR_CLIENT_ID>, <YOUR_CLIENT_SECRET>, <REDIRECT_URI>, <YOUR_CODE>)
    vk.set_access_token(access_token)
