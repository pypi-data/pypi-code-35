import base64
import csv
import io
import json
import os
import pandas
import pickle
import unittest
from sklearn.model_selection import train_test_split

from predictionmodel.model.defs.strings.config_keys import *
from predictionmodel.wrapper.PredictionModelWrapper import PredictionModelWrapper

config = {
    MODEL: {
        DATA_SERVICE_URL: 'https://reporting-production.swiss-iil.intel.com/reportingquerierformatter',
        GET_DATA_FROM_X_MINUTES_BACK: 1,
        POOL_MASTER: 'iil_vp_tiers',
        MIN_LONG_JOB_RUNTIME_IN_SECONDS: 1200,
        SHORT_JOB_CERTAINTY: 0.7,
        USED_FIELDS_AS_INPUT: 'user,qslot,cmdname,class,queue,task,classreservation',
        USED_FIELD_AS_OUTPUT: 'wtime'
    }
}


class TestPredictionModel(unittest.TestCase):

    def __exception_error_msg(self, e):
        return 'Exception caught. type: {}, message: {}'.format(type(e), str(e))

    def test_wrapper_build_model(self):
        try:
            # config['model']['save_intermediate_processed_data'] = 'True'
            wrapper = PredictionModelWrapper(config)
            model_data = wrapper.build()

            short_job1 = {
                "class": "SLES11&&8G",
                "qslot": "/DCG/Columbiaville/RTL/regression",
                "classreservation": None,
                "user": "orweiser1",
                "queue": "iil_normal",
                "cmdname": "trex",
                "task": "fxp.cse_level2.2019_03_27_12_32_59"
            }

            short_job2 = {
                "class": "SLES11_4G",
                "qslot": "/ipg_cnl/val/glc/debug/debug_regression/core_te",
                "classreservation": None,
                "user": "siris",
                "queue": "iil_normal",
                "cmdname": "trex",
                "task": "exe.level0.20190327_134540"
            }

            long_job3 = {
                "class": "SLES11",
                "qslot": "/perc_perc/asic/normal",
                "classreservation": "memory=8",
                "user": "grosenfe",
                "queue": "iil_normal",
                "cmdname": "ace",
                "task": "DOA_FW_TX"
            }

            pred1 = wrapper.get_prediction(input_features=short_job1)
            pred2 = wrapper.get_prediction(input_features=short_job2)
            pred3 = wrapper.get_prediction(input_features=long_job3)



            self.assertTrue('model' in model_data)
            self.assertTrue('identifier' in model_data)
            self.assertTrue('build_time' in model_data)
            self.assertTrue('stats' in model_data)
            self.assertTrue('build_duration' in model_data)
        except Exception as e:
            self.fail(self.__exception_error_msg(e))

    def test_wrapper_load_model(self):
        try:
            wrapper = PredictionModelWrapper(config)
            model_data = wrapper.build()

            wrapper.load(model_data['model'])

        except Exception as e:
            self.fail(self.__exception_error_msg(e))

    def test_model_pickling_size(self):
        try:
            wrapper = PredictionModelWrapper(config)
            model_data = wrapper.build()

            model = model_data['model']
            model_enc = base64.b64encode(model)
            model_data['model'] = model_enc.decode(
                'utf-8')  # Convert byte string to string (for json serialization to send over the network)

            model_data_str = str(model_data).encode('utf-8')
            model_data_size_kb = len(model_data_str) / 1024

            self.assertLessEqual(model_data_size_kb, 1024, msg='model pickle is larger than 1MB!')

        except Exception as e:
            self.fail(self.__exception_error_msg(e))

    def __load_dataset_from_file_system(self):
        csv_path = os.path.join(os.getcwd(), 'out/model_internals/jobs_data.csv')
        f_data = open(csv_path, 'r')
        csv_data = f_data.read()
        f_data.seek(0)
        csv_reader = csv.DictReader(f_data)
        column_names = csv_reader.fieldnames
        f_data.close()
        features = column_names[:-1]
        label = column_names[-1]

        jobs = pandas.read_csv(io.StringIO(csv_data))

        test_ratio = 0.3
        train_data, test_data = train_test_split(jobs, test_size=test_ratio, random_state=42)
        x_train = train_data[features]
        y_train = train_data[label]
        x_test = test_data[features]
        y_test = test_data[label]

        return x_train, y_train, x_test, y_test

    def __load_trained_classifier_from_file_system(self):
        model_path = os.path.join(os.getcwd(), 'out/model_internals/trained_model_data.json')
        f_model = open(model_path, 'r')
        model_data = json.loads(f_model.read())
        f_model.close()
        classifier_enc = model_data['model']
        classifier_dec = base64.b64decode(classifier_enc)
        classifier = pickle.loads(classifier_dec)

        return classifier


if __name__ == '__main__':
    unittest.main()
