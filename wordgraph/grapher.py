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

from . import analysers
from . import points

def generic():

    return AutoGraph()

class Graph():

    def as_dict(self):
        raise NotImplementedError


class AutoGraph(Graph):

    def auto_ingest(self, raw_data):

        self.raw_data = raw_data

        return

class GraphiteGraph(Graph):

    def __init__(self):

        self.defaults = {
            'title': None,
            'x_axis': {
                'label': 'time',
            },
            'y_axis': {
                'label': 'load',
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
        self._create_series()


    def as_dict(self):

        return self.result_dict.copy()

    def _create_series(self):

        series_data = self.raw_data['graphite_data']
        series = series_data[0]  # Pull out the first series only
        series_name = series["target"]
        values = self._convert_points(series['datapoints'])
        analysis = analysers.get_analysis(values)

        series_dict = {
            "name": series_name,
            "distribution": analysis['name'],
        }

        self.result_dict['series'].append(series_dict)
        
    def _convert_points(self, list_of_points):

        # NOTE: Graphite uses None for "no value", but want to plot at '0'
        the_points = [points.Point(x, y or 0) for [y, x] in list_of_points]
        return the_points





