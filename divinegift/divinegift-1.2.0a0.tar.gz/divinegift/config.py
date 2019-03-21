from divinegift.logger import log_info, log_err, log_warning
from divinegift.cipher import read_key, encrypt_str, decrypt_str, get_key, write_key
try:
    from divinegift.main import dict_compare, Yaml, Json
except:
    pass
#########################################################################


class Settings:
    def __init__(self):
        self.settings = {}
        self.cipher_key = None

    def get_settings(self):
        return self.settings

    def set_settings(self, json_str: object):
        self.settings = json_str

    def parse_settings(self, file_: str = './settings.conf', encoding: str = 'utf-8', log_changes: bool = True, use_yaml=True):
        """
        Parse settings from file_
        :param file_: Filename with settings
        :param encoding: Encoding
        :return: None
        """
        if use_yaml:
            c = Yaml(file_, encoding=encoding)
        else:
            c = Json(file_, encoding=encoding)

        json_data = c.parse()

        if log_changes and json_data:
            dict_c = dict_compare(self.settings, json_data)
            added, removed, modified, same = dict_c.values()
            if len(added) > 0:
                for r in list(added):
                    log_warning(f'Added {r}: {json_data.get(r)}')
            if len(removed) > 0:
                for r in list(removed):
                    log_warning('Removed {}: {}'.format(r, self.settings.get(r)))
            if len(modified) > 0:
                for r in list(modified):
                    log_warning('Modified {}: {} -> {}'.format(r, modified.get(r)[0], modified.get(r)[1]))
        elif log_changes and not json_data:
            raise Exception('Settings not parsed. Is there any data?')

        self.set_settings(json_data)

    def initialize_cipher(self, ck_fname: str = 'key.ck'):
        self.cipher_key = get_key()
        write_key(ck_fname, self.cipher_key)

    def encrypt_password(self, conn_name: str, ck_fname: str = 'key.ck'):
        if not self.cipher_key:
            self.cipher_key = read_key(ck_fname)
            if not self.cipher_key:
                self.initialize_cipher()
        cipher = get_cipher(self.cipher_key)
        self.settings[conn_name]['db_pass'] = encrypt_str(self.settings[conn_name]['db_pass'], cipher)

    def decrypt_password(self, conn_name: str, ck_fname: str = 'key.ck'):
        if not self.cipher_key:
            self.cipher_key = read_key(ck_fname)
        cipher = get_cipher(self.cipher_key)
        self.settings[conn_name]['db_pass'] = decrypt_str(self.settings[conn_name]['db_pass'], cipher)

    def encode_password(self, conn_name: str):
        settings = self.get_settings().copy()
        settings[conn_name]['db_pass'] = encode_password(settings[conn_name]['db_pass'])
        self.set_settings(settings)

    def decode_password(self, conn_name: str):
        settings = self.get_settings().copy()
        settings[conn_name]['db_pass'] = decode_password(settings[conn_name]['db_pass'])
        self.set_settings(settings)

    def save_settings(self, file_: str = './settings.conf', encoding='utf-8', use_yaml=True):
        if use_yaml:
            c = Yaml(file_, encoding=encoding)
        else:
            c = Json(file_, encoding=encoding)
        c.set_data(self.get_settings())
        c.create()


if __name__ == '__main__':
    pass
