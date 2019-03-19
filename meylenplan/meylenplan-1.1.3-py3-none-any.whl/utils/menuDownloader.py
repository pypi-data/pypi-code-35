import urllib

def download_menu(url, path):
    u = urllib.request.urlopen(url)
    f = open(path, 'wb')
    f.write(u.read())
    f.close()
