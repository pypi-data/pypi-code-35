class LanguageCodes(object):
    sanskrit = 'sa'

    def get_all_language_codes(self):
        return [self.sanskrit]


class LMConfigs(object):
    all_language_codes = LanguageCodes()
    lm_model_file_url = {
        all_language_codes.sanskrit: 'https://www.dropbox.com/s/4ay1by5ryz6k39l/sanskrit_export.pkl?raw=1'
    }
    tokenizer_model_file_url = {
        all_language_codes.sanskrit: 'https://www.dropbox.com/s/e13401nsekulq17/tokenizer.model?raw=1'
    }

    def __init__(self, language_code: str):
        self.language_code = language_code

    def get_config(self):
        return {
            'lm_model_url': self.lm_model_file_url[self.language_code],
            'lm_model_file_name': 'export.pkl',
            'tokenizer_model_url': self.tokenizer_model_file_url[self.language_code],
            'tokenizer_model_file_name': 'tokenizer.model'
        }

