# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '1.3.2'
major           = '1'
minor           = '3'
patch           = '2'
rc              = '0'
istaged         = True
commit          = '845f36c79b8a7618427c8d9a2eed4a77463caaae'
with_mkl        = 'ON'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl
