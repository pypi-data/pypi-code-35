from enum import Enum

from .condition import Condition


class Rule:
    """Rule of the DSL"""

    class Result(Enum):
        MATCH = "MATCH"
        MISMATCH = "MISMATCH"
        UNKNOWN = "UNKNOWN"

    def __init__(
            self, id: str, description: str,
            condition: Condition, result: Result):
        """
        :param id: identifier of the rule
        :param description: description of the rule
        :param condition: condition that must be true to satisfy the rule
        :param result: result obtained if the rule is satisfied
        """
        self.id = id
        self.description = description
        self.condition = condition
        self.result = result

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.__dict__)
