import re
import sys

import obitools.seqdb.genbank as gb
from obitools.seqdb import nucEntryIterator,aaEntryIterator

_featureMatcher = re.compile('^FEATURES.+\n(?=ORIGIN)',re.DOTALL + re.M)

_headerMatcher = re.compile('^LOCUS.+(?=\nFEATURES)', re.DOTALL + re.M)
_seqMatcher    = re.compile('(?<=ORIGIN).+(?=//\n)', re.DOTALL + re.M)
_cleanSeq      = re.compile('[ \n0-9]+')
_acMatcher     = re.compile('(?<=^ACCESSION   ).+',re.M)
_deMatcher     = re.compile('(?<=^DEFINITION  ).+\n( .+\n)*',re.M)
_cleanDe       = re.compile('\n *')

def __gbparser(text):
    try:
        header = _headerMatcher.search(text).group()
        ft     = _featureMatcher.search(text).group()
        seq    = _seqMatcher.search(text).group()
        seq    = _cleanSeq.sub('',seq).upper()
        acs    = _acMatcher.search(text).group()
        acs    = acs.split()
        ac     = acs[0]
        acs    = acs[1:]
        de     = _deMatcher.search(header).group()
        de     = _cleanDe.sub(' ',de).strip().strip('.')
    except Exception as e:
        print>>sys.stderr, "\nCould not import sequence id:", text.split()[1], "(error raised:", e, ")"
        # Do not raise any Exception if you need the possibility to resume the generator
        # (Python generators can't resume after any exception is raised)
        return None
    
    return (ac,seq,de,header,ft,acs)


def genbankParser(text):
    parsed_text = __gbparser(text)
    if parsed_text is not None:
        return gb.GbSequence(*parsed_text)
    else:
        return None
    
    
def genbankIterator(file):
    for e in nucEntryIterator(file):
        yield genbankParser(e)
    
    
def genpepParser(text):
    parsed_text = __gbparser(text)
    if parsed_text is not None:
        return gb.GpepSequence(*parsed_text)
    else:
        return None
    
    
def genpepIterator(file):
    for e in aaEntryIterator(file):
        yield genpepParser(e)
    
    