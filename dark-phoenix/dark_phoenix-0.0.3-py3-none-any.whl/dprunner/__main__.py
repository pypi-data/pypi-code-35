import unittest
import HtmlTestRunner
import argparse


def run_test_in_multiple_module_file_generate_html_report(testfolder, reportname,  reporttitle, reportdir):

    # Load all test case class.
    test_loader = unittest.TestLoader()
    all_test_cases = test_loader.discover(start_dir=testfolder, pattern='*.py')

    # Create HtmlTestRunner object and run the test suite.
    test_runner = HtmlTestRunner.HTMLTestRunner(
        combine_reports=True, report_name=reportname, report_title=reporttitle, output=reportdir)

    test_runner.run(all_test_cases)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--html', action='store_true',
                        help='Create html output')
    parser.add_argument('--testfolder', default='.',
                        help='Folder containing test')
    parser.add_argument('--reportname', default='Report_Name',
                        help='Name of the report file')
    parser.add_argument(
        '--reporttitle', default='Test results', help='Title of the report')
    parser.add_argument('--reportdir', default='html_report',
                        help='Html report directory')
    options, args = parser.parse_known_args()

    run_test_in_multiple_module_file_generate_html_report(str(options.testfolder), str(options.reportname),
                                                          str(options.reporttitle), str(options.reportdir))
