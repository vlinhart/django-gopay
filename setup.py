#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
    
import os

setup(
    name = "django-gopay",
    version = "0.1",
    url = 'https://github.com/vlinhart/django-gopay',
	download_url = 'https://github.com/vlinhart/django-gopay/downloads',
    license = 'BSD',
    description = "Django app to ease gopay payment integration for weary developer.",
    author = 'Vladimir Linhart',
    author_email = 'vladimir.linhart@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
