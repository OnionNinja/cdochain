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
      version='0.2b1',
      description='Easy chaining of cdo methods.',
      author='Uğur Çayoğlu',
      author_email='urcyglu@gmail.com',
      url='https://github.com/OnionNinja/cdochain',
      license='MIT',
      packages=['cdochain'],
      install_requires=[
          'cdo',  # duh?
          'numpy',
      ],
      classifiers=[
          # More at http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Scientific/Engineering :: GIS',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Intended Audience :: Science/Research',
        ],
      keywords=['netcdf', 'cdo', 'wrapper', 'chaining'],
      long_description=long_description,
      include_package_data=True,
      zip_safe=False)
