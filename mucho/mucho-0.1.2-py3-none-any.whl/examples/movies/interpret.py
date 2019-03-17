import argparse
import logging
import sys

from mucho.dsl.compiler import Compiler
from mucho.dsl.virtualmachine import ExecutionError, VirtualMachine
from mucho.dsl.compiler import CompilationError

from examples.movies.comparators import AVWorkComparator
from examples.movies.entities import AVWork

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())


def main():
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    comparator = AVWorkComparator()
    compiler = Compiler(comparator=comparator)
    rules_text = """
    discarded: Those whose titles are very different
    titles.similarity <= 50 => mismatch
    
    perfect: Those matching almost perfectly
    titles.similarity >= 90 and years.difference < 2 => match
    
    similar: Those quite similar
    titles.similarity >= 85 and years.are_same => unknown

    last:
    (not titles.are_exact and years.are_same)
    => mismatch
    """
    try:
        rules = compiler.compile(rules_text, debug=args.verbose)
    except CompilationError as e:
        logger.error(e)
        return 3
    virtual_machine = VirtualMachine()
    try:
        work_src = AVWork(title="The Goonies", year=1985)
        work_trg = AVWork(title="The Goonie", year=1985)
        rule = virtual_machine.run(
            rules, comparator.compare(work_src, work_trg))
        if rule:
            sys.stdout.write("Rule '{0}' matched: {1}\n".format(
                rule.id, rule.result.value))
    except ExecutionError as e:
        logger.error(e)
        return 3
    return 0


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--verbose', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    sys.exit(main())
