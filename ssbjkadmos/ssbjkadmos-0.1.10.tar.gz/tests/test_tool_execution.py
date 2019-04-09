from __future__ import absolute_import, division, print_function

import os
import unittest

from ssbjkadmos.tools.aerodynamics.Aerodynamics import Aerodynamics
from ssbjkadmos.tools.dpdxcalc.DpdxCalc import DpdxCalc
from ssbjkadmos.tools.outputfunctions.Constraints import Constraints
from ssbjkadmos.tools.outputfunctions.Objective import Objective
from ssbjkadmos.tools.performance.Performance import Performance
from ssbjkadmos.tools.propulsion.Propulsion import Propulsion
from ssbjkadmos.tools.structures.Structures import Structures


class TestSsbjToolExecution(unittest.TestCase):
    """Run all the tools from the ssbjkadmos/tools folder in test mode."""

    # General test settings
    TOOL_LIST = ['aerodynamics', 'dpdxcalc', 'outputfunctions',
                 'performance', 'propulsion', 'structures']
    FMT_SKIP_MSG = '{} not included in TOOL_LIST setting'

    @unittest.skipUnless('aerodynamics' in TOOL_LIST, FMT_SKIP_MSG.format('aerodynamics'))
    def test_aerodynamics_tool(self):
        tool = Aerodynamics()
        tool.run_tool(['Aerodynamics.py', '--test'])

    @unittest.skipUnless('dpdxcalc' in TOOL_LIST, FMT_SKIP_MSG.format('dpdxcalc'))
    def test_dpdxcalc_tool(self):
        tool = DpdxCalc()
        tool.run_tool(['DpdxCalc.py', '--test'])

    @unittest.skipUnless('performance' in TOOL_LIST, FMT_SKIP_MSG.format('performance'))
    def test_performance_tool(self):
        tool = Performance()
        tool.run_tool(['Performance.py', '--test'])

    @unittest.skipUnless('propulsion' in TOOL_LIST, FMT_SKIP_MSG.format('propulsion'))
    def test_propulsion_tool(self):
        tool = Propulsion()
        tool.run_tool(['Propulsion.py', '--test'])

    @unittest.skipUnless('structures' in TOOL_LIST, FMT_SKIP_MSG.format('structures'))
    def test_structures_tool(self):
        tool = Structures()
        tool.run_tool(['Structures.py', '--test'])

    @unittest.skipUnless('outputfunctions' in TOOL_LIST, FMT_SKIP_MSG.format('outputfunctions'))
    def test_outputfunctions_tool(self):
        tool1 = Constraints()
        tool1.run_tool(['Constraints.py', '--test'])
        tool2 = Objective()
        tool2.run_tool(['Objective.py', '--test'])

    # Tear-down class to clean up after tests are performed
    @classmethod
    def tearDownClass(cls):
        # Remove created directories
        super(TestSsbjToolExecution, cls).tearDownClass()
        files = [name for name in os.listdir('.') if name.endswith('.xml')]
        for file in files:
            os.remove(file)


if __name__ == '__main__':
    unittest.main()
