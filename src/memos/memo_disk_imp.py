import os


from . import logger
from .utils import safe_pickle_dump, safe_pickle_load

import hashlib


__all__ = ['memo_disk']


MEMO_DISK_CACHE_DIR = 'out-memo_disk'

def memo_disk(func, *args, **kwargs):
    """ 
        Caches a result that is associated to the given function.
        
        The cache file is 
            
            <dirname>/memo_disk_cache/<basename>.<key>.pickle
        
        The result must be msgpackable.
        
    """

    dirname = os.curdir
    cachedir = os.path.join(dirname, MEMO_DISK_CACHE_DIR)
    if not os.path.exists(cachedir):
        try:
            os.makedirs(cachedir)
        except:
            if os.path.exists(cachedir):
                pass
            else:
                raise

    import msgpack

    s = msgpack.packb((args, kwargs))
    hash1 = hashlib.sha224(s).hexdigest()

    key = '%s.%s' % (func.__name__, hash1)

    cachename = key + '.pickle'
    cachefile = os.path.join(cachedir, cachename)

    if os.path.exists(cachefile):
        logger.info('reading from cache: %s' % cachefile)
        res = safe_pickle_load(cachefile)
        return res

    res = func(*args, **kwargs)

    logger.info('writing to cache: %s' % cachefile)
    safe_pickle_dump(res, cachefile)

    return res
