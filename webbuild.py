import os, os.path
import core
from .core import logger
import util

def merge(source, target, sep = '\r\n'):
    return util.merge_files(source, target, sep)

def compress(source, target, file_type = None):
    if file_type is None:
        ext = os.path.splitext(source)[1].lower()
        if ext == '.js':
            file_type = 'js'
        elif ext == '.css':
            file_type = 'css'
        else:
            raise

    bin = core.get_registry('yuicompressor')
    if not os.path.isfile(bin):
        logger.error('please specify path of yuicompressor')
        return False
    else:
        dirname = os.path.dirname(target)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        opts = ['java', '-jar', bin, '--type', file_type, '-v', '--charset', 'utf-8', source, '-o', target]
        if file_type == 'js':
            opts.insert(3, '--nomunge')

        output, error = util.run(opts, False, True)

        err_count = error.count('[ERROR]')
        warn_count = error.count('[WARNING]')
        if err_count:
            logger.error('%d errors found when compress %s' % (err_count, source))
            logger.debug(error)
            return False
        if warn_count:
            logger.warn('%d warnings found when compress %s' % (warn_count, source))
        return os.path.isfile(target)

def compress_js(source, target):
    return compress(source, target, 'js')

def compress_css(source, target):
    return compress(source, target, 'css')

def find_image_ref(css_file):
    pass