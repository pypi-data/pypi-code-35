import os, time
def get_cur_time():
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

def touch_suffix(target, suffix):
    return target + ('' if target.endwith(suffix) else suffix)

def touch_prefix(target, prefix):
    return ('' if target.startwith(prefix) else prefix) + target

def file_stat(path):
    '''
    @params:
        path (str): path to query
    
    @returns:
        one of [dir, file, link, None]
    '''
    if os.path.isdir(path):
        return 'dir'
    if os.path.isfile(path):
        return 'file'
    if os.path.islink(path):
        return 'link'
    return None

def touchdir(path):
    if file_stat(path) is not None:
        return False
    os.makedirs(path)
    return True
