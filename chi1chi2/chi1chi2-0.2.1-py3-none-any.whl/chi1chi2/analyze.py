#!/usr/bin/env python
from optparse import OptionParser

from chi1chi2.core.property_reader import PropsBulk
from chi1chi2.utils.constants import resolve_path, OUT_FILENAME_PATTERN

usage = """
%prog [options]
pogram for analysis of the calculations resluts:
- optical indicatrix
- refractive indices
- rotation of chi(1) and chi(2) tensors
- reporting of the properties as a function of the wavelength

required input:
- name of the bulk properties (chi1, chi2)
optional input:
- name of the analysis file

default output:
- analysis output file
"""
parser = OptionParser(usage=usage)

parser.add_option("-i", "--input-file", dest="input_file", help="input file (R)", action="store", type="string",
                  default=None)
parser.add_option("-o", "--output-file", dest="output_file", help="output file", action="store", type="string",
                  default=None)

(options, args) = parser.parse_args()


def run():
    if options.input_file is None:
        parser.error("Provide required input parameters; check usage with --help")

    properties = PropsBulk.from_file(options.input_file)

    property_output = properties.get_analysis_report()

    print(property_output)

    if options.output_file is None:
        options.output_file = resolve_path(options.input_file, OUT_FILENAME_PATTERN, "_analysis.out")
        with open(options.output_file, 'w') as fh:
            fh.writelines(property_output)


if __name__ == '__main__':
    run()
