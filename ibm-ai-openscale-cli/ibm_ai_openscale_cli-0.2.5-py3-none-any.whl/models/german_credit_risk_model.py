# coding=utf-8
import os
import logging
import random
import json
import copy
from ibm_ai_openscale_cli.enums import ResetType, MLEngineType
from ibm_ai_openscale_cli.utility_classes.utils import choices
from ibm_ai_openscale.supporting_classes import PayloadRecord
from ibm_ai_openscale_cli.models.model import Model

logger = logging.getLogger(__name__)

class GermanCreditRiskModel(Model):

    def __init__(self, args, model_instances=1, training_data_dict=None):
        super().__init__('GermanCreditRiskModel', args, model_instances, training_data_dict)
        self._fields = ["CheckingStatus","LoanDuration","CreditHistory","LoanPurpose","LoanAmount","ExistingSavings","EmploymentDuration","InstallmentPercent","Sex","OthersOnLoan","CurrentResidenceDuration","OwnsProperty","Age","InstallmentPlans","Housing","ExistingCreditsCount","Job","Dependents","Telephone","ForeignWorker"]
        self._field_choices = {
            'CheckingStatus': ['no_checking', '0_to_200', 'greater_200', 'less_0'],
            'LoanDuration': 0,
            'CreditHistory': ['no_credits', 'prior_payments_delayed', 'credits_paid_to_date', 'all_credits_paid_back', 'outstanding_credit'],
            'LoanPurpose': ['car_new', 'furniture', 'appliances', 'retraining', 'business', 'car_used', 'education', 'other', 'radio_tv', 'repairs', 'vacation'],
            'LoanAmount': 0,
            'ExistingSavings': ['unknown', 'less_100', '100_to_500', '500_to_1000', 'greater_1000'],
            'EmploymentDuration': ['less_1', '1_to_4', '4_to_7', 'greater_7', 'unemployed'],
            'InstallmentPercent': 0,
            'Sex': ['female', 'male'],
            'OthersOnLoan': ['none', 'co-applicant', 'guarantor'],
            'CurrentResidenceDuration': 0,
            'OwnsProperty': ['unknown', 'savings_insurance', 'real_estate', 'car_other'],
            'Age': 0,
            'InstallmentPlans': ['none', 'stores', 'bank'],
            'Housing': ['own', 'free', 'rent'],
            'ExistingCreditsCount': 0,
            'Job': ['skilled', 'management_self-employed', 'unskilled', 'unemployed'],
            'Dependents': 0,
            'Telephone': ['yes', 'none'],
            'ForeignWorker': ['yes', 'no']
        }

    def get_payload_history(self, num_day):
        """ Retrieves payload history from a json file"""
        if self._args.ml_engine_type is MLEngineType.WML or self._args.ml_engine_type is MLEngineType.AZUREML:
            return super().get_payload_history(num_day)
        elif self._args.ml_engine_type is MLEngineType.SAGEMAKER:
            return self._generate_payload_history_sagemaker(num_day)
        else: # Custom or SPSS
            return self._generate_payload_history(num_day)

    def _get_all_choices(self):
        all_choices = []
        for key, value in self._field_choices.items():
            if isinstance(value, list):
                for v in value:
                    all_choices.append('{}_{}'.format(key, v))
            else:
                all_choices.append(key)
        return all_choices

    def _generate_payload_history_sagemaker(self, num_day):
        fullRecordsList = []
        choices = self._get_all_choices()
        for day in range(num_day, num_day+1):
            hourly_records = random.randint(2,20)
            for hour in range(24):
                for i in range(hourly_records):
                    choices, choice_values =self.get_score_input_sagemaker()
                    req = {'fields': choices, 'values': choice_values }
                    resp = copy.deepcopy(req)
                    resp['fields'].append('predicted_label')
                    resp['fields'].append('score')
                    resp['values'].append(float(random.randint(0, 1)))
                    resp['values'].append(float(random.uniform(0.01, 0.09)))
                    score_time = str(self._get_score_time(day, hour))
                    fullRecordsList.append(PayloadRecord(request=req, response=resp, scoring_timestamp=score_time))
        return fullRecordsList

    def _generate_payload_history(self, num_day):
        """ Generates random payload history"""
        fullRecordsList = []
        for day in range(num_day, num_day+1):
            hourly_records = random.randint(2,20)
            for hour in range(24):
                for i in range(hourly_records):
                    fields, values = self.get_score_input()
                    req = {'fields': fields, 'values': values }
                    resp = copy.deepcopy(req)
                    if self._args.ml_engine_type is MLEngineType.SPSS:
                        resp['fields'].append('$N-Risk')
                        resp['fields'].append('$NC-Risk')
                        resp['values'][0].append(random.choice(['Risk', 'No Risk']))
                        resp['values'][0].append(random.uniform(0.1, 0.9))
                    elif self._args.ml_engine_type is MLEngineType.CUSTOM:
                        resp['fields'].append('prediction')
                        resp['fields'].append('probability')
                        resp['values'][0].append(random.choice(['Risk', 'No Risk']))
                        probability = random.uniform(0.1, 0.9)
                        resp['values'][0].append([probability, 1 - probability])
                    score_time = str(self._get_score_time(day, hour))
                    fullRecordsList.append(PayloadRecord(request=req, response=resp, scoring_timestamp=score_time))
        return fullRecordsList

    def get_score_input_sagemaker(self):
        """generates a single request payload"""
        choices = self._get_all_choices()
        choice_values = []
        fields = self._fields
        values = self._get_weighted_score_input_value()
        current_mapping = {}
        for i in range(len(fields)):
            field = fields[i]
            value = values[i]
            current_mapping[field] = value
        for choice in choices:
            choice_split = choice.split('_', 1)
            if len(choice_split) == 1:
                choice_values.append(float(current_mapping[choice]))
            else:
                if current_mapping[choice_split[0]] == choice_split[1]:
                    choice_values.append(1.0)
                else:
                    choice_values.append(0.0)
        choices.append('Risk_Risk')
        choices.append('Risk_No Risk')
        prediction = random.randint(0, 1)
        choice_values.append(float(prediction))
        choice_values.append(float(1 if prediction == 0 else 0))
        return (choices, choice_values)

    # generate a valid value based roughly on the training data distribution
    def _get_weighted_score_input_value(self):
        checkingstatus = choices(['no_checking', '0_to_200', 'greater_200', 'less_0'], weights=[20, 13, 3, 14])
        loanduration = choices([0, 1, 2, 3, 4], weights=[5, 18, 5, 18, 1])
        if loanduration == 0:
            loanduration = random.randint(4,6)
        elif loanduration == 1:
            loanduration = random.randint(7,23)
        elif loanduration == 2:
            loanduration = 24
        elif loanduration == 3:
            loanduration = random.randint(25,35)
        else:
            loanduration = random.randint(36,50)
        credithistory = choices(['no_credits', 'prior_payments_delayed', 'credits_paid_to_date', 'all_credits_paid_back', 'outstanding_credit'], weights=[1, 17, 15, 8, 10])
        loanpurpose = choices(['appliances', 'business', 'car_new', 'car_used', 'education', 'furniture', 'other', 'radio_tv', 'repairs', 'retraining', 'vacation'], weights=[6, 1, 9, 8, 2, 9, 1, 8, 3, 2, 2])
        loanamount = choices([0, 1, 2], weights=[10, 35, 5])
        if loanamount == 0:
            loanamount = 250
        elif loanamount == 1:
            loanamount = 10*random.randint(26, 700)
        else:
            loanamount = 10*random.randint(701, 1000)
        existingsavings = choices(['unknown', 'less_100', '100_to_500', '500_to_1000', 'greater_1000'], weights=[4, 19, 11, 11, 6])
        employmentduration = choices(['unemployed', 'less_1', '1_to_4', '4_to_7', 'greater_7'], weights=[3, 9, 15, 14, 9])
        installmentpercent = choices([1, 2, 3, 4, 5], weights=[5, 12, 16, 12, 4])
        sex = choices(['female', 'male'], weights=[17, 33])
        othersonloan = choices(['none', 'co-applicant', 'guarantor'], weights=[42, 7, 1])
        currentresidenceduration = choices([1, 2, 3, 4, 5], weights=[6, 12, 17, 11, 4])
        ownsproperty = choices(['unknown', 'savings_insurance', 'real_estate', 'car_other'], weights=[7, 17, 11, 15])
        age = choices([0, 1, 2, 3, 4], weights=[30, 6, 27, 6, 3])
        if age == 0:
            age = random.randint(19, 21)
        elif age == 1:
            age = random.randint(22, 27)
        elif age == 2:
            age = random.randint(28, 45)
        elif age == 3:
            age = random.randint(46, 52)
        else:
            age = random.randint(53, 74)
        installmentplans = choices(['none', 'stores', 'bank'], weights=[35, 10, 5])
        housing = choices(['own', 'free', 'rent'], weights=[32, 7, 11])
        existingcreditscount = choices([1, 2, 3], weights=[28, 20, 2])
        job = choices(['skilled', 'management_self-employed', 'unskilled', 'unemployed'], weights=[34, 6, 7, 3])
        dependents = choices([1, 2], weights=[42, 8])
        telephone = choices(['yes', 'none'], weights=[21, 29])
        foreignworker = random.choice(['yes', 'no'])
        return [checkingstatus, loanduration, credithistory, loanpurpose, loanamount, existingsavings, employmentduration, installmentpercent, sex, othersonloan, currentresidenceduration, ownsproperty, age, installmentplans, housing, existingcreditscount, job, dependents, telephone, foreignworker]

