import logging
import os
import re
from typing import List

from lark import Lark
from lark.exceptions import VisitError

from mucho.comparison.comparator import EntityComparator
from mucho.dsl.compiler.transformer import RulesTransformer
from mucho.dsl.compiler.transformer.model import Rule

logger = logging.getLogger(__name__)


class Compiler:
    """Compiles the string with the defined rules into its equivalent object
    representation."""

    _GRAMMAR_FILE_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'grammar', 'rules.lrk',
    )
    _GRAMMAR_RULE_START = 'rules'

    def __init__(
            self,
            grammar_file_path: str = _GRAMMAR_FILE_PATH,
            grammar_rule_start: str = _GRAMMAR_RULE_START,
            comparator: EntityComparator = None,
    ):
        """
        :param grammar_file_path: path of the file containing the grammar of
        the DSL in Extended Backus-Naur form (EBNF).
        :param grammar_rule_start: name of the rule in which the analysis
        starts
        :param comparator: the comparator that generates the context to be used
        during the evaluation of the rules. If specified, the transformer will
        make sure that the names of the variables used in the definition of the
        rules match the names of the dimension comparators and properties
        defined in the entity comparator.
        """
        self._file_path_grammar = grammar_file_path
        self._grammar_rule_start = grammar_rule_start
        self._comparator = comparator
        self._parser = Lark(
            open(self._file_path_grammar), start=self._grammar_rule_start)
        self._transformer = RulesTransformer(comparator)

    def compile(self, text: str, debug: bool = False) -> List[Rule]:
        """Compiles the text with the defined rules into its equivalent object
        representation.

        :param text: text with the rules defined according to the DSL
        :param debug: if True, some debug messages are logged during the
        compilation process
        :return: list of objects representing the defined rules
        """
        tree = self._parser.parse(text)
        if debug:
            logger.debug(tree.pretty())
        try:
            return self._transformer.transform(tree)
        except VisitError as e:
            raise CompilationError.create(e)


class CompilationError(Exception):
    """Error generated during the compilation process."""

    _RE_MSG_BOILERPLATE = re.compile(
        r'^Error trying to process rule "[^"]+":\n\n(.+)$')

    @classmethod
    def create(cls, exception: Exception) -> 'CompilationError':
        """ Instantiates the error and sets its message to the message of the
        error param.

        :param exception: error from which the message is taken
        :return: instance of the compilation error
        """
        message = str(exception)
        if isinstance(exception, VisitError):
            match = cls._RE_MSG_BOILERPLATE.match(exception.args[0])
            if match:
                message = match.groups()[0]
        return cls(message)
