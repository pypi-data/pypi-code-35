import os
import sys

def test1():
    target = os.path.join(os.path.dirname(__file__), 'test1.py')
    os.execv(target, sys.argv)

def test2():
    target = os.path.join( os.path.dirname(__file__), 'test2.py')
    os.execl(sys.executable,'python',target, sys.argv)

