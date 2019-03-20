# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '1.3.1'
major           = '1'
minor           = '3'
patch           = '1'
rc              = '0'
istaged         = False
commit          = 'e61d7245dbe34875f66b0d6f179730f4dde647e2'
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
