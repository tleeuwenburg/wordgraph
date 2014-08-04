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

def test_graphite_documentation():
    """Verify description of Graphite JSON response from Graphite docs.

    The Graphite JSON response is for a single timeseries with five,
    monotonically increasing data points with the series name 'entries'.

    There is not graph title for the response.
    """
    graphite_data = json.loads("""
[{
  "target": "entries",
  "datapoints": [
    [1.0, 1311836008],
    [2.0, 1311836009],
    [3.0, 1311836010],
    [5.0, 1311836011],
    [6.0, 1311836012]
  ]
}]
    """)
    full_long_description = wordgraph.describe(graphite_data)
    assert full_long_description is not None

def test_server_requests():
    """Response data from Graphite server of fictional server requests.

    Fictional data represents server requests for four fictional web servers.
    Each server's request load are approximately linear.

    http://play.grafana.org/graphite/render?from=-15min&until=now&target=aliasByNode(scaleToSeconds(apps.fakesite.*.counters.requests.count%2C1)%2C2)&format=json
    """
    with open('tests/data/server_requests.json') as data:
        graph = {'graphite_data': json.load(data)}
        full_long_description = wordgraph.describe(graph)
        assert full_long_description is not None

def test_memory_usage():
    """Response data from Graphite server of fictional memory usage.

    Fictional data represents memory usage of a Graphite server.

    http://play.grafana.org/graphite/render?from=-15min&until=now&target=aliasByNode(integral(carbon.agents.ip-172-31-27-225-a.memUsage),3)&format=json
    """
    with file('tests/data/memory_usage.json') as data:
        graph = {'graphite_data': json.load(data)}
        full_long_description = wordgraph.describe(graph)
        assert full_long_description is not None
