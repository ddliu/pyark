import os, os.path

'''
svn files will be ignored
'''
def ignore_svn(a):
    return os.path.basename(a) == '.svn'
    
'''
ignore compiler generated files
'''
def ignore_compile(a):
    return a.endswith('.pyc')
    
'''
ignore version controll files
'''
def ignore_vcs(a):
	basename = os.path.basename(a)
	return (basename in ['.svn', '.git', '.cvs']) or basename.startswith('.git')

'''
ignore files with specific extensions
'''
def ignore_ext(a, ext_list):
    return os.path.splitext(a).lower() in ext_list

'''
ignore file
'''
def ignore_file(a):
    return os.path.isfile(a)

'''
ignore dir
'''
def ignore_dir(a):
    return os.path.isdir(a)

'''
ignore temporary files
'''
def ignore_tmp(a):
    name = os.path.basename(a)
    return name.endswith(('.tmp', '.bck', '.bak', '__pycache__'))

'''
ignore if two files have the same size
'''
def ignore_filesize_unchange(a, b):
    return os.path.isfile(a) and os.path.isfile(b) and (os.path.getsize(a) == os.path.getsize(b))
    
'''
ignore if two files have the same mtime
'''
def ignore_mtime_unchange(a, b):
    if not os.path.isfile(a) or not os.path.isfile(b):
        return False
    ta = os.path.getmtime(a)
    tb =  os.path.getmtime(b)
    #mtime is not always the same, difference that less than 0.5s is allowed
    return  abs(ta - tb) < 0.5