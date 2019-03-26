import csv
import json

from matchlight import Matchlight


def get_document_data():
    output = []
    with open('formatted-data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            output += [row]
    return output


def generate_fingerprints(document_data):
    '''Generate fingerprints but do not upload them to Matchlight.'''
    # Tip: Your access and secret keys can be blank here because we're
    # not uploading anything yet.
    ml = Matchlight(access_key='', secret_key='')

    fingerprinted_data = []
    for counter, item in enumerate(document_data):
        fingerprint_json_blob = ml.records.add_document(
            project='',
            name=item['name'],
            description=item['desc'],
            content=item['data'],
            user_record_id=item['user_record_id'],
            offline=True
        )
        fingerprinted_data += [fingerprint_json_blob]
    return fingerprinted_data


def save_fingerprints(fingerprinted_data):
    '''Save a local copy of the fingerprinted data.

    Using JSON instead of CSV because the fingerprinted data is nested
    as opposed to flat.
    '''
    with open('fingerprints.json', 'w', newline='') as jsonfile:
        json.dump(fingerprinted_data, jsonfile)


def main():
    '''Create an offline set of Matchlight document fingerprints.'''
    document_data = get_document_data()
    fingerprinted_data = generate_fingerprints(document_data)
    save_fingerprints(fingerprinted_data)
    print(f'Fingerprinted {len(fingerprinted_data)} records')


if __name__ == '__main__':
    main()
