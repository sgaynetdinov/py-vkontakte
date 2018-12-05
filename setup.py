#!/usr/bin/env python
from setuptools import setup

setup(
    name='py-vkontakte',
    version='5.63.3',
    packages=['vk'],
    url='https://github.com/sgaynetdinov/py-vkontakte',
    license='MIT License',
    author='Sergey Gaynetdinov',
    author_email='s.gaynetdinov@gmail.com',
    description='Python API wrapper around vk.com API',
    long_description=open('README.md').read(),
    keywords='vk.com, vk, vkontakte, vk api',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
