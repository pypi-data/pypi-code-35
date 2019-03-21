import math
import argparse
import requests
import validators
import os
from tqdm import tqdm
import random

cs = 1024
urlist = ['com','org','net','edu','gov','co','io','biz','dev','kr','cf','onion','cat','am','ag','uk','in','tv']

parser = argparse.ArgumentParser(description='file downloader')
parser.add_argument('url',help="url to be downloaded",metavar='url')
parser.add_argument('-o','--output',help="output file",metavar='')
args = parser.parse_args()

def churl(u):
	do = u.split('.')[-1]
	for dom in urlist:
		if (do==dom):
			return True
			break

def getfilename(u):
	file = u.split('/')[-1]
	new = file.split('?')[0]
	
	if new=='':
		return 'file{}.html'.format(random.randint(1,1000))
	elif (churl(new)==True):
		return '{}.html'.format(new)
	else:
		return new
def main():
	if validators.url(args.url) is True:
		try:
			r = requests.get(args.url,stream=True)
			if(r.status_code==200):
				r.encoding = 'UTF-8'
				if args.output:
					file = str(args.output)
				else:
					file = getfilename(args.url)
				ts = int(r.headers.get('content-length'))
				with open(file,'wb') as f:
					for data in tqdm(iterable = r.iter_content(chunk_size=cs),total=ts/cs,unit='KB'):
						f.write(data)
				print('\nfile downloaded to:{}\\{}').format(os.getcwd(),file)
			else:
				print('error:status-code:%s') % r.status_code
		except (requests.exceptions.ConnectionError,TypeError):
			print('error:connection-refused')
	else:
		print('error:invalid-url')

if __name__=='__main__':
	main()
