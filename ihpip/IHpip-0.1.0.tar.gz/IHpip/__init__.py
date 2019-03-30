import yaml
import sys
from pip._internal import main as pip

def run():
	try:
		requirements_name = sys.argv[1]
		install_list = sys.argv[2]
	except:
		print("invalid amount of arguments")
	else:
		for requirement in parse_file(requirements_name)[install_list]:
			pip(['install', requirement])


def parse_file(file_name):
	with open(file_name, 'r') as stream:
		try:
			return yaml.load(stream)
		except yaml.YAMLError as e:
			print(e)
