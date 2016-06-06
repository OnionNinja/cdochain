#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""Setup of cdochain."""

from setuptools import setup
import os

if os.path.exists('README.rst'):
    long_description = open('README.rst').read()
else:
    long_description = ""

setup(name='cdochain',
      version='0.1a7',
      description='Easy chaining of cdo methods.',
      author='Uğur Çayoğlu',
      url='https://github.com/OnionNinja/cdochain',
      license='MIT',
      packages=['cdochain'],
      install_requires=[
          'cdo',  # duh?
          'numpy',
      ],
      classifiers=[
          # More at http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3 :: Only',
        ],
      keywords=['netcdf', 'cdo', 'wrapper', 'chaining'],
      long_description=long_description,
      include_package_data=True,
      zip_safe=False)
