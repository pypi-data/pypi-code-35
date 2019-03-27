import omxware
from omxware.Connect import Connection

"""
OMXWare Protein Entity Class
"""


class Protein:
    """Protein Class"""
    __omx_token = ''

    def __init__(self, connecthdr: Connection, protein):
        """Constructor"""

        if not ("PROTEIN_UID_KEY" in protein):
            raise Exception("The PROTEIN_UID_KEY is missing in the given Protein object.")

        self._jobj = protein

        self._proteinUidKey = protein['PROTEIN_UID_KEY']
        self._proteinName = protein['PROTEIN_FULLNAME']

        if 'PROTEIN_SEQUENCE' in protein:
            self._proteinSequence = protein['PROTEIN_SEQUENCE']
        else:
            self._proteinSequence = ''

        self._connecthdr = connecthdr

        config = self._connecthdr.getConfig()
        self.__omx_token = config.getOMXToken()

    def __str__(self):
        return "{ 'type': 'protein', 'uid': '" + self.get_uid() + "', 'name': '" + self.get_name() + "', 'sequence: '"+self.get_sequence()+"'}"

    def get_name(self):
        return str(self._proteinName)

    def get_sequence(self):
        return str(self._proteinSequence)

    def get_uid(self):
        return str(self._proteinUidKey)

    def genomes(self):
        omx = omxware.omxware(self.__omx_token)
        return omx.genomes_by_protein(self._proteinUidKey)

    def genera(self):
        omx = omxware.omxware(self.__omx_token)
        return omx.genera_by_protein(self._proteinUidKey)

    def toFasta(self):
        if(len(self.get_sequence().strip()) == 0):
            return ''
        else:
            fasta_content = '\n' + '>omx|protein_' + self.get_uid() + ' ' + self.get_name() + '\n' + self.get_sequence()
            return fasta_content
