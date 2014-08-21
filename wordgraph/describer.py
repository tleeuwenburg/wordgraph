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

from . import grapher
from . import analysers
from . import realiser

GRAPH_TYPES = {
    'graphite': grapher.GraphiteGraph,
    'matplotlib': grapher.MPLGraph
}

class Describer():
    def __init__(self, source=None, language='English', demographic='summary'):
        '''
        utility class for holding nondefault variables
        >>> spanish_for_the_masses = Describer('graphite', 'es', 'summary')
        >>> spanish_for_the_masses.description(data)
        '''
        self.source = source
        self.language = language
        self.demographic = demographic

    def description(self, data, **kwargs):
        args = self.__dict__.copy()
        for key, value in kwargs.items():
            args[key] = value

        return describe(data, **args)

def describe(data, source=None, language='English', demographic='summary'):
    '''
    Describe the supplied graph object, together with a hint about the source of that object.

    @return: None if there was no description text generated for the graph
    @return: 

    Supported sources include:
      -- Raw data
      -- matplotlib (under dev)


    Unsupported sources include:
      -- graphite (under dev)
      -- dot, networkx?
      -- json, text?
    '''

    # If the source is a recognised type, then use a specialist graph type
    if source in GRAPH_TYPES:
        graph = GRAPH_TYPES[source]()

    else:
        graph = grapher.generic()

    graph.auto_ingest(data)
    text = realiser.english(graph.as_dict()) # , title, x_name, y_name) TODO: how to handle meta

    return text
