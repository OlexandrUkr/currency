# import sys

try:
    from .local import *
except ImportError:
    from .base import *

# if 'test' in sys.argv:
#     from .tests import *
