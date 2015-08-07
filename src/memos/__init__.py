
import logging
logging.basicConfig()
from logging import getLogger
logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)

from .memoization import *
from .memoize_limits import *
from .memo_disk_cache_imp import *
from .memo_disk_imp import *
