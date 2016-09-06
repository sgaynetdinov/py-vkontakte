#!/usr/bin/env python
from distutils.core import setup

setup(
    name='pyvk',
    version='2016.08',
    packages=['pyvk'],
    url='https://github.com/sgaynetdinov/pyvk',
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
