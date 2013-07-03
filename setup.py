#!/usr/bin/env python

"""Setup for untokenize."""

import ast
from distutils import core


def version():
    """Return version string."""
    with open('untokenize.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


with open('README.rst') as readme:
    core.setup(name='untokenize',
               version=version(),
               description='Transforms tokens into original source code '
                           '(while preserving whitespace).',
               long_description=readme.read(),
               license='Expat License',
               author='Steven Myint',
               url='https://github.com/myint/untokenize',
               classifiers=['Intended Audience :: Developers',
                            'Environment :: Console',
                            'Programming Language :: Python :: 2.6',
                            'Programming Language :: Python :: 2.7',
                            'Programming Language :: Python :: 3',
                            'License :: OSI Approved :: MIT License'],
               keywords='tokenize,untokenize,transform,generate',
               py_modules=['untokenize'])
