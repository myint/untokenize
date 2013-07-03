============
untokenize
============

Transforms tokens into original source code. Unlike the standard library's
``tokenize.untokenize()``, it preserves the original whitespace.

.. image:: https://travis-ci.org/myint/untokenize.png?branch=master
   :target: https://travis-ci.org/myint/untokenize
   :alt: Build status


Usage
=====

.. code-block:: python

    import untokenize
    untokenize.untokenize(tokens)
