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

"Test of the Graphite JSON response object."
import json
import wordgraph
from wordgraph import grapher


def test_server_requests_graph_structure():
    """Response data from live Graphite server filled with test data.

    Fictional data represents server requests for four fictional web servers.
    Each server's request load are approximately linear.

    http://play.grafana.org/graphite/render?from=-15min&until=now&target=aliasByNode(scaleToSeconds(apps.fakesite.*.counters.requests.count%2C1)%2C2)&format=json
    """
    with open('tests/data/server_requests.json') as data:
        graphite_data = json.load(data)
    with open('tests/data/server_requests.graph') as data:
        expected_data = json.load(data)
    graph = grapher.GraphiteGraph()
    graph.auto_ingest(graphite_data)
    structure = graph.as_dict()
    assert structure == expected_data
