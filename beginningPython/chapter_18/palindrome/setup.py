#!/usr/bin/python
from distutils.core import setup, Extension

setup(name='azhe\'s palindrome', 
        version='1.0',
        ext_modules=[
            Extension('palindrome',
                ['palindrome.c', 'palindrome.i'])
            ])
