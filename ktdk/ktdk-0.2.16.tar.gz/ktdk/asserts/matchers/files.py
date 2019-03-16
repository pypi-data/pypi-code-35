from pathlib import Path

from ktdk.asserts.matchers import GeneralMatcher


class FileExists(GeneralMatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol='is')
        self.message = self.message or 'File not Exists'

    def predicate(self, orig):
        orig = Path(orig)
        return orig.exists()
