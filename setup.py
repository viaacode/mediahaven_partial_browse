#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 11:28:05 2022

@author: tina
"""


from setuptools import setup

setup(name='mediahaven_partial',
      version='v1.0',
      description='export browse partial from mediahaven',
      long_description='use pid start en end time in frames',
      classifiers=[
        'Development Status :: v1.0',
        'Intended Audience :: Developers',
        'License :: MIT 2020 Meemomo',
        'Programming Language :: Python :: 3.7',
        'Topic :: mediahaven export',
      ],
      keywords='mediahaven',
      author='Tina Cochet',
      author_email='tina.cochet@meemoo.be',
      license='MIT 2020 Meemoo',
      packages=['get_partial',
                'timecode_helper'],
      package_dir={'get_partial': 'get_partial',
                   'timecode_helper': 'timecode_helper'},
      package_data={
        'mediahaven_partial': ['_build/*'],
      },
      install_requires=[
              'requests',
              'retry==0.9.2',
              'pytest==5.4.1',
              'pytest-cov==2.8.1'
      ],


      entry_points={
         'console_scripts': ['mediahaven_partial=get_partial.get_partial:main',
                             'timecode_convert=timecode_helper.convert:main'
                             ],
    }, include_package_data=True, zip_safe=False)
