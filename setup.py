#!/usr/bin/python

from distutils.core import setup, Extension

module1 = Extension('cquarto', sources = ['lib/minimax.c'],
        extra_compile_args=['-std=c99', '-march=native'], include_dirs=['lib'])

setup(name = 'CQuarto', version = '0.1', description = 'This is a minimax package which can be\
        used in Python', ext_modules = [module1])
