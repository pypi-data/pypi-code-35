from .basic_functions import other_seq,typeii_enzymes,random_dna_sequence,reverse_complement_list, biobricks_enzymes

iscei = other_seq['I-SceI']
banned = reverse_complement_list([value['seq'] for key,value in typeii_enzymes.items()])+ [letter*8 for letter in ['A','T','G','C']] + reverse_complement_list([value for key,value in biobricks_enzymes.items()])

def barcode(enzyme:str=iscei,banned:list=banned, length:int=21, silent:bool=True)-> str:
    '''Creates a DNA barcode consisting of an enzyme flanked by two equal length random dna sequences that do not contain any banned sequences'''
    full_barcode = random_dna_sequence(length) + enzyme + random_dna_sequence(length)
    for ban in banned:
        if ban in full_barcode:
            if silent != True:
                print('FOUND {}'.format(ban))
            return barcode()
    return full_barcode

