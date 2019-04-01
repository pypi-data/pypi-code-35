class BidsGenerator:

    def __init__(self):
        self.dictionary = None
        self.valid = False
        self.subject = None
        self.session = None
        self.acq = None
        self.ce = None
        self.rec = None
        self.run = None
        self.mod = None
        self.task = None
        self.dir = None
        self.suffix = None


    def parse_row(self, pd_row):

        self.dictionary = pd_row.to_dict()
        self.subject = self.dictionary['subject.label']
        self.session = self.dictionary['session.label']
