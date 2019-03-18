import csv
import json

def csv_to_json(path_to_file):
    with open( path_to_file) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        json_data = json.dumps( [ row for row in csv_reader ] )
        json_data = json.loads(json_data, encoding='utf8')
        return json_data