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

    graph = grapher.generic()
    graph.auto_ingest(data)
    text = realiser.english(graph) # , title, x_name, y_name) TODO: how to handle meta

    return None