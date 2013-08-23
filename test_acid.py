#!/usr/bin/env python
"""Test that untokenize always generates the expected output.

That is, the output of

untokenize.untokenize(tokenize.generate_tokens(file_input.readline))

is exactly equal to the input file.

"""

from __future__ import print_function
from __future__ import unicode_literals

import io
import os
import sys
import tokenize

import untokenize


try:
    unicode
except NameError:
    unicode = str


def open_with_encoding(filename, encoding, mode='r'):
    """Return opened file with a specific encoding."""
    return io.open(filename, mode=mode, encoding=encoding,
                   newline='')  # Preserve line endings


def detect_encoding(filename):
    """Return file encoding."""
    try:
        with open(filename, 'rb') as input_file:
            from lib2to3.pgen2 import tokenize as lib2to3_tokenize
            encoding = lib2to3_tokenize.detect_encoding(input_file.readline)[0]

            # Check for correctness of encoding.
            with open_with_encoding(filename, encoding) as input_file:
                input_file.read()

        return encoding
    except (SyntaxError, LookupError, UnicodeDecodeError):
        return 'latin-1'


def diff(before, after):
    """Return diff of two files."""
    import difflib
    return ''.join(difflib.unified_diff(
        before.splitlines(True),
        after.splitlines(True),
        lineterm='\n'))


def run(filename):
    """Check untokenize with file.

    Return True on success.

    """
    with open_with_encoding(filename,
                            encoding=detect_encoding(filename)) as input_file:
        source_code = input_file.read()

        # Handle files with trailing whitespace, but no final newline.
        # tokenize.generate_tokens() will not report the trailing whitespace in
        # such a case.
        if source_code.endswith((' ', '\t')):
            source_code = source_code.rstrip()

        string_io = io.StringIO(source_code)

        generated = untokenize.untokenize(
            tokenize.generate_tokens(string_io.readline))

        if source_code == generated:
            return True
        else:
            print('untokenize failed on ' + filename,
                  file=sys.stderr)
            print(diff(source_code, generated),
                  file=sys.stderr)


def process_args():
    """Return processed arguments (options and positional arguments)."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help='files to format')
    return parser.parse_args()


def check(args):
    """Run test recursively on directory of files.

    Return False if the fix results in broken syntax.

    """
    if args.files:
        dir_paths = args.files
    else:
        dir_paths = [path for path in sys.path
                     if os.path.isdir(path)]

    filenames = dir_paths
    completed_filenames = set()

    while filenames:
        try:
            name = os.path.realpath(filenames.pop(0))
            if not os.path.exists(name):
                # Invalid symlink.
                continue

            if name in completed_filenames:
                print('--->  Skipping previously tested ' + name,
                      file=sys.stderr)
                continue
            else:
                completed_filenames.update(name)

            if os.path.isdir(name):
                for root, directories, children in os.walk(unicode(name)):
                    filenames += [os.path.join(root, f) for f in children
                                  if f.endswith('.py') and
                                  not f.startswith('.')]

                    directories[:] = [d for d in directories
                                      if not d.startswith('.')]
            else:
                print('--->  Testing with ' + name,
                      file=sys.stderr)

                if not run(os.path.join(name)):
                    return False
        except (IndentationError,
                tokenize.TokenError,
                UnicodeDecodeError,
                UnicodeEncodeError) as exception:
            print('--->  Skipping bad file {0} ({1})'.format(name, exception),
                  file=sys.stderr)
            continue

    return True


def main():
    """Run main."""
    return 0 if check(process_args()) else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)
