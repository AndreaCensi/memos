import os

from contracts import contract

from . import logger
from .utils import safe_pickle_dump, safe_pickle_load


__all__ = ['memo_disk_cache']


MEMO_DISK_CACHE_DIR = 'memo_disk_cache'

@contract(filename='str', key='str')
def memo_disk_cache(filename, key, func, *args, **kwargs):
    """ 
        Caches a result that is associated to the given file.
        
        The parameter 'key' must be a simple string that can appear
        in a filename. 
        
        The cache file is 
            
            <dirname>/memo_disk_cache/<basename>.<key>.pickle
        
        The result must be pickable.
        
    """
    
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)

    cachedir = os.path.join(dirname, MEMO_DISK_CACHE_DIR)
    if not os.path.exists(cachedir):
        try:
            os.makedirs(cachedir)
        except:
            if os.path.exists(cachedir):
                pass
            else:
                raise

    cachename = basename + '.' + key + '.pickle'
    cachefile = os.path.join(cachedir, cachename)

    if os.path.exists(cachefile):
        # logger.info('reading from cache: %s' % cachefile)
        res = safe_pickle_load(cachefile)
        return res

    res = func(*args, **kwargs)

    logger.info('writing to cache: %s' % cachefile)
    safe_pickle_dump(res, cachefile)
    
    return res


