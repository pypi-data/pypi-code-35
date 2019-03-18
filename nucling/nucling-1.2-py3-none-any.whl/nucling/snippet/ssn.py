import re


def clean_ssn( ssn ):
    return re.sub( r'[-_]', '', ssn )


def is_full( ssn ):
    return len( clean_ssn( ssn ) ) == 9
