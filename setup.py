#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.md') as file:
    long_description = file.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='automile_api',
    version='0.1',
    author='Andreas Klintberg',
    author_email='ankl@kth.se',
    description='Library for connecting to the Automile v1 API',
    long_description=long_description,
    url='https://api.automile.com',
    license='MIT',
    packages=find_packages(),
    install_requires=required,
    py_modules=['automile/automile_api'],
)
