class InvalidTaxIDException(Exception):
    def __init__(self):
        Exception.__init__(self, 'Invalid Tax ID')


class InvalidCPFException(InvalidTaxIDException):
    def __init__(self):
        Exception.__init__(self, 'Invalid CPF')


class InvalidCNPJException(InvalidTaxIDException):
    def __init__(self):
        Exception.__init__(self, 'Invalid CNPJ')
