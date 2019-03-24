#!/usr/bin/python3

import sys
import re
import requests
import zipfile
import os
import tempfile
from subprocess import call
from distutils.spawn import find_executable as which
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
try:
    from urllib.request import Request, urlopen  # Python 3
    from urllib.error import HTTPError
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import Request, urlopen, HTTPError  # Python 2

def version():
    print ('Vesion 0.1');

def help():
    print ('Call the application with the right arguments:')
    print ("\t./eprism.py install APP_NAME|ROM_URL")

def report(count, blockSize, totalSize):
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("\r%d%%" % percent + ' complete')
    sys.stdout.flush()

def download(url):
    '''new_file, filename = tempfile.mkstemp()
    u = urlopen(url)
    #request = urllib2.Request(url, headers={'Accept-Encoding': 'gzip'})
    #request = urllib2.Request(url)
    #u = urllib2.urlopen(request)
    meta = u.info()
    file_name = url.split('/')[-1]
    #u = urllib2.urlopen(url)
    #f = open(file_name, 'wb')
    print('getheader' in dir(u))
    if 'getheader' in dir(u):
        file_size = int(u.getheader("Content-Length"))
    else:
        file_size = int(meta.getheaders("Content-Length")[0])

    # TODO: Check if it's zip, for now we just accept zip
    # contentType = meta.getheaders("Content-Type")[0]
    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

    file_size_dl += len(buffer)
    os.write(new_file, buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print(status),

    os.close(new_file)

    return filename'''

    print ('Download ROM...')
    file = urlopen(url)
    with open('rom.bin.zip','wb') as output:
        output.write(file.read())
    return 'rom.bin.zip'

def unzip(filename):
    print ("Decompress: " + filename)
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(filename + '_files')
    zip_ref.close()

    return os.path.join(filename + '_files', 'rom.bin')

def setup(filename):
    print ("Installing the app")

    call([which('esptool.py'), "write_flash", "0", filename])

def install(app):
    print ('Try to install: ' + app)
    pattern = re.compile("^(?i)https?://.*$")
    if pattern.match(app):
        url = app;
    else:
        url = 'https://github.com/eprism/eprism-apps/releases/download/' + app + '-latest/rom.bin.zip';
    file = download (url)
    rom = unzip (file)
    setup (rom)

def main():
    if len(sys.argv) < 2:
        help()
    elif sys.argv[1] == 'version':
        version()
    elif sys.argv[1] == 'help':
        help()
    elif sys.argv[1] == 'install' and len(sys.argv) == 3:
        install(sys.argv[2])
    else:
        version()

if __name__ == '__main__':
    main()