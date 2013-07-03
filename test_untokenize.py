#!/usr/bin/env python

"""Test suite for untokenize."""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import io
import tokenize
import unittest

import untokenize


class TestUnits(unittest.TestCase):

    def check(self, source_code):
        string_io = io.StringIO(source_code)
        self.assertEqual(
            source_code,
            untokenize.untokenize(
                tokenize.generate_tokens(string_io.readline)))

    def test_untokenize(self):
        self.check('''

def zap():

    """Hello zap.

  """; 1


    x \t= \t\t  \t 1


''')

    def test_untokenize_with_tab_indentation(self):
        self.check("""
if True:
\tdef zap():
\t\tx \t= \t\t  \t 1
""")

    def test_untokenize_with_backslash_in_comment(self):
        self.check(r'''
def foo():
    """Hello foo."""
    def zap(): bar(1) # \
''')

    def test_untokenize_with_escaped_newline(self):
        self.check(r'''def foo():
    """Hello foo."""
    x = \
            1
''')


if __name__ == '__main__':
    unittest.main()
