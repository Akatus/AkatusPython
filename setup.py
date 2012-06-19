#!/usr/bin/env python

from distutils.core import setup

setup(name='Pykatus',
      version='0.0.2',
      description='Python integration with Akatus payment gateway via API',
      author='Ale Borba',
      author_email='alexandre.borba@imasters.com.br',
      url='https://www.akatus.com/',
      packages=['pykatus'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOSX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',  
      ])
