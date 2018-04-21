#!/usr/bin/env python

PROJECT = 'graffiti'
VERSION = '0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Graffiti',
    long_description=long_description,

    author='Paul blottiere',
    author_email='paul.blottiere@gmail.com',

    url='https://github.com/pblottiere/graffiti',
    download_url='https://github.com/pblottiere/graffiti/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['pygal',],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
