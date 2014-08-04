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
    assert False
