from functools import partial
from multiprocessing import Pool, cpu_count

import numpy as np
from cognite_ml.timeseries.pattern_search import auxiliary as aux


class PatternSearchBase:
    def __init__(self, min_range, max_range, limit):
        self.limit = limit
        self.min_range = min_range
        self.max_range = max_range
        self.overlap_th = 0.1
        self.filterVariance = True

        self.input_ts = None
        self.query_seq = None
        self.granularity_second = None

    def search_init(self, input_timeseries, pattern_timeseries, timeout=None):
        self.timeout = timeout

        self.input_ts = input_timeseries
        self.query_seq = pattern_timeseries

        # make data evenly spaced
        self.input_ts = aux.make_index_even(self.input_ts)
        self.query_seq = aux.make_index_even(self.query_seq)

        # fill in missing values again in case there still are some NaNs
        aux.fill_nan(self.input_ts)
        aux.fill_nan(self.query_seq)

        timestamps = self.input_ts.timestamp.values
        self.granularity_second = int((timestamps[1] - timestamps[0]) / 1000)

    def find_similar_periods(self, expected_seq, timeseries):
        min_length = (
            aux.convert_time_delta_to_num_points(self.granularity_second, self.min_range)
            if self.min_range
            else len(expected_seq)
        )
        max_length = (
            aux.convert_time_delta_to_num_points(self.granularity_second, self.max_range)
            if self.max_range
            else len(expected_seq)
        )

        if max_length < min_length:
            raise ValueError("minRange is larger than maxRange.")

        lengths = sorted(set(map(int, np.linspace(min_length, max_length, 10, endpoint=True))))
        self.max_length = lengths[len(lengths) - 1]
        distances = []

        num_cpu = cpu_count()
        with Pool(processes=num_cpu) as p:
            results = p.map_async(
                partial(self.find_similar_patterns, expected_seq=expected_seq, timeseries=timeseries), lengths
            ).get(timeout=self.timeout)

        for res in results:
            distances += res
        return distances

    def combine_scores(self, score1, score2):
        """
        Combines the scores in score1 and score2 when length and index matches.
        """
        result = []
        j1 = 0
        j2 = 0

        while j1 < len(score1) and j2 < len(score2):
            len1 = score1[j1]["len"]
            len2 = score2[j2]["len"]
            i1 = score1[j1]["i"]
            i2 = score2[j2]["i"]
            stride1 = score1[j1]["stride"]
            stride2 = score2[j2]["stride"]

            if len1 == len2:
                if i1 == i2:
                    if stride1 != stride2:
                        raise ValueError("different strides")
                    result.append(
                        {
                            "distance": score1[j1]["distance"] + score2[j2]["distance"],
                            "stride": stride1,
                            "len": len1,
                            "i": i1,
                        }
                    )
                    j1 += 1
                    j2 += 1
                elif i1 < i2:
                    j1 += 1
                else:
                    j2 += 1

            elif len1 < len2:
                j1 += 1

            else:
                j2 += 1
        return result

    def find_similar_patterns(self, search_len, expected_seq, timeseries):
        raise NotImplementedError

    def search(self, dataframes):
        raise NotImplementedError
