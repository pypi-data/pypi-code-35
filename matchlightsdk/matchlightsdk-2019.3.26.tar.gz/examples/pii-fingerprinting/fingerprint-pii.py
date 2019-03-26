'''
This module contains an example script showing how to upload PII
data using the Matchlight SDK.
'''

import csv
import uuid

from matchlight import Matchlight


def get_pii_data():
    '''Get the plain text PII data to fingerprint.

    This is just a placeholder for any function that loads plaintext
    data, in practice this could pull data in from anywhere: a
    database, a CSV, another API, etc.
    '''
    return [
        {
            'email': 'richardwoodward@gardner.biz',
            'first_name': 'Preston',
            'last_name': 'Wiggins',
            'address': '83037 Amy Lodge',
            'city': 'Alexanderstad',
            'state': 'New Mexico',
            'zipcode': '81075',
            'phone': '1035223952',
            'ssn': '129602039',
            'credit_card': '4916528483361601'
        },
        {
            'email': 'daniel58@gmail.com',
            'first_name': 'Edward',
            'last_name': 'Figueroa',
            'address': 'Unit 1041 Box 1550',
            'city': 'Brendamouth',
            'state': 'South Carolina',
            'zipcode': '07721',
            'phone': '(434)191-8466',
            'ssn': '096571603',
            'credit_card': '4532566428800162'
        },
        {
            'email': 'gregory39@schultz.com',
            'first_name': 'Hunter',
            'last_name': 'Hill',
            'address': 'PSC 5552, Box 2365',
            'city': 'Martinshire',
            'state': 'Mississippi,67262',
            'zipcode': '32334',
            'phone': '9338226',
            'ssn': '261500223',
            'credit_card': '5569181104928858'
        }
    ]


def save_formatted_data(formatted_data):
    with open('formatted-data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=formatted_data[0].keys()
        )
        writer.writeheader()
        for item in formatted_data:
            writer.writerow(item)


def main():
    '''Fingerprint PII data and upload to Matchlight.'''
    plaintext_pii_data = get_pii_data()

    # Add a unique `user_record_id` to each record as an index to
    # connect plaintext data back to Matchlight fingerprints.
    for record in plaintext_pii_data:
        record.update({'user_record_id': uuid.uuid4()})

    # Tip: You should save this formatted plaintext output so you will
    # be able to connect Matchlight alerts back to source input data
    # using the `user_record_id` field.
    save_formatted_data(plaintext_pii_data)

    # Tip: You can generate your Matchlight API keys through the
    # Matchlight web interface
    # https://python-matchlightsdk.readthedocs.io/en/latest/guide.html?highlight=keys#authentication
    ml = Matchlight(
        access_key='your-matchlight-api-access-key',
        secret_key='your-matchlight-api-secret-key'
    )
    # Tip: Make sure you have already created a project
    # https://python-matchlightsdk.readthedocs.io/en/latest/guide.html#create-a-new-project
    project = ml.projects.get('your-project-upload-token')

    total_records = len(plaintext_pii_data)
    for counter, record in enumerate(plaintext_pii_data):
        print(
            f'Uploading {record["email"]} '
            f'({counter + 1} of {total_records})'
        )
        ml.records.add_pii(
            project=project,
            description='Created from SDK example script',
            email=record['email'],
            first_name=record['first_name'],
            middle_name=None,
            last_name=record['last_name'],
            ssn=record['ssn'],
            address=record['address'],
            city=record['city'],
            state=record['state'],
            zipcode=record['zipcode'],
            phone=record['phone'],
            credit_card=record['credit_card'],
            user_record_id=str(record['user_record_id'])
        )


if __name__ == '__main__':
    main()
