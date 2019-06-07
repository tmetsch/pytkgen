#!/bin/python

#
# Copyright (c) 2011. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301  USA

from distutils.core import setup

setup(name = 'pytkgen',
      version = '1.6',
      description = 'Create Tkinter GUIs from JSON definition files.',
      author = 'Thijs Metsch',
      author_email = 'tmetsch@opensolaris.org',
      url='https://github.com/tmetsch/pytkgen',
      license='LGPL',
      packages = ['tkgen'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Manufacturing',
          'Intended Audience :: Other Audience',
          'Intended Audience :: Science/Research',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Desktop Environment',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: Utilities'
      ]
     )
