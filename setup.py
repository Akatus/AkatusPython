#!/usr/bin/env python

from distutils.core import setup

setup(name='Pykatus',
      version='0.0.7',
      description='Python integration with Akatus payment gateway via API',
      author=['Ale Borba', 'Igor Hercowitz'],
      author_email=['alexandre.borba@imasters.com.br', 'ihercowitz@gmail.com'],
      url='https://www.akatus.com/',
      packages=['pykatus','validators'],
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
