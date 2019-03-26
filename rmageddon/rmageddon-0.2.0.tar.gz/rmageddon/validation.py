import difflib
import logging


class RAnalysisValidation:

    def __init__(self, R_analysis_result_one, R_analysis_result_two):
        self.R_analysis_result_one = R_analysis_result_one
        self.R_analysis_result_two = R_analysis_result_two
        self.failed = []
        self.warned = []
        self.passed = []

    def diff(self):
        """
        Performs a diff on two R analysis result files

        :param R_analysis_result_one
        :param R_analysis_result_Two:
        """
        with open(self.R_analysis_result_one, 'r') as R_analysis_one:
            with open(self.R_analysis_result_two, 'r') as R_analysis_two:
                diff = list(difflib.unified_diff(
                    R_analysis_one.readlines(),
                    R_analysis_two.readlines(),
                    fromfile='R_analysis_one',
                    tofile='R_analysis_two',
                ))
                failures = len(diff)
                if failures == 0:
                    self.passed.append((1, "No differences found"))
                else:
                    for line in diff:
                        self.failed.append((1, line))

    def print_results(self):
        logging.info("===========\n VALIDATION RESULTS\n=================\n" +
                     "{0:>4} build steps passed".format(len(self.passed)) +
                     "{0:>4} build steps had warnings".format(len(self.warned)) +
                     "{0:>4} build steps failed".format(len(self.failed))
                     )
        if len(self.passed) > 0:
            logging.debug(
                "Test Passed:\n  {}".format("\n  ".join(["#{}: {}".format(eid, msg) for eid, msg in self.passed])))
        if len(self.warned) > 0:
            logging.warning(
                "Test Warnings:\n  {}".format("\n  ".join(["#{}: {}".format(eid, msg) for eid, msg in self.warned])))
        if len(self.failed) > 0:
            logging.error(
                "Test Failures:\n  {}".format("\n  ".join(["#{}: {}".format(eid, msg) for eid, msg in self.failed])))
