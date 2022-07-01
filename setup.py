# -*- coding: utf-8 -*-

"""
The setup script is the centre of all activity in building, distributing, and installing modules.
"""

from __future__ import absolute_import
from setuptools import setup, find_packages


def readme():
    """
    Return README content.

    :return: The specified number of bytes from the file
    """
    with open('README.md') as filepointer:
        return filepointer.read()


setup(name='untraceables',
      version='1.5.0',
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
