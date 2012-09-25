#!/usr/bin/python

from distutils.core import setup, Extension
 
module1 = Extension('quarto', sources = ['lib/minimax.c'], extra_compile_args=['-std=c99'])
  
setup(name = 'PackageName', version = '0.1', description = 'This is a minimax package which can be\
        used in Python', ext_modules = [module1])
