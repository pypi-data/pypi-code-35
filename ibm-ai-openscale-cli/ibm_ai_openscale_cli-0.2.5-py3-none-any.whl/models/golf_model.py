# coding=utf-8
import os
import logging
import random
import json
from ibm_ai_openscale.supporting_classes import PayloadRecord
from ibm_ai_openscale_cli.models.model import Model

logger = logging.getLogger(__name__)

class GolfModel(Model):

    def __init__(self, args, model_instances=1, training_data_dict=None):
        self._training_data_type = { "crowd_score":float, "gesture_score":float, "face_score":float, "speaker_sound_score":float, "age":int, "country":int, "years_professional":int, "tourn_entered":int, "play_status":int, "hole":int, "ground":int, "stroke":int, "par_number":float, "hole_yardage":float, "hit_bunker":float, "hit_fairway":float, "green_in_regulation":float, "putts":float, "sand_save":float, "player_rank":float, "player_in_top10":float, "player_tied":float, "in_water":float, "ball_position":float, "shot_length":float, "penalty":int, "last_shot":int, "is_eagle_or_better":int, "is_birdie":int, "is_par":int, "is_bogey":int, "is_double_bogey_or_worse":int, "close_approach":int, "long_putt":int, "feels_like":float, "temperature":float, "heat_index":float, "barometric_pressure":float, "relative_humidity":float}
        super().__init__('GolfModel', args, model_instances, training_data_dict, self._training_data_type)

    def get_score_input(self, num_values=1):
        fields = ["crowd_score","gesture_score","face_score","speaker_sound_score","age","country","years_professional","tourn_entered","play_status","hole","ground","stroke","par_number","hole_yardage","hit_bunker","hit_fairway","green_in_regulation","putts","sand_save","player_rank","player_in_top10","player_tied","in_water","ball_position","shot_length","penalty","last_shot","is_eagle_or_better","is_birdie","is_par","is_bogey","is_double_bogey_or_worse","close_approach","long_putt","feels_like","temperature","heat_index","barometric_pressure","relative_humidity"]
        values = []
        for _ in range(num_values):
            value = []
            for field in fields:
                if self._training_data_type[field] == float:
                    value.append(random.uniform(0.1,0.9))
                elif self._training_data_type[field] == int:
                    value.append(float(random.randint(15, 65)))
            values.append(value)
        return (fields, values)

    def get_payload_history(self, num_day):
        historyfile = os.path.join(self._model_dir, 'history_payloads.json')
        fullRecordsList = []
        if historyfile != None:
            with open(historyfile) as f:
                payloads = json.load(f)
            for day in range(num_day, num_day+1):
                for hour in range(24):
                    for payload in payloads:
                        req = payload['request']
                        resp = payload['response']
                        score_time = str(self._get_score_time(day, hour))
                        fullRecordsList.append(PayloadRecord(request=req, response=resp, scoring_timestamp=score_time))
        return fullRecordsList

    def get_quality_history(self, num_day):
        return super().get_quality_history(num_day, 0.75, 0.95)
