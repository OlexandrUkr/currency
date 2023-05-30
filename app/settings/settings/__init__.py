# import sys

try:
    from .local import *  # noqa: F401, F403
except ImportError:
    from .base import *  # noqa: F401, F403

# if 'test' in sys.argv:
#     from .tests import *
