import os
import json
import tarfile
from typing import Iterable

CONFIG_SRC=[
	'/etc/arim/arim.json',    
        os.environ['HOME']+'/.config/arim/arim.json'
]
APP_DIRS=['/.','/.config/','/.loca/share/']

def config():
  result = dict()
  for f in CONFIG_SRC:
    try:
      with open(f,'r') as fd:
        result.update(json.load(fd))
    except FileNotFoundError: 
      pass

  return result

def getConfig(name: str) -> str:
  try:
    return config()[name]
  except KeyError :
    print("The configuration option: "+name+" was not defined")
    print("Please define it in one of "+str(CONFIG_SRC))
    raise 

def files(root: str) -> Iterable[str]:
  for path, dirs, files in os.walk(root):
    yield path
    for file in files:
      yield os.path.join(path,file)

def filesOf(name: str) -> Iterable[str]:
  for l in APP_DIRS:
    for p in files(os.environ['HOME']+l+name):
      yield p
def tarApp(name: str):
  bdir = getConfig('BDIR')
  os.makedirs(bdir,exist_ok=True)
  tarAppTo(name,bdir+'/'+name+".tar.bz2")

def tarAppTo(name: str, out: str):
  count=0
  with tarfile.open(out,'w:bz2') as tar:
    for p in filesOf(name):
      tar.add(p,arcname=p[9:],recursive=False)
      count+=1

  if count < 1:
    os.remove(out)
    print("No such app found: "+name)
