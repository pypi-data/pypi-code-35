# -*- coding: utf-8 -*-

import os
import sys


from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from ppdland.entities import entities


assert sys.version_info[0] == 3, "You should run this file with Python 3"

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


# Our country tax and benefit class inherits from the general TaxBenefitSystem class.
# The name CountryTaxBenefitSystem must not be changed, as all tools of the OpenFisca ecosystem expect a CountryTaxBenefitSystem class to be exposed in the __init__ module of a country package.
class CountryTaxBenefitSystem(TaxBenefitSystem):
    """PPDLand tax and benefit system"""
    CURRENCY = u""

    def __init__(self):
        # We initialize our tax and benefit system with the general constructor
        super(CountryTaxBenefitSystem, self).__init__(entities)

        # We add to our tax and benefit system all the variables
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))

        # self.Scenario = Scenario

        # We add to our tax and benefit system all the legislation parameters defined in the  parameters files
        self.load_parameters(os.path.join(COUNTRY_DIR, 'parameters'))
