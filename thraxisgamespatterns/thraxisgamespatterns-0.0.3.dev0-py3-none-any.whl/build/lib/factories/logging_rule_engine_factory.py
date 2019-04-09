import logging

from factories.abstract_factory import TGAbstractFactory
from rules.logging_rule_engine import TGLoggingRuleEngine


class TGLoggingRuleEngineFactory(TGAbstractFactory):

    def create(self, options=None):
        return TGLoggingRuleEngine(logging.getLogger())
