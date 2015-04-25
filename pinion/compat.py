import sys

PY3 = sys.version_info[0] >= 3


if PY3:
    text_type = str
    string_types = (str,)
    bytes_type = bytes
else:
    text_type = unicode
    string_types = (str, bytes,)
    bytes_type = bytes
