import os, os.path, shutil
from .core import logger

def run(para, output = True, fetch = False):
    import subprocess
    if output and not fetch:
        subprocess.call(para)
    else:
        p = subprocess.Popen(para, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        txt, error = p.communicate()
        #python 3
        if txt.__class__.__name__ == 'bytes':
            txt = txt.decode(sys.stdout.encoding)
            error = error.decode(sys.stdout.encoding)
        if output:
            print(txt)
        if fetch:
            return (txt, error)

    return None

def get_file_list(path, ignore = None, absolute = True, basepath = None):
    rst = []
    #first run
    if not absolute and basepath is None:
        basepath = path
        path = ''
    if basepath is not None:
        abspath = os.path.join(basepath, path)
    else:
        abspath = path

    for f in os.listdir(abspath):
        full_file_path = os.path.join(abspath, f)
        if ignore is not None and ignore(full_file_path):
            continue
        if os.path.isfile(full_file_path):
            rst.append(os.path.join(path, f))
        elif os.path.isdir(full_file_path):
            rst.extend(get_file_list(os.path.join(path, f), ignore, absolute, basepath))
    return rst

def merge_files(files, target, sep = ''):
    content = ''
    try:
        for f in files:
            fh = open(f)
            content += fh.read() + sep
            fh.close()
        dirname = os.path.dirname(target)
        if not os.path.isdir(dirname):
            os.path.makedirs(dirname)
        fh = open(target, 'w')
        fh.write(content)
        fh.close()
        return True
    except Exception as e:
        logger.error('merge failed: %s' %e)
        return False

def replace_file_content(f, find, replace):
    try:
        fh = open(f)
        content = fh.read()
        fh.close()
        fh = open(f, 'w')
        fh.write(content.replace(find, replace))
        fh.close()
        return True
    except:
        return False

def convert_encoding(f, from_encoding, to_encoding):
	source = open(f)
	source_content=source.read()
	source.close()
	
	target = open(f, 'w')
	
	target.write(unicode(source_content, from_encoding).encode(to_encoding))
	target.close()

def rmtree(path):
    shutil.rmtree(path, ignore_errors = False, onerror = _handleRemoveReadonly)

def _handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

def check_bom(f):
    fh = open(f)
    bom = fh.read(3) == "\xef\xbb\xbf"
    fh.close()

    return bom