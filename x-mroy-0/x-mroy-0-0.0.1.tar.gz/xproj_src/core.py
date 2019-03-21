import os
import sys
from .data import E, J, Mk, Con, Proj, create
import git
from termcolor import colored
import logging
from .tmp import py_setup_tmp, py_ignore, py_cmd_tmp, read_me_tmp
import getpass
import requests
# from mroylib.config import Config
logging.basicConfig(level=logging.INFO)




def L(cmd, head="msg", bold=False, color='blue'):
    h =colored("[%s]" % head, 'green')
    if color:
        cmd = colored(cmd, color)
    if bold:
        logging.info(h + colored(cmd, attrs=['bold']))
    else:
        logging.info(h + colored(cmd, attrs=['bold']))


def create_git(repo_dir):
    # file_name = os.path.join(repo_dir, 'new-file')

    r = git.Repo.init(repo_dir)
    # This function just creates an empty file ...
    name = os.path.basename(repo_dir)
    L("init -> %s" % name, head='git', bold=True, color='green')
    return r

def init(name):
    path = os.getcwd()
    path = J(path, name)
    if not E(path):
        Mk(path)
    else:
        L("exists git", bold=True, color='red', head='git')

    if not E(J(path, '.git')):
        return create_git(path)
    else:
        return git.Repo(path)


def create_remote(name, user, proxy='socks5h://127.0.0.1', desc="some"):
    passwd = getpass.getpass("git passwd>")
    sess = requests.Session()
    if proxy:
        sess.proxies['https'] = proxy
        sess.proxies['http'] = proxy
    data = {
        "name": "%s" % name,
        "description": "%s" % desc,
        "homepage": "https://github.com/%s/%s" % (user, name),
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }
    res = sess.post("https://github.com/user/repo/", data=data)


def py_init(path,name, *dependences, 
            desc='some desc', 
            url='https://github.com/xxx',
            auth='auth',
            email='xxx@gmail.com', 
            cmd=''):
    if cmd:
        cmd = cmd + "=%s_src.cmd:main" % name
    if dependences:
        ds = ','.join(["'%s'" % i for i in dependences])
    py_setup = py_setup_tmp % (name, desc, url, auth, email, ds, cmd)
    with open(J(path, "setup.py"), "w") as fp:
        fp.write(py_setup)
    
    with open(J(path, '.gitignore'), 'w') as fp:
        fp.write(py_ignore)
    
    if not E(J(path,"%s_src")):
        Mk(J(path,"%s_src" % name))

    with open(J(path, "%s_src/cmd.py" % name), 'w') as fp:
        fp.write(py_cmd_tmp)

    with open(J(path, "%s_src/__init__.py" % name), 'w') as fp:
        pass

    read_me = read_me_tmp % (name, auth, url, desc) 
    with open(J(path, 'README.md'), 'w') as fp:
        fp.write(read_me)
    
    create(name, path, desc=desc)
