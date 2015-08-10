from .utils import safe_pickle_dump, safe_pickle_load
import cPickle
import hashlib
import os
# from . import logger

__all__ = [
    'memo_disk',
    'memo_disk_dec',  # decorator
]

MEMO_DISK_CACHE_DIR = 'out-memo_disk'


def memo_disk_dec(f):
    ''' Decorator fro memo_disk '''
    def f2(*args, **kwargs):
        return memo_disk(f, *args, **kwargs)
    return f2



def memo_disk(func, *args, **kwargs):
    ''' 
        Caches a result that is associated to the given function.
        
        The cache file is 
            
            <dirname>/memo_disk_cache/<basename>.<key>.pickle
        
        The result must be msgpackable.
        
    '''

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

    hash1 = _get_hash((args, kwargs))

    key = '%s.%s' % (func.__name__, hash1)

    cachename = key + '.pickle'
    cachefile = os.path.join(cachedir, cachename)

    if os.path.exists(cachefile):
        # logger.info('reading from cache: %s' % cachefile)
        res = safe_pickle_load(cachefile)
        return res

    res = func(*args, **kwargs)

    # logger.info('writing to cache: %s' % cachefile)
    safe_pickle_dump(res, cachefile)

    return res


def _get_hash(x):
    s = cPickle.dumps(x)
    hash1 = hashlib.sha224(s).hexdigest()
    return hash1
