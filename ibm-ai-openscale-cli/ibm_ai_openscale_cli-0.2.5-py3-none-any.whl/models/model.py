# coding=utf-8
import logging
import os
import datetime
import random
import math
import json
import pandas as pd
from ibm_ai_openscale.supporting_classes import BluemixCloudObjectStorageReference
from ibm_ai_openscale.supporting_classes import PayloadRecord
from ibm_ai_openscale_cli.utility_classes.utils import jsonFileToDict
from pathlib import Path

logger = logging.getLogger(__name__)

class Model():

    CONFIGURATION_FILENAME = 'configuration.json'
    MODEL_META_FILENAME = 'model_meta.json'
    MODEL_CONTENT_FILENAME = 'model_content.gzip'
    PIPELINE_META_FILENAME = 'pipeline_meta.json'
    PIPELINE_CONTENT_FILENAME = 'pipeline_content.gzip'
    TRAINING_DATA_STATISTICS_FILENAME = 'training_data_statistics.json'
    FAIRNESS_HISTORY_FILENAME = 'history_fairness.json'
    PAYLOAD_HISTORY_FILENAME = 'history_payloads.json'
    TRAINING_DATA_CSV_FILENAME = 'training_data.csv'
    FEEDBACK_CSV_FILENAME = 'feedback_data.csv'
    DEBIAS_HISTORY_FILENAME = 'history_debias.json'
    MANUAL_LABELING_HISTORY_FILENAME = 'history_manual_labeling.json'

    def __init__(self, name, args, model_instances=1, training_data_dict=None, training_data_type=None):
        self._args = args
        self.name = name
        if model_instances > 1:
            self.name += str(model_instances)

        if self._args.custom_model_directory:
            self._model_dir = self._args.custom_model_directory
        else:
            self._model_dir = os.path.join(os.path.dirname(__file__), name)
        env_name = '' if self._args.env_dict['name'] == 'YPPROD' else self._args.env_dict['name']

        # model create and deploy
        self.metadata = {}
        self.metadata['model_name'] = self.name + env_name
        self.metadata['model_metadata_file'] = self._get_file_path(Model.MODEL_META_FILENAME)
        self.metadata['model_file'] = self._get_file_path(Model.MODEL_CONTENT_FILENAME)
        self.metadata['pipeline_metadata_file'] = self._get_file_path(Model.PIPELINE_META_FILENAME)
        self.metadata['pipeline_file'] = self._get_file_path(Model.PIPELINE_CONTENT_FILENAME)
        self.metadata['deployment_name'] = self.name + env_name
        self.metadata['deployment_description'] = 'Created by Watson OpenScale Fast Path.'

        # configuration
        configuration_file = self._get_file_path(Model.CONFIGURATION_FILENAME)
        if configuration_file:
            self.configuration_data = jsonFileToDict(configuration_file)
        else:
            logger.error('ERROR: Unable to find configuration file: {}'.format(configuration_file))
            exit(1)

        # training data
        self.training_data_reference = None
        self.training_data = None
        self.training_data_statistics = None
        if not training_data_type:
            training_data_type = self._get_training_data_type()
        if training_data_dict:
            self._cos_credentials = training_data_dict['connection']
            self._training_data_filename = training_data_dict['source']['file_name']
            self._bucket_name = training_data_dict['source']['bucket']
            first_line_header = True if training_data_dict['source']['firstlineheader'] == 'true' else False
            self.training_data_reference = BluemixCloudObjectStorageReference( self._cos_credentials,
                                        '{}/{}'.format( self._bucket_name,
                                                        self._training_data_filename ),
                                        first_line_header=first_line_header )
        else:
            statistics_file = self._get_file_path(Model.TRAINING_DATA_STATISTICS_FILENAME)
            if statistics_file:
                self.training_data_statistics = jsonFileToDict(statistics_file)
            else:
                training_data_file = self._get_file_path(Model.TRAINING_DATA_CSV_FILENAME)
                if training_data_file:
                    self.training_data = pd.read_csv(training_data_file, dtype=training_data_type)
                else:
                    logger.error('ERROR: Unable to find training data')
                    exit(1)

        # refactor training data for use by online scoring
        self._set_training_data_columns(training_data_type)

        # feedback data - uses same dtype as training data
        feedback_file = self._get_file_path(Model.FEEDBACK_CSV_FILENAME)
        if feedback_file:
            self.feedback_data = pd.read_csv(feedback_file, dtype=training_data_type).to_dict('records') # make a list-style DICT
        else:
            logger.error('ERROR: Unable to find feedback file: {}'.format(feedback_file))
            exit(1)

    def _get_training_data_type(self):
        training_data_type = None
        if 'training_data_type' in self.configuration_data:
            training_data_type = {}
            for key in self.configuration_data['training_data_type'].keys():
                if self.configuration_data['training_data_type'][key] == 'int':
                    training_data_type[key] = int
                elif self.configuration_data['training_data_type'][key] == 'float':
                    training_data_type[key] = float
        return training_data_type

    # refactor training data csv (if available) for scoring
    # override this method in <model>.py as empty if training data csv should not be used for scoring
    def _set_training_data_columns(self, training_data_type):
        training_data_file = self._get_file_path(Model.TRAINING_DATA_CSV_FILENAME)
        if training_data_file:
            df = pd.read_csv(training_data_file, dtype=training_data_type)
            self.training_data_columns = {}
            for column_name in df.columns:
                column = []
                for values in df[column_name]:
                    column.append(values)
                self.training_data_columns[column_name] = column

    def _get_file_path(self, filename):
        """
        Returns the path for the file for the current serve engine, else the common file
        Eg. /path/to/sagemaker/training_data_statistics.json OR /path/to/training_data_statistics.json OR None
        """
        engine_specific_path = os.path.join(self._model_dir, self._args.ml_engine_type.name.lower(), filename)
        if Path(engine_specific_path).is_file():
            return engine_specific_path
        else:
            path = os.path.join(self._model_dir, filename)
            if Path(path).is_file():
                return path
        return None

    def _get_score_time(self, day, hour):
        return datetime.datetime.utcnow() + datetime.timedelta(hours=(-(24 * day + hour + 1)))

    # return an array of tuples with datestamp, response_time, and records
    def get_performance_history(self, num_day):
        fullRecordsList = []
        now = datetime.datetime.utcnow()
        for day in range(num_day, num_day+1):
            # model "typical" day (min at midnight, max at noon)
            # but with some days more busy overall than others, plus some random "noise"
            day_base = random.randint(1,4)
            for hour in range(24):
                score_time = (now + datetime.timedelta(hours=(-(24 * day + hour + 1)))).strftime('%Y-%m-%dT%H:%M:%SZ')
                score_count = day_base*60 + math.fabs(hour - 12)*30*random.randint(1,2) + 2*random.randint(-30, 90) + 1
                score_resp = random.uniform(60, 300)
                fullRecordsList.append({'timestamp': score_time, 'value': {'response_time': score_resp, 'records': score_count}})
        return fullRecordsList

    def get_fairness_history(self, num_day):
        """ Retrieves fairness history from a json file"""
        fullRecordsList = []
        history_file = self._get_file_path(Model.FAIRNESS_HISTORY_FILENAME)
        if history_file:
            with open(history_file) as f:
                fairness_values = json.load(f)
            for hour in range(24):
                score_time = self._get_score_time(num_day, hour).strftime('%Y-%m-%dT%H:%M:%SZ')
                index = (num_day * 24 + hour) % len(fairness_values) # wrap around and reuse values if needed
                fullRecordsList.append({'timestamp': score_time, 'value': fairness_values[index]})
        return fullRecordsList

    def get_debias_history(self, num_day):
        """ Retrieves debias history from a json file"""
        fullRecordsList = []
        history_file = self._get_file_path(Model.DEBIAS_HISTORY_FILENAME)
        if history_file:
            with open(history_file) as f:
                debias_values = json.load(f)
            for hour in range(24):
                score_time = self._get_score_time(num_day, hour).strftime('%Y-%m-%dT%H:%M:%SZ')
                index = (num_day * 24 + hour) % len(debias_values) # wrap around and reuse values if needed
                fullRecordsList.append({'timestamp': score_time, 'value': debias_values[index]})
        return fullRecordsList

    def get_quality_history(self, num_day, quality_min=0.75, quality_max=0.95):
        fullRecordsList = []
        for day in range(num_day, num_day+1):
            for hour in range(24):
                qualityTime = self._get_score_time(day, hour).strftime('%Y-%m-%dT%H:%M:%SZ')
                quality = random.uniform(quality_min, quality_max)
                fullRecordsList.append({
                    'timestamp': qualityTime,
                    'value': {
                        'quality': quality,
                        'threshold': 0.8,
                        'metrics': [{
                            'name': 'auroc',
                            'value': quality,
                            'threshold': 0.8
                        }]
                    }
                })
        return fullRecordsList

    def get_manual_labeling_history(self, num_day):
        """ Retrieves manual labeling history from a json file"""
        fullRecordsList = []
        history_file = self._get_file_path(Model.MANUAL_LABELING_HISTORY_FILENAME)
        if history_file:
            with open(history_file) as f:
                manual_labeling_records = json.load(f)
            for record in manual_labeling_records:
                # use fastpath_history_day value to check to see if this manual labeling history record is in the right range
                if record['fastpath_history_day'] == num_day:
                    # generate the scoring_timestamp value and then remove the fastpath_history_day/hour values
                    hour = record['fastpath_history_hour']
                    record['scoring_timestamp'] = self._get_score_time(num_day, hour).strftime('%Y-%m-%dT%H:%M:%SZ')
                    del record['fastpath_history_day']
                    del record['fastpath_history_hour']
                    fullRecordsList.append(record)
        return fullRecordsList

    def get_score_input(self, num_values=1):
        values = []
        for _ in range(num_values):
            value = []
            for field in self.configuration_data['asset_metadata']['feature_columns']:
                value.append(random.choice(self.training_data_columns[field]))
            values.append(value)
        return (self.configuration_data['asset_metadata']['feature_columns'], values)

    def get_payload_history(self, num_day):
        fullRecordsList = []
        # each 'payload_history_N.json' file contains a full day of payloads, to be divided across 24 hours
        history_file = self._get_file_path(Model.PAYLOAD_HISTORY_FILENAME.replace('.json', ('_' + str(num_day) + '.json')))
        if history_file:
            with open(history_file) as f:
                payloads = json.load(f)
                hourly_records = len(payloads) // 24
                index = 0
                for hour in range(24):
                    for i in range(hourly_records):
                        req = payloads[index]['request']
                        resp = payloads[index]['response']
                        score_time = str(self._get_score_time(num_day, hour))
                        fullRecordsList.append(PayloadRecord(request=req, response=resp, scoring_timestamp=score_time))
                        index += 1
        else:
            # the 'payload_history.json' file contains one hour of payloads, to be duplicated for every hour
            history_file = self._get_file_path(Model.PAYLOAD_HISTORY_FILENAME)
            if history_file:
                with open(history_file) as f:
                    payloads = json.load(f)
                for hour in range(24):
                    for payload in payloads:
                        req = payload['request']
                        resp = payload['response']
                        score_time = str(self._get_score_time(num_day, hour))
                        fullRecordsList.append(PayloadRecord(request=req, response=resp, scoring_timestamp=score_time))
        return fullRecordsList

    def get_score_input_sagemaker(self):
        logger.error('ERROR: Sagemaker scoring not supported for this model')
        exit(1)

