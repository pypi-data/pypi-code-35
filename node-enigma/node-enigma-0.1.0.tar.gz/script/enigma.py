import sys
import argparse
import requests


logo = '\033[95m'+ '      '+''' 
                   _______       _                   
                  (_______)     (_)                  
                   _____   ____  _  ____ ____   ____ 
                  |  ___) |  _ \| |/ _  |    \ / _  |
                  | |_____| | | | ( ( | | | | ( ( | |
                  |_______)_| |_|_|\_|| |_|_|_|\_||_|
                                  (_____|    '''

note = '''Please be advised that this cli/programe is run via Heroku and so it might take few seconds to start up.
		   
		  Refer help --help for basic usage
		'''
	
error = "Error: Wrong input. Refer help --help for basic usage"

base_url = "https://node-enigma-api.herokuapp.com/api/"



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', "--verbosity", action="count", default=0)
	parser.add_argument('-e', "--encrypt", help="message to be encrypted")
	parser.add_argument('-f', "--input", help="file input")
	parser.add_argument('-o', "--output", help="file output")
	parser.add_argument('-t', "--type", help="machine type")
	parser.add_argument('-s', "--setting", help="machine setting")
	parser.add_argument('-k', "--key", help="machine key/code")
	parser.add_argument('-p', "--plug", help="machine plugboard")

	args = parser.parse_args()


	if args.input and args.output:
		f = open(args.input,'r')
		if f.mode == 'r':
			contents = "".join(f.read().split());
			w = open(args.output, 'w+')
			#print(contents)
			try:
				cypher = enigma(args.encrypt, type=args.type.lower() if args.type  else "m3", plug=args.plug, code=args.key, setting=args.setting)	
				w.write(cypher[ 15: cypher.find(',') - 1])
			except ValueError as ve:
				error()
				sys.exit(1)
			w.close()
		sys.exit(0)

	if args.encrypt and args.verbosity:
			try:
				print(enigma(args.encrypt, type=args.type.lower() if args.type  else "m3", plug=args.plug, code=args.key, setting=args.setting))
			except ValueError as ve:
				error()
				sys.exit(1)
			sys.exit(0)

	if args.encrypt: 
		try:
			cypher = enigma(args.encrypt, type=args.type.lower() if args.type  else "m3", plug=args.plug, code=args.key, setting=args.setting)
			print(cypher[ 15: cypher.find(',') - 1])
		except ValueError as ve:
				error()
				sys.exit(1)
		sys.exit(0)

	intro()
	
	
def intro():
	print(logo)
	print(note)

def error():
	print(error)

def enigma(plain, type="m3", **kwargs):
	config = ""
	for key, value in kwargs.items():
		if value is not None:
			config += '{0}={1} '.format(key,value)
	config = config.replace(' ','&')[:-1];
	endpoint = base_url + '{0}/{1}?'.format(type,plain) + config;
	response = requests.get(endpoint)
	#print(endpoint)
	return response.text
