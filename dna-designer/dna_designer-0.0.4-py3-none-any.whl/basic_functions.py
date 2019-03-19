import numpy as np

end_codons = {
    'M': 'ATG',
    'W': 'TGG',
    'F': 'TTT',
    'L': 'CTG',
    'I': 'ATT',
    'V': 'GTG',
    'S': 'TCC',
    'P': 'CCA',
    'T': 'ACC',
    'A': 'GCC',
    'Y': 'TAC',
    'H': 'CAT',
    'Q': 'CAG',
    'N': 'AAC',
    'K': 'AAG',
    'D': 'GAT',
    'E': 'GAG',
    'C': 'TGC',
    'R': 'CGC',
    'G': 'GGC',
    '*': 'TGA'
}

typeii_enzymes = {
        "AarI" : {
            "seq" : "CACCTGC",
            "jump" : 4,
            "overhang" : 4
            },
        "BbsI" : {
            "seq" : "GAAGAC",
            "jump" : 2,
            "overhang" : 4
            },
        "BfuAI" : {
            "seq" : "ACCTGC",
            "jump" : 4,
            "overhang" : 4
            },
        "BsaI" : {
            "seq" : "GGTCTC",
            "jump" : 1,
            "overhang" : 4
            },
        "BsmBI" : {
            "seq" : "CGTCTC",
            "jump" : 1,
            "overhang" : 4
            },
        "BtgZI" : {
            "seq" : "GCGATG",
            "jump" : 10,
            "overhang" : 4
            },
        "SapI" : {
            "seq" : "GCTCTTC",
            "jump" : 1,
            "overhang" : 3
            }
        }

other_seq = {
        "I-SceI": "TAGGGATAACAGGGTAAT",
        "homopolymerA": "AAAAAAAA",
        "homopolymerT": "TTTTTTTT",
        "homopolymerG": "GGGGGGGG",
        "homopolymerC": "CCCCCCCC"
        }

biobricks_enzymes = {
        "EcorI":"GAATTC",
        "XbaI":"TCTAGA",
        "SpeI":"ACTAGT",
        "PstI":"CTGCAG",
        "NotI":"GCGGCCGC"}

def reverse_complement(seq):
    '''Creates reverse complement of a DNA string.'''
    seq = seq.upper()
    return seq.translate(str.maketrans("ATGCN","TACGN"))[::-1]

def reverse_complement_list(seqs:list)->list:
    reverse = []
    for seq in seqs:
        reverse.append(reverse_complement(seq))
    return seqs+reverse

def random_dna_sequence(length):
    return ''.join(np.random.choice(('A', 'C', 'T', 'G')) for _ in range(length))
