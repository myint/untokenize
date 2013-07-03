"""Transform tokens into original source code."""

import tokenize


__version__ = '0.1'


def untokenize(tokens):
    """Return source code based on tokens.

    This is like tokenize.untokenize(), but it preserves spacing between
    tokens. So if the original soure code had multiple spaces between some
    tokens or if escaped newlines were used, those things will be reflected
    by untokenize().

    """
    text = ''
    previous_line = ''
    last_row = 0
    last_column = -1
    last_non_whitespace_token_type = None

    for (token_type, token_string, start, end, line) in tokens:

        (start_row, start_column) = start
        (end_row, end_column) = end

        # Preserve escaped newlines
        if (
            last_non_whitespace_token_type != tokenize.COMMENT and
            start_row > last_row and
            (previous_line.endswith('\\\n') or
             previous_line.endswith('\\\r\n') or
             previous_line.endswith('\\\r'))
        ):
            text += previous_line[len(previous_line.rstrip(' \t\n\r\\')):]

        # Preserve spacing
        if start_row > last_row:
            last_column = 0
        if start_column > last_column:
            text += line[last_column:start_column]

        text += token_string

        previous_line = line

        last_row = end_row
        last_column = end_column

        if token_type not in [tokenize.INDENT, tokenize.NEWLINE, tokenize.NL]:
            last_non_whitespace_token_type = token_type

    return text
