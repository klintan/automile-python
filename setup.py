#!/usr/bin/env python
from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='automile_api',
    version='0.1',
    author='Andreas Klintberg',
    author_email='ankl@kth.se',
    description='Library for connecting to the Automile v1 API',
    long_description=long_description,
    url='https://api.automile.com',
    license='MIT',
    py_modules=['automile_api'],
)