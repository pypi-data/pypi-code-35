#!/usr/bin/env python
from sakura.daemon.processing.operator import Operator
from sakura.daemon.processing.parameter import NumericColumnSelection
from sakura.daemon.processing.source import ComputedSource,ComputeMode

class GPSCoderStream(ComputedSource):
    def __init__(self, input_stream, lng_col, lat_col):
        self.input = input_stream
        self.lng_col = lng_col
        self.lat_col = lat_col
        self.gps_col_index = min(self.lng_col._index, self.lat_col._index)
        self.removed_col_index = max(self.lng_col._index, self.lat_col._index)
        ComputedSource.__init__(self, 'GeoJSON GPS', self.compute, ComputeMode.CHUNKS)
        self.add_columns()
    def filter_in(self, geo_region):
        # If someone issues self.filter(gps_col in geo_region):
        # 1- we filter the input stream given the bounding box of geo_region
        min_lng, min_lat, max_lng, max_lat = geo_region.bounds
        filtered_input = self.input
        filtered_input = filtered_input.filter(self.lng_col >= min_lng)
        filtered_input = filtered_input.filter(self.lng_col <= max_lng)
        filtered_input = filtered_input.filter(self.lat_col >= min_lat)
        filtered_input = filtered_input.filter(self.lat_col <= max_lat)
        # 2- we recursively create a GPSCoderStream over the filtered input
        coded_stream = GPSCoderStream(filtered_input, self.lng_col, self.lat_col)
        if isinstance(geo_region, GeoRectangle):
            # 3a- no more filtering is needed
            return coded_stream
        else:
            # 3b- we make the expensive computation on the coded stream
            return InFilterStream(coded_stream, self.gps_col_index, geo_region)
    def add_columns(self):
        # output columns are the same as input, except that
        # 1st of longitude or latitude column is replaced by gps
        # and the other one is removed.
        for i, col in enumerate(self.input.columns):
            if i == gps_col_index:
                self.add_column('GPS', object, ['gps'])
            elif i == removed_col_index:
                pass
            else:
                self.add_column(col._label, col._type, col._tags)
        # we define what happens if someone issues
        # self.filter(gps_col in geo_region)
        gps_column = self.columns[gps_col_index]
        gps_column.filter_functions['in'] = self.filter_in
    def compute(self):
        for in_chunk in column.chunks():
            out_chunk = np.empty(in_chunk.shape, self.get_dtype())
            ...
            GeoPoint(lng, lat).geojson
            ...
            yield out_chunk

class GPSCoder(Operator):
    NAME = "GPS Coder"
    SHORT_DESC = "Turn 2-columns latitude & longitude into 1-column GPS point data."
    TAGS = [ "gps" ]
    def construct(self):
        # inputs
        self.input = self.register_input('Mean input data')
        
        # parameters
        self.lng_column_param = self.register_parameter('longitude column',
                TagBasedColumnSelection(self.input, 'longitude'))
        self.lat_column_param = self.register_parameter('latitude column',
                TagBasedColumnSelection(self.input, 'latitude'))
        
        # outputs
        # dynamically constructed (see below)

    def get_outputs(self):
        if self.input.connected():
            lng_column = self.lng_column_param.value
            lat_column = self.lat_column_param.value
            return [ GPSCoderStream(self.input, lng_column, lat_column) ]
        else:
            return [ ]
