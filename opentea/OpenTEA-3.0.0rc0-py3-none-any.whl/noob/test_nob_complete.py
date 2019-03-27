""" Testing the nob complete and the nob print functions"""

import json
from opentea.noob.inferdefault import nob_complete
from opentea.noob.asciigraph import nob_asciigraph


def create_dummy():
    """create a dummy nested object for testing purposes"""

    dummy = dict()
    # Checking the standard nodes
    dummy['controle_existif_require'] = dict()
    dummy['controle_existif_require']['controle'] = dict()
    dummy['controle_existif_require']['controle'] = dict()
    dummy['controle_existif_require']['controle']['controle_ei'] = True
    # Checking the case of a choice
    dummy['ouexclusif'] = dict()
    dummy['ouexclusif']['ouex_mod'] = dict()
    dummy['ouexclusif']['ouex_mod']['modele_a_2'] = dict()
    # Checking the case of uncompatible types of values
    dummy['ouexclusif']['ouex_mod']['modele_a_2']['desc'] = 15

    # Checking the case of an array (a multiple)
    dummy['multiple'] = dict()
    dummy['multiple']['mul_cont'] = []
    array_element_1 = dict()
    array_element_2 = dict()
    array_element_3 = dict()
    array_element_4 = dict()

    # Check the auto completion of item name if none provided
    array_element_1['name'] = 'p1'
    array_element_2['name'] = 'p2'
    # Check the auto completion of array item children
    array_element_1['bcliq'] = dict()
    array_element_2['bnd_gas'] = dict()
    array_element_3['bcliq'] = dict()
    # Check if the elements not contained in the schema are auto-cleaned
    array_element_1['bcliq']['outlet'] = {'pressure': 400.,
                                          'temperature': 800.,
                                          'Unwanted element': 1989}

    array_element_2['bnd_gas']['inlet7'] = {'pressure': "junk_pressure",
                                            'temperature': 800.}

    dummy['multiple']['mul_cont'].append(array_element_1)
    dummy['multiple']['mul_cont'].append(array_element_2)
    dummy['multiple']['mul_cont'].append(array_element_3)
    dummy['multiple']['mul_cont'].append(array_element_4)

    return dummy


def main():
    """Test the nob complete and the nob print functions"""
    schema_file = 'schema.json'
    with open(schema_file, "r") as fin:
        schema = json.load(fin)
    nob = create_dummy()
    schema_file = 'dmmy.json'
    with open(schema_file, "w") as fout:
        json.dump(nob, fout, indent=4)
    
    nob_c = nob_complete(schema, update_data=nob)
    # nob_c = nob_complete(schema, dummy_items=True)
    # nob_c = nob_complete(schema, dummy_items=False)
    nob_asciigraph(nob_c)


if __name__ == '__main__':
    main()
