from abc import abstractmethod
from tmg_etl_library.components.component import Component


class Database(Component):
    def __init__(self, log):
        super().__init__(log)

    @abstractmethod
    def list_tables(self, table_regex=''):
        pass

    @abstractmethod
    def run_query(self, query, config):
        pass

