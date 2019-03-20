import numpy as np
import textwrap
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class BaseEvaluator(object):
    def __init__(self):
        print('======================================================')
        print('AImageLab OLJ')
        print('======================================================')
        self.run_tests()

    def run_tests(self):
        counter_passed = 0
        for i, t in enumerate(self.tests):
            sys.stdout.write('Test %i/%i (%s)...' % (i+1, len(self.tests), t.__name__))
            #try:
            passed, message = t()
            #except:
            #    passed = False
            #    message = 'Exception thrown.'
            if passed:
                print(bcolors.OKGREEN, 'PASSED', bcolors.ENDC)
                counter_passed += 1
            else:
                print(bcolors.FAIL, 'NOT PASSED', bcolors.ENDC)
                if message:
                    print(textwrap.indent(message, '  '))
                break
        print('======================================================')
        print('%i out of %i test passed.' % (counter_passed, len(self.tests)))
        print('======================================================')

    def inputs(self):
        raise NotImplementedError

    def assertAllClose(self):
        inputs = self.inputs()
        expected = self.Fn(*inputs)
        actual = self.fn(*inputs)
        if not np.allclose(expected, actual):
            msg = "Using the following inputs:\n"
            for input in inputs:
                msg += str(input) + "\n"
            msg += "function '%s' returned a wrong output\n" % self.fn.__name__
            msg += "Expected output:\n" + str(expected) + "\n"
            msg += "Returned output:\n" + str(actual) + "\n"
            return False, msg
        return True, None

    def assertType(self):
        inputs = self.inputs()
        expected = type(self.Fn(*inputs))
        actual = type(self.fn(*inputs))
        if not expected == actual:
            msg = "Function '%s' returned a wrong output type\n" % self.fn.__name__
            msg += "Expected type: %s\n" % str(expected)
            msg += "Returned type: %s\n" % str(actual)
            return False, msg
        return True, None

    def assertAttribute(self, attribute):
        def fn():
            inputs = self.inputs()
            expected = getattr(self.Fn(*inputs), attribute)
            actual = getattr(self.fn(*inputs), attribute)
            if not expected == actual:
                msg = "Function '%s' returned a wrong %s\n" % (self.fn.__name__, attribute)
                msg += "Expected %s:\n" % attribute + str(expected) + "\n"
                msg += "Returned %s:\n" % attribute + str(actual) + "\n"
                return False, msg
            return True, None
        fn.__name__ = 'assert'+attribute.title()
        return fn