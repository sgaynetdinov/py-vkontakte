#!/usr/bin/env python
from setuptools import setup

setup(
    name='py-vkontakte',
    version='2016.8',
    packages=['vk'],
    url='https://github.com/sgaynetdinov/py-vkontakte',
    license='MIT License',
    author='Sergey Gaynetdinov',
    author_email='s.gaynetdinov@gmail.com',
    description='Python API wrapper around vk.com API',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
    install_requires=[
        'requests',
    ],
)
