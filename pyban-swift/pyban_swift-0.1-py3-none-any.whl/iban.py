import re
import textwrap

from pyban.country import Countries


class IBAN:
    def __init__(self, iban: str):
        self.iban = None

        try:
            self.__parse_iban(iban)
        except ValueError as e:
            raise e

    def __parse_iban(self, iban: str):
        """
        :param iban: str IBAN number to validate and format
        :return: None
        """
        self.iban = self.clean_iban(iban)
        self.validate_general_format(self.iban)
        self.check_country_meta(self.iban)
        self.checksum_validation(self.iban)

    @property
    def formatted(self):
        return self.format_to_readable_iban(self.iban)

    @staticmethod
    def checksum_validation(iban: str):
        """
        This function checks the IBAN if it is valid via the MOD-97 check.
        This process has the following steps to validate the IBAN:
        1 - Move first four characters (Country and checksum) to end of str
        2 - Translate all characters to integers, where A=10, ... Z = 35
            - NOTE: ord(A) returns ASCII value 65, so we can calculate the
              correct integer by subtracting offset 55
        3 - Check if the resulting integer has a remainder of 1 when applying
            MOD-97

        :param iban: str IBAN number, stripped and uppercase characters
        :return: None
        :raises: ValueError
        """
        character_list = list(iban[4:] + iban[:4])

        offset = 55  # For character to integer translation
        translated_list = map(
            lambda x: str(ord(x) - offset) if x.isalpha() else x,
            character_list)
        translated_iban = ''.join(list(translated_list))

        # Mod-97 check on translated IBAN
        iban_integer = int(translated_iban)

        if iban_integer % 97 != 1:
            raise ValueError('IBAN fails mod-97 integrity check')

    @staticmethod
    def check_country_meta(iban: str):
        """
        Fetches validation meta according to the IBAN country code (for now
        just the length of the entire IBAN).
        TODO - check formatting

        :param iban: str IBAN number, stripped and uppercase characters
        :return: None
        :raises: ValueError
        """
        countries = Countries()
        country = countries.get(alpha_2=iban[:2])
        if not country:
            raise ValueError('Invalid country code or unsupported country')

        if len(iban) != country.length:
            raise ValueError('IBAN length not conform country format')

    @staticmethod
    def validate_general_format(iban: str):
        """
        First check if the IBAN conforms to the general format. We can raise
        formatting errors early to prevent more expensive validation

        :param iban: str IBAN number, stripped and uppercase characters
        :return: None
        :raises: ValueError
        """
        iban_regex = r'^[A-Z]{2}[0-9]{2}[A-Za-z0-9]{11,32}$'
        if not re.match(iban_regex, iban):
            raise ValueError('Invalid IBAN format')

    @staticmethod
    def clean_iban(iban: str):
        """
        Sets all letters to uppercase and strips needless spaces

        :param iban: str IBAN number, stripped and uppercase characters
        :return: str stripped and upped iban
        """
        return re.sub(r' +', '', iban).upper()

    @staticmethod
    def format_to_readable_iban(iban: str):
        """
        Formats an IBAN to a consistent, readable format.
        Separates the country code and checksum from the remaining data,
         then divides it in blocks of four characters
        :param iban: str IBAN number
        :return: str readable IBAN format
        """
        iban = re.sub(r' +', '', iban).upper()
        iban_list = textwrap.wrap(iban, 4)
        country_checksum = iban_list.pop(0)
        return (
            f"{country_checksum[:2]} {country_checksum[2:4]} "
            f"{' '.join(iban_list)}")
