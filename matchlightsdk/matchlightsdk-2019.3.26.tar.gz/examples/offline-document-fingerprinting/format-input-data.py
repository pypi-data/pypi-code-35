import uuid
import csv


def get_unformatted_data():
    '''Get the plain text document data to fingerprint.

    This is just a placeholder for any function that loads plaintext
    data, in practice this could pull data in from anywhere: a
    database, a CSV, another API, etc.
    '''
    return [{
        'name': 'Internal Record #53',
        'desc': 'Dataset 15 from 2019-01',
        'data': (
            'Ye on properly handsome returned throwing am no whatever. '
            'In without wishing he of picture no exposed talking minutes. '
            'Curiosity continual belonging offending so explained it '
            'exquisite. Do remember to followed yourself material mr '
            'recurred carriage. High drew west we no or at john. About or '
            'given on witty event. Or sociable up material bachelor bringing '
            'landlord confined. Busy so many in hung easy find well up. So '
            'of exquisite my an explained remainder. Dashwood denoting '
            'securing be on perceive my laughing so. Improve him believe '
            'opinion offered met and end cheered forbade. Friendly as '
            'stronger speedily by recurred. Son interest wandered sir '
            'addition end say. Manners beloved affixed picture men ask. '
            'Explain few led parties attacks picture company. On sure fine '
            'kept walk am in it. Resolved to in believed desirous unpacked '
            'weddings together. Nor off for enjoyed cousins herself. '
            'Little our played lively she adieus far sussex. Do theirs '
            'others merely at temper it nearer. '
        )
    }]


def segment_input(input_data, length=840):
    '''Split strings into a list of 840 character strings.'''
    segmented_data = []
    quotient, remainder = divmod(len(input_data), length)
    for i in range(quotient):
        segmented_data += [input_data[i * length:(i + 1) * length]]
    if remainder != 0:
        segmented_data += [input_data[-remainder:]]
    return segmented_data


def format_data(unformatted_data):
    formatted_data = []
    for item in unformatted_data:
        for counter, data_segment in enumerate(segment_input(item['data'])):
            output_line = {}
            output_line['user_record_id'] = uuid.uuid4()
            output_line['data'] = data_segment
            output_line['name'] = f'{item["name"]}-{counter + 1}'
            output_line['desc'] = item['desc']
            formatted_data += [output_line]
    return formatted_data


def save_formatted_data(formatted_data):
    # Tip: You should save this formatted plaintext output so you will
    # be able to connect Matchlight alerts back to source input data.
    with open('formatted-data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=formatted_data[0].keys()
        )
        writer.writeheader()
        for item in formatted_data:
            writer.writerow(item)


def main():
    unformatted_data = get_unformatted_data()
    print(f'Read in {len(unformatted_data)} unformatted records')
    formatted_data = format_data(unformatted_data)
    save_formatted_data(formatted_data)
    print(f'Saved {len(formatted_data)} formatted records')


if __name__ == '__main__':
    main()
