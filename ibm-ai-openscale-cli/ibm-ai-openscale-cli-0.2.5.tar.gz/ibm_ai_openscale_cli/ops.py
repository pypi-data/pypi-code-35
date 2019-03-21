# coding=utf-8

import logging
from ibm_ai_openscale_cli.credentials import Credentials
from ibm_ai_openscale_cli.enums import MLEngineType
from ibm_ai_openscale_cli.ml_engines.azure_machine_learning import AzureMachineLearningEngine
from ibm_ai_openscale_cli.ml_engines.custom_machine_learning import CustomMachineLearningEngine
from ibm_ai_openscale_cli.ml_engines.sagemaker_machine_learning import SageMakerMachineLearningEngine
from ibm_ai_openscale_cli.ml_engines.spss_machine_learning import SPSSMachineLearningEngine
from ibm_ai_openscale_cli.ml_engines.watson_machine_learning import WatsonMachineLearningEngine
from ibm_ai_openscale_cli.models.model import Model
from ibm_ai_openscale_cli.models.german_credit_risk_model import GermanCreditRiskModel

logger = logging.getLogger(__name__)

class Ops:

    _wml_modelnames = ['DrugSelectionModel', 'GermanCreditRiskModel', 'GolfModel'] # suppress ScikitDigitsModel for now
    _azure_modelnames = ['GermanCreditRiskModel']
    _spss_modelnames = ['GermanCreditRiskModel']
    _custom_modelnames = ['GermanCreditRiskModel']
    _sagemaker_modelnames = ['GermanCreditRiskModel']

    def __init__(self, args):
        self._args = args
        self._credentials = Credentials(args)
        self._ml_engine = None

    def get_modeldata_instance(self, modelname, model_instance_num):
        model = None
        if modelname == 'GermanCreditRiskModel':
            model = GermanCreditRiskModel(self._args, model_instance_num)
        else:
            model = Model(modelname, self._args, model_instance_num)
        return model

    def get_ml_engine_instance(self):
        if not self._ml_engine:
            ml_engine_credentials = self._credentials.get_ml_engine_credentials()
            if self._args.ml_engine_type is MLEngineType.WML:
                self._ml_engine = WatsonMachineLearningEngine(ml_engine_credentials)
            elif self._args.ml_engine_type is MLEngineType.AZUREML:
                self._ml_engine = AzureMachineLearningEngine()
            elif self._args.ml_engine_type is MLEngineType.SPSS:
                self._ml_engine = SPSSMachineLearningEngine(ml_engine_credentials)
            elif self._args.ml_engine_type is MLEngineType.CUSTOM:
                self._ml_engine = CustomMachineLearningEngine(ml_engine_credentials)
            elif self._args.ml_engine_type is MLEngineType.SAGEMAKER:
                self._ml_engine = SageMakerMachineLearningEngine(ml_engine_credentials)
        return self._ml_engine
