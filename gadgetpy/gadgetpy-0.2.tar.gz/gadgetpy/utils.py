import os

def verifyName(name):
    parts = name.split('.')
    return len(parts)==2

def verifyPointer(path,pointer):
    for gadget in os.listdir(path):
        if os.path.isfile(os.path.join(path,gadget,'UDC')):
            with open(os.path.join(path,gadget,'UDC')) as f:
                if f.read().strip() == pointer:
                    return False
    return pointer in os.listdir('/sys/class/udc')
