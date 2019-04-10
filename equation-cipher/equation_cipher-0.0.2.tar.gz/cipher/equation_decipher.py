"""
Contains the methods to decipher the equation cipher method.
"""
import base64
import datetime
import sys
sys.path.append('..')

from cipher.equation_cipher import Encrypter


class Decrypter(Encrypter):
    """
    Class to decrypt the equation cipher encryption.
    Note: This decryption can not be done complete decryption but partial
    decryption can be done and string passed can be verified at some stage of
    encryption.
    """

    def match_deceypt(self, target: str, hash_str: bytes) -> bool:
        """
        Checks if the passed hash_str is representation of passed
        target string or not.
        :param target: <data type: str>
        :param hash_str: <data type: str(bytes)>
        :return: <data type: bool>
        """
        decrypted_hash = base64.b64decode(hash_str).decode('utf-8')
        equation = decrypted_hash.split('@')[0]
        date_obj = datetime.datetime.strptime(decrypted_hash.split('@')[1],
                                              '%m/%d/%Y,%H:%M:%S')
        en_str = self._form_equation(target, date_obj)

        return True if equation == en_str else False


# below code snippet is been written for user to  check working
if __name__ == '__main__':
    dec_obj = Decrypter()
    result = dec_obj.match_deceypt('hello@123',
                          b'KzE4MFheNDIrNzJYXjM5KzMyNFheNDYrMzI0WF40Nis3MlheM'
                          b'zgtWV40Nis3NDkxNis3NDk1Mis3NDk4OEAwNC8wOS8yMDE5LD'
                          b'EyOjE3OjA3')
    print('result', result)
