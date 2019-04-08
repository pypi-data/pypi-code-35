#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `brewerwall` package."""


import unittest
from click.testing import CliRunner

from brewerwall import brewerwall
from brewerwall import cli


class TestBrewerwall(unittest.TestCase):
    """Tests for `brewerwall` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def testABV(self):
        """Test Alcohol by Volume calculation."""
        self.assertEqual(7.319479429051208, brewerwall.abv(1.055, 1))
        self.assertEqual(None, brewerwall.abv(1, 1.055))
    
    def testABW(self):
        """Test Alochol by Weight calculation."""
        self.assertEqual(5.782388748950455, brewerwall.abw(1.055, 1))
        self.assertEqual(None, brewerwall.abw(1, 1.055))
    
    def testMCU(self):
        """Test Malt Color Unit calculation."""
        self.assertEqual(None, brewerwall.mcu(1, 1, 0))
        self.assertEqual(5, brewerwall.mcu(5, 5, 5))
        self.assertEqual(5.5, brewerwall.mcu(5.5, 5.5, 5.5))
    
    def testSRM(self):
        """Test Standard Reference Method calculation."""
        self.assertEqual(None, brewerwall.srm(7, 5, 0))
        self.assertEqual(5.668651803424155, brewerwall.srm(7, 5, 5))
        self.assertEqual(5.943353419684101, brewerwall.srm(7.5, 5.5, 5.5))
    
    def testAAU(self):
        """Test Alpha Acid Unit calculation.

        Based off Palmer's Calculation
        """
        self.assertEqual(9.600000000000001, brewerwall.aau(1.5, 6.4))
        self.assertEqual(4.6, brewerwall.aau(1, 4.6))
    
    def testUtilization(self):
        """Test hop utilization calculation."""
        self.assertEqual(0.08363227080582435, brewerwall.utilization(10, 1.050))
        self.assertEqual(0.30113013986478654, brewerwall.utilization(120, 1.030))
        self.assertEqual(0.0, brewerwall.utilization(0, 1.070))
        self.assertEqual(0.14780486892282785, brewerwall.utilization(45, 1.090))
    
    def testIBU(self):
        """Test International Bittering Units calculation.
        
        Based off Palmer's Calculation
        """
        self.assertEqual(25.365869680614512, brewerwall.ibu(6.4, 1.5, 60, 1.080, 5))
        self.assertEqual(6.03108750923272, brewerwall.ibu(4.6, 1, 15, 1.080, 5))
    
    def testPlato(self):
        """Test conversion from specific gravity to plato."""
        self.assertEqual(17.055185000000108, brewerwall.convertToPlato(1.070))
    
    def testRealExtract(self):
        """Test Real Extract calculation."""
        self.assertEqual(6.216277095999994, brewerwall.realExtract(1.070, 1.015))
        self.assertEqual(None, brewerwall.realExtract(1.015, 1.070))
    
    def testCalories(self):
        """Test calories per 12 oz. serving calculation.
        
        Based on http://hbd.org/ensmingr/
        """
        self.assertEqual(234.97692128247783, brewerwall.calories(1.070, 1.015))
        self.assertEqual(None, brewerwall.calories(1.015, 1.070))
    
    def testAttenuation(self):
        """Test attenuation calculation."""
        self.assertEqual(0.7777777777777778, brewerwall.attenuation(1.054, 1.012))
        self.assertEqual(None, brewerwall.attenuation(1, 1.055))
    
    def testGravityCorrection(self):
        """Test gravity correction calculation."""
        self.assertEqual(1.0562227410996516, brewerwall.gravityCorrection(100.4, 1.050, 60))
    
    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'brewerwall.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
