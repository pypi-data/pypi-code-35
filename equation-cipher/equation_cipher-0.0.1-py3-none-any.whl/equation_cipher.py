"""
File contains the core of algorithm to encrypt the string passed to it.
"""
import datetime
import base64


class Encrypter(object):
    """
    This class will work for encrypting any string which is passed to it, in
    Equation cipher form.
    """
    def encrypt_by_date(self, target: str,
                        date_for_encryption: datetime) -> str:
        """
        This function will accept the date and time separately for encryption.
        :param target: <data type: str>
        :param date_for_encryption: <data type: datetime>
        :return: <data type: str(bytes)>
        """
        equation = self.__form_equation(target, date_for_encryption)
        final_str = equation + "@" + date_for_encryption.strftime(
            "%m/%d/%Y,%H:%M:%S")
        final_byte_string = b'' + final_str
        base_encoded = base64.b64encode(final_byte_string)
        return base_encoded

    def encrypt(self, target: str) -> str:
        """
        Function to encrypt any string with equation encryption form.
        :param target: <data type: str>
        :return: <data type: str(bytes)>
        """
        date_obj = datetime.datetime.now()
        equation = self._form_equation(target, date_obj)
        final_str = equation + "@" + date_obj.strftime("%m/%d/%Y,%H:%M:%S")
        base_encoded = base64.b64encode(final_str.encode('utf-8'))
        return base_encoded

    def __get_mult_and_pow(self, char: str, date_obj: datetime) -> (int, int):
        """
        Returns the multiplier of the character to be encrypted.
        :param char: <data type: str>
        :param date_obj: <data type: datetime>
        :return: <data type: tuple>
        """
        addition_factor = date_obj.day + date_obj.month + date_obj.year
        mult = None
        pow_val = None

        if char.isalpha():
            char_ord = (ord(char) + addition_factor) % 26
            mult = (char_ord % 10) + 1
            pow_val = (char_ord % 3) + 1

        if char.isdigit():
            mult = ord(char) + addition_factor

        else:
            pow_val = (ord(char) % 11) + 1

        return mult, pow_val

    def _form_equation(self, target: str, date_obj: datetime) -> str:
        """
        Returns the encrypted equation which is formed using the datetime and
        passed target.
        :param target: <data type: str>
        :param date_obj: <data type: datetime>
        :return: <data type: str>
        """
        equation = str()
        multi_factor = date_obj.hour + date_obj.minute + date_obj.second

        for char in target:
            mult, pow_val = self.__get_mult_and_pow(char, date_obj)

            if not pow_val:
                equation += "+"+str(mult * multi_factor)

            elif not mult:
                power = pow_val + multi_factor
                term = "-Y^" + str(power)
                equation += term

            elif mult and pow_val:
                multiplier = mult * multi_factor
                power = pow_val + multi_factor
                if char.isupper():
                    term = "+"+str(multiplier)+"x^"+str(power)
                else:
                    term = "+" + str(multiplier) + "X^" + str(power)
                equation += term

        return equation


if __name__ == "__main__":
    # this part of code is written so that user can
    # check how the string is encrypted.
    enc = Encrypter()
    print("hello@123 encoded to: --")
    print(enc.encrypt("hello@123"))
