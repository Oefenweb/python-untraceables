# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def readme():
  with open('README.md') as f:
    return f.read()


setup(name='untraceables',
      version='0.0.0',
      author='Mischa ter Smitten',
      author_email='mtersmitten@oefenweb.nl',
      maintainer='Mischa ter Smitten',
      maintainer_email='mtersmitten@oefenweb.nl',
      url='https://www.oefenweb.nl/',
      download_url='https://github.com/Oefenweb/python-untraceables',
      license='MIT',
      description='Tools to work with ...',
      long_description=readme(),
      packages=find_packages(exclude=['test']),
      scripts=['bin/randomize-ids'],
      data_files=[('config', ['untraceables.cfg.default'])],
      platforms=['GNU/Linux'])
