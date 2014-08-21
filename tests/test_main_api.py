import json
import wordgraph

from tests.lib.compare import assertParagraph

def test_main_api():
    """
    Based on one of the integration tests... push some data through the main API methods
    to verify the public interfaces are basically solid
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

    graph = {'graphite_data': graphite_data}

    expected = """
    This graph shows the relationship between time and metric
    The x axis, time, ranges from 28 Jul 2011 06:53:28 to 28 Jul 2011 06:53:32
    The y axis, metric, ranges from 1.0 to 6.0
    It contains 1 series
    The entries series is loosely linear
    """

    full_long = wordgraph.describe(graph, source='graphite')
    assertParagraph(full_long, expected)

    english = wordgraph.Describer(source='graphite')
    result = english.description(graph)
    assertParagraph(result, expected)