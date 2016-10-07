#!/usr/bin/env python

from distutils.core import setup

setup(name='PEAS',
      version='1.0',
      description='ActiveSync Library',
      author='Adam Rutherford',
      author_email='adam.rutherford@mwrinfosecurity.com',
      packages=['peas', 'peas.eas_client',
                'peas.pyActiveSync', 'peas.pyActiveSync.client', 'peas.pyActiveSync.objects', 'peas.pyActiveSync.utils'],
      scripts=['scripts/peas'],
     )
