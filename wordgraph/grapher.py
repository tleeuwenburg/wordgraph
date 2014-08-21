# Copyright 2014 Tennessee Leeuwenburg

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
This module contains the code for extracting the values needed for text generation
out of the supplied data package.

The Graph class defines the basic interface, which is simply to be able to get 
a dictionary of descriptor variables back. It is extended by AutoGraph which is also
abstract, and defines the interface for automated data ingestion.

AutoGraph is extended by GraphiteGraph, which does something. This Graph class makes
various non-general assupmtions about the incoming data, consistent with the data
being generated by the "graphite" web graphing application. 

Useful extensions to this module would include a broader selection of specific graph
types, supporting a wider array of input data use cases.

'''


import sys
from time import gmtime
from time import strftime

from . import analysers
from . import points

def generic():

    return AutoGraph()

class Graph():
    '''
    Base class for all other graph types, defining the data access method which will
    be used by the Realiser classes to fetch descriptor data.
    '''

    def as_dict(self):
        '''
        Return a dictionary of values for use by the realiser classes.
        '''
        raise NotImplementedError


class AutoGraph(Graph):
    '''
    Base class for automated data ingestion types. Defines the call to data ingestion.
    '''

    def auto_ingest(self, raw_data):
        '''
        Perform the processing on raw data and prepare the dictionary of values
        needed for the realisers
        '''

        raise NotImplementedError

class MPLGraph(AutoGraph):

    def auto_ingest(self, fig):

        # import ipdb; ipdb.set_trace()
        self.fig = fig
        self.axes = fig.gca()

        d = {}
        self.data_dict = d

        d['title'] = self.axes.title.get_text()
        

    def as_dict(self):
        return self.data_dict

class GraphiteGraph(AutoGraph):
    '''
    Expects data as produced by the "graphite" web application.
    '''

    """Graphite is timeseries, so we know that the x-axis will always be time."""

    def __init__(self):

        self.defaults = {
            'title': None,
            'x_axis': {
                'label': 'time',
                'min': sys.maxsize,
                'max': -1 * sys.maxsize
            },
            'y_axis': {
                'label': 'metric',
                'min': sys.maxsize,
                'max': -1 * sys.maxsize
            },
            "series": []

        }

    def auto_ingest(self, raw_data):
        '''
        Stores the raw data into self.raw_data
        Stores structured data into self.processed_data
        Creates the response for as_dist ad self.result
        '''

        self.raw_data = raw_data
        self.result_dict = self.defaults.copy()

        for series in self.raw_data['graphite_data']:
            self._create_series(series)

        # set values from raw data keys
        for key in ('title',):
            if key in raw_data:
                self.result_dict[key] = raw_data[key]
        # merge dicts from raw data keys
        for key in ('x_axis', 'y_axis'):
            if key in raw_data:
                self.result_dict[key].update(raw_data[key])

    def as_dict(self):

        readable_dict = self.result_dict.copy()
        if readable_dict.get('name', None) != analysers.UNPROCESSABLE:
            readable_dict['x_axis']['max'] = self._to_readable_date(readable_dict['x_axis']['max'])
            readable_dict['x_axis']['min'] = self._to_readable_date(readable_dict['x_axis']['min'])
            for item in readable_dict['series']:
                item['start_value']['x'] = self._to_readable_date(item['start_value']['x'])
                item['end_value']['x'] = self._to_readable_date(item['end_value']['x'])
        return readable_dict

    def _to_readable_date(self, datestring):
        readable_date = gmtime(int(datestring))
        return strftime("%d %b %Y %H:%M:%S", readable_date)

    def _create_series(self, series):
        '''
        Iterate over the data series contained in the raw data and add these 
        to the graph descriptor dictionary.
        '''

        values = self._convert_points(series['datapoints'])
        self._update_extremes(values)
        analysis = analysers.get_analysis(values)

        if analysis['name'] == analysers.UNPROCESSABLE:
            self.result_dict = analysis
        else:
            if len(values) == 1:
                distribution_name = 'single-point'
            else:
                distribution_name = analysis['name']

            series_dict = {
                "name": series['target'],
                "distribution": distribution_name,
                "min_y_value": analysis['min_y_value'],
                "fit": analysis['p_value'],
                "start_value": {"x": values[0].x, "y": values[0].y},
                "end_value": {"x": values[-1].x, "y": values[-1].y},
                "num_values": len(values)
            }

            self.result_dict['series'].append(series_dict)

    def _update_extremes(self, values):
        '''
        Used to maintain a reference to the bounds of the data contained
        in the graph, used for overall graph description.
        '''

        min_x = self.result_dict['x_axis']['min']
        max_x = self.result_dict['x_axis']['max']
        min_y = self.result_dict['y_axis']['min']
        max_y = self.result_dict['y_axis']['max']
        for x, y in values:
            min_x = min(x, min_x)
            min_y = min(y, min_y)
            max_x = max(x, max_x)
            max_y = max(y, max_y)
        self.result_dict['x_axis']['min'] = min_x
        self.result_dict['x_axis']['max'] = max_x
        self.result_dict['y_axis']['min'] = min_y
        self.result_dict['y_axis']['max'] = max_y

    def _convert_points(self, list_of_points):
        '''
        Pulls data values out of the raw data and produces objects suitable for later use.
        '''
        # NOTE: Graphite uses None for "no value", but want to plot at '0'
        the_points = [points.Point(x, y or 0) for [y, x] in list_of_points]
        return the_points
