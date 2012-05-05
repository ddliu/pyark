import os, os.path, shutil
from core import logger

'''
directory syncing
'''
def sync(a, b, ignore_copy = None, ignore_delete = None):
    if sync_copy(a, b, ignore_copy):
        sync_delete(b, a, ignore_delete)
        return True
    else:
        return False
    
'''
transfer everything in "a" to "b"
'''
def sync_copy(a, b, ignore = None):
    #ignonre
    if callable(ignore) and ignore(a, b):
        return True
    #dir
    if os.path.isdir(a):
        if not os.path.isdir(b):
            os.makedirs(b)
        for f in os.listdir(a):
            if not sync_copy(os.path.join(a, f), os.path.join(b, f), ignore):
                return False
        return True
    elif os.path.isfile(a):
        try:
            logger.info('copy %s => %s' % (a, b))
            shutil.copy2(a, b)
            
            return True
        except:
            logger.error('failed to copy file "%s"' % a)
            return False
            
    else:
        logger.warn('%s is not file or dir, and will not be copied' % a)
        return True
    
'''
delete everying that in "a" but not in "b"
'''
def sync_delete(a, b, ignore = None):
    if callable(ignore) and ignore(a, b):
        return True
    #dir
    if os.path.isdir(a):
        #if source dir not exist, remove target dir
        if not os.path.isdir(b):
            try:
                logger.info('remove dir %s' % a)
                util.rmtree(a)
                return True
            except:
                logger.error('failed to remove dir "%s"' % a)
                return False
        else:
            for f in os.listdir(a):
                if not sync_delete(os.path.join(a, f), os.path.join(b, f), ignore):
                    return False
            return True
    #file
    elif os.path.isfile(a):
        if not os.path.isfile(b):
            try:
                logger.info('remove file %s' % a)
                os.remove(a)
                return True
            except:
                logger.error('failed to remove file "%s"' % a)
                return False
        else:
            return True
    else:
        logger.info('%s is not dir or file, and will not be removed' % a)
        return True
