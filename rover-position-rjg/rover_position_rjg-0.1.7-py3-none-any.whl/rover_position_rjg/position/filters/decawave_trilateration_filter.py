from typing import List

import numpy as np
from decawave_1001_rjg import DwmLocationResponse, DwmDistanceAndPosition, DwmPosition
from scipy import optimize

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.data_filter import DataFilter
from rover_position_rjg.position.calibration.decawave.decawave_range_scaler import DecawaveRangeScaler


class DecawaveTrilaterationFilter(DataFilter[DwmLocationResponse, DwmLocationResponse]):
    def __init__(self, range_scaler: DecawaveRangeScaler, name: str = ''):
        super().__init__(name)
        self.range_scaler = range_scaler
        self.tag_temperature = DecawaveRangeScaler.reference_temp
        self.anchor_temperatures = DecawaveRangeScaler.reference_temp

    def set_temperatures(self, tag_temperature: float, anchor_temperatures: float):
        self.tag_temperature = tag_temperature
        self.anchor_temperatures = anchor_temperatures

    def receive(self, data: Data[DwmLocationResponse]) -> None:
        message = data.value
        # Scale the measured distances using existing calibration
        new_anchors: List[DwmDistanceAndPosition] = []
        for dp in message.get_anchor_distances_and_positions():
            scaled = self.range_scaler.scale(dp.distance(), self.tag_temperature, self.anchor_temperatures, dp.address())
            new_dp = DwmDistanceAndPosition.from_properties(dp.address(), scaled, dp.quality_factor(), dp.position())
            new_anchors.append(new_dp)

        # Find the best fit solution for the tag position
        if len(new_anchors) < 3:
            new_tag_coordinate = message.get_tag_position().position()
        else:
            new_tag_coordinate = self.trilaterate(message.get_tag_position().position(), new_anchors)

        # Build the result and send it out
        new_tag_position = DwmPosition.from_properties(new_tag_coordinate, message.get_tag_position().quality_factor())
        response = DwmLocationResponse.from_properties(new_tag_position , new_anchors)
        self.send(Data(response, data.timestamp))

    @staticmethod
    def trilaterate(initial_guess: List[int], distances_and_positions: List[DwmDistanceAndPosition]) -> List[int]:
        anchors = []
        measurements = []
        for dp in distances_and_positions:
            anchor_position = dp.position().position()
            anchors.append(anchor_position)
            measurements.append(dp.distance())
        co_ords = optimize.least_squares(DecawaveTrilaterationFilter._least_squares_error, initial_guess, method='lm', xtol=1e-8, args=(anchors, measurements))
        return [int(round(co_ords.x[0])), int(round(co_ords.x[1])), int(round(co_ords.x[2]))]

    @staticmethod
    def _least_squares_error(guess, anchors: List[List[int]], measurements: List[float]) -> List[float]:
        x, y, z = guess
        results = []
        for i in range(0, len(anchors)):
            results.append(DecawaveTrilaterationFilter._measurement_error(x, y, z, anchors[i], measurements[i]))
        return results

    @staticmethod
    def _measurement_error(x: float, y: float, z: float, position: np.array, measurement: float):
        return ((x - position[0]) ** 2) + ((y - position[1]) ** 2) + ((z - position[2]) ** 2)*5 - (measurement ** 2)
