#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Static Sauce',
    version='0.1',
    description='Static Website Generator',
    author='Jon Dufresne',
    author_email='jon.dufresne@gmail.com',
    url='http://github.com/jdufresne/staticsauce',
    packages=[
        'staticsauce',
        'staticsauce.commands',
        'staticsauce.modules',
        'staticsauce.modules.blog',
        'staticsauce.modules.photo',
        'staticsauce.modules.photo.controllers',
        'staticsauce.templating',
    ],
    scripts=['scripts/staticsauce'],
)
