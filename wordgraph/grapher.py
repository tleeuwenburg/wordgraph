

def generic():

    return AutoGraph()

class Graph():

    pass


class AutoGraph(Graph):

    def auto_ingest(self, raw_data):

        self.raw_data = raw_data

        return