from unittest import TextTestResult


class TextTestResultWithSuccesses(TextTestResult):
    """
    This class extends TextTestResult such that passing tests get reported in
    `self.successes`.

    This is necessary because TextTestResult doesn't report successes by
    default.
    """
    def __init__(self, *args, **kwargs):
        super(TextTestResultWithSuccesses, self).__init__(*args, **kwargs)
        self.successes = []

    def addSuccess(self, test):
        super(TextTestResultWithSuccesses, self).addSuccess(test)
        self.successes.append(test)
