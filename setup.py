#!/usr/bin/env python

from setuptools import setup, find_packages
from pybiosas.version import VERSION

setup(name='pybiosas',
      version=VERSION,
      description='Library of SANS model fitting and management tools',
      author='Cameron Neylon',
      author_email='pypi@cameroneylon.net',
      url='https://github.com/cameronneylon/contrail',
      packages=find_packages(),
      package_data = {
          'test' : ['*.json', '*.xml', '*.sh']
          },
      install_requires = [
          'numpy',
          'scipy',
          'pycml',
          'contrail_sansmodels'
          ],
      test_suite='test'
     )
