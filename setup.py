#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='contrail-cli',
    version='0.0.1.dev1',

    description='A tool for interacting with Contrail',
    long_description=open('README.rst').read(),

    author='Adrian Smith',
    author_email='adrian@17od.com',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    install_requires=['cliff', 'requests'],

    packages=['contrailcli'],

    entry_points={
        'console_scripts': [
            'contrail = contrailcli.main:main'
        ]
    }
)

