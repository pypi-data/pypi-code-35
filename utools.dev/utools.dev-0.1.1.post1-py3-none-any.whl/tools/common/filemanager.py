import os


class IFileManager(object):
    workdirname = '.utools'
    workdirpath = ''

    def createworkspace(self):
        pass

    def readconfig(self):
        pass
    @staticmethod
    def filter_by_ext(files:list=[],ext:list=['.png']):
        return list(filter(lambda f:os.path.splitext(f)[-1] in ext,files))

class IGit(object):

    @staticmethod
    def get_git_root_dir():
        lines = os.popen('git rev-parse --show-toplevel').readlines()
        if(len(lines) > 0):
            return lines[0].strip()
    @staticmethod
    def get_cache_diff_files():
        difffiles=[]
        lines = os.popen('git diff --cached  --name-only').readlines()
        for line in lines:
            difffiles.append(line.strip())
        return difffiles
        
class FileManager(IFileManager):
    pass


if __name__ == "__main__":
    # print(IGit.get_cache_diff_files())
    ext=['.md','.cfg']
    files =IGit.get_cache_diff_files()
    print(files)
    for a in IFileManager.filter_by_ext(files,ext):
        print(a)
    