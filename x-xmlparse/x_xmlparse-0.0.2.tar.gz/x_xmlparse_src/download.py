from tqdm import tqdm
import requests
import math
import  os
from concurrent.futures.thread import ThreadPoolExecutor

if not os.path.exists("/tmp/downloads"):
	os.mkdir("/tmp/downloads")

DOWN_ROOT = "/tmp/downloads"

exe = ThreadPoolExecutor(max_workers=12)

def download(url, proxy=None, name=None):
	# Streaming, so we can iterate over the response.
	sess = requests.Session()
	if proxy:
		sess.proxies['https'] = proxy
		sess.proxies['http'] = proxy
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


def add_url_to_download(url, proxy):
	exe.submit(download, url, proxy=proxy)


