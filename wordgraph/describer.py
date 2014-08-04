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