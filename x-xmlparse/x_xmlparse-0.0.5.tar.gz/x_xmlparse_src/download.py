from tqdm import tqdm
import requests
import math
import  os
from concurrent.futures.thread import ThreadPoolExecutor

if not os.path.exists("/tmp/downloads"):
    os.mkdir("/tmp/downloads")

DOWN_ROOT = "/tmp/downloads"

exe = ThreadPoolExecutor(max_workers=12)

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

Process = None

def init_process(total, desc=' no desc'):
    global Process
    Process = tqdm(total=total, desc=desc)

def update():
    global Process
    if not Process:
        Process = tqdm()
    Process.update()

def download(url, proxy=None, name=None):
    # Streaming, so we can iterate over the response.
    sess = requests.Session()
    if proxy:
        sess.proxies['https'] = proxy
        sess.proxies['http'] = proxy
    sess.headers.update({'User-agent':UA})
    r = requests.get(url, stream=True)
    block_size = 1024
    if not name:
        name = os.path.basename(url)
    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0)); 
    wrote = 0 
    with open(os.path.join(DOWN_ROOT, name), 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
            wrote = wrote  + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")


def get(url, parser, show, proxy=''):

    sess = requests.Session()
    if proxy:
        sess.proxies['https'] = proxy
        sess.proxies['http'] = proxy
    sess.headers.update({'User-agent':UA})
    res = sess.get(url)
    if res.status_code == 200:
        if parser:
            e = parser(res.text)
        if show:
            e = show(e)
        else:
            e = res.text
        return  e
        
    return  ''
    

def add_url_to_download(url, proxy):
    exe.submit(download, url, proxy=proxy)


def linesprint(res):
    for l in res:
        print(l)

def add_url(url, proxy, parser, show,callback=None):
    f = exe.submit(get, url, parser, show, proxy=proxy)
    if callback:
        f.add_done_callback(callback)

    return  f