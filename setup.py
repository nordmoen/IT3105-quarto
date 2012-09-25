#!/usr/bin/python

from distutils.core import setup, Extension
 
module1 = Extension('minimax', sources = ['lib/minimax.c'])
  
setup(name = 'PackageName', version = '0.1', description = 'This is a minimax package which can be\
        used in Python', ext_modules = [module1])
