
from wrapapi.http import Report
from wrapapi.settings import Settings
from wrapapi.validations.assertions import SoftAsserts
from wrapapi.web import Application


class TestSuite(object):

    app = None
    check = None

    def setup_method(self, method):
        app_settings = Settings()  # default settings
        self.check = SoftAsserts()
        self.app = Application(app_settings)

    def teardown_method(self):
        self.app.close()
        if self.check.errors:
            msg = Report(self.app.response, self.check.errors)
            raise AssertionError(msg)

        self.app = None
        self.check = None
