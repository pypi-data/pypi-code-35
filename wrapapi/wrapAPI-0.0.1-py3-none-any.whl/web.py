
from wrapapi import Settings
from wrapapi.http import AppRequest, Report


class Application(object):

    def __init__(self, config: Settings = None):
        self.config = config or Settings()
        self._session = None
        self.response = None

    def __repr__(self) -> str:
        return f'<App {self.config}>'

    def create(self):
        self._session = AppRequest(self.config)
        return self._session

    def reset(self):
        # TODO make method in request class
        self._session.errors = []
        self.build_report()
        return True

    def refresh(self):
        self.reset()
        self.close()
        return self.create()

    def close(self) -> bool:
        # TODO make method in request class
        self._session._session.close()
        self._session = None
        return True

    def build_report(self) -> Report:
        return self._session.report.build()
