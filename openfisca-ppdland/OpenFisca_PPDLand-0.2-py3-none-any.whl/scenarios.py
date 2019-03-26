# -*- coding: utf-8 -*-

import logging

from openfisca_survey_manager.scenarios import AbstractSurveyScenario


from ppdland import CountryTaxBenefitSystem as PPDLandTaxBenefitSystem


log = logging.getLogger(__name__)


class PPDLandSurveyScenario(AbstractSurveyScenario):
    def __init__(self, data = None, tax_benefit_system = None,
            baseline_tax_benefit_system = None, year = None):
        super(PPDLandSurveyScenario, self).__init__()
        assert data is not None
        assert year is not None
        self.year = year
        if tax_benefit_system is None:
            tax_benefit_system = PPDLandTaxBenefitSystem()
        self.set_tax_benefit_systems(
            tax_benefit_system = tax_benefit_system,
            baseline_tax_benefit_system = baseline_tax_benefit_system
            )
        self.used_as_input_variables = list(
            set(tax_benefit_system.variables.keys()).intersection(
                set(data['input_data_frame'].columns)
                ))
        self.init_from_data(data = data)
        # self.new_simulation()
        # if baseline_tax_benefit_system is not None:
        #     self.new_simulation(use_baseline = True)


def init_single_entity(scenario, axes = None, parent1 = None, period = None):
    assert parent1 is not None

    individus = {}
    count_so_far = 0
    for nth in range(0, 1):
        group = [parent1]
        for index, individu in enumerate(group):
            if individu is None:
                continue
            id = individu.get('id')
            if id is None:
                individu = individu.copy()
                id = 'ind{}'.format(index + count_so_far)
            individus[id] = individu

        count_so_far += len(group)

    test_data = {
        'period': period,
        'individus': individus
        }
    if axes:
        test_data['axes'] = axes
    scenario.init_from_dict(test_data)
    return scenario


# -class Scenario(AbstractScenario):
# -    def init_single_entity(self, axes = None, parent1 = None, period = None):
# -        individus = []
# -        for index, individu in enumerate([parent1]):
# -            if individu is None:
# -                continue
# -            id = individu.get('id')
# -            if id is None:
# -                individu = individu.copy()
# -                individu['id'] = id = 'ind{}'.format(index)
# -            individus.append(individu)
# -        conv.check(self.make_json_or_python_to_attributes())(dict(
# -            axes = axes,
# -            period = period,
# -            test_case = dict(
# -                individus = individus,
# -                ),
# -            ))
# -        return self
