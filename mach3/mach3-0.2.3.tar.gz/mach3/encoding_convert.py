import codecs
import os
from chardet import detect

BLOCKSIZE = 1048576
targetFormat = "utf-8"

def get_encoding_type(fileName):
    with open(fileName, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']



def writeConversion(srcfile):
    print(srcfile, get_encoding_type(srcfile))
    trgfile = srcfile + "UTF-8"
    try:
        with open(srcfile, 'r', encoding=get_encoding_type(srcfile)) as f, open(trgfile, 'w', encoding='utf-8') as e:
            text = f.read()
            e.write(text)

        os.remove(srcfile)
        os.rename(trgfile, srcfile)
    except UnicodeDecodeError:
        print('Decode Error')
    except UnicodeEncodeError:
        print('Encode Error')