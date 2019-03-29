
__author__ = "Yury D."
__credits__ = ["Yury D.", "Some Dude", "Some Dudette"]
__license__ = "MIT"
__version__ = "0.5.8"
__maintainer__ = "Yury D."
__email__ = "SoulGate@yandex.ru"
__status__ = "Alpha"

class PythonReleaseTest:
    """
    Python Release Test Class
    """
    def __init__(self):
        self.variable = 1

    def execute(self):
        """
        Some function
        :return: value of self.variable
        """
        print("Python Release Test, variable="+str(self.variable))
        return self.variable