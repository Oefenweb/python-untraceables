# -*- coding: utf-8 -*-

from __future__ import absolute_import
from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='untraceables',
      version='1.4.1',
      author='Mischa ter Smitten',
      author_email='mtersmitten@oefenweb.nl',
      maintainer='Mischa ter Smitten',
      maintainer_email='mtersmitten@oefenweb.nl',
      url='https://www.oefenweb.nl/',
      download_url='https://github.com/Oefenweb/python-untraceables',
      license='MIT',
      description='Randomizes IDs for a given set of tables making them untraceable across environments',
      long_description=readme(),
      packages=find_packages(exclude=['test']),
      scripts=['bin/randomize-ids'],
      data_files=[('config', ['untraceables.cfg.default'])],
      platforms=['GNU/Linux'])
