import operator
from Graph import Graph
from GraphGen import GraphGen


class Greedy(object):
    def __init__(self, org_graph, r):
        """

        :param Graph graph: is the graph of which we want to find a spanner
        :param int r: is the dialation factor, it is the maximum stretch
        :return:
        """
        print "lol"

        self.org_graph = org_graph
        self.sorted_edges = self.to_sorted_edges()
        self.r_factor = r
        self.spanner = Graph()
        pass

    def make_spanner(self):
        edges = self.org_graph.get_graph()

        pass

    def to_sorted_edges(self,):
        """

        :param {} graph_dict:
        :return:
        """
        edges = {}
        for source_entry, entries in self.org_graph.get_graph().iteritems():
            print source_entry
            for target_entry, weight in entries.iteritems():
                # We don't want to add matching edge going in the other direction
                if not (edges.has_key((source_entry, target_entry)) or edges.has_key((target_entry, source_entry))):
                    edges[(source_entry, target_entry)] = weight
        sorted_edges = sorted(edges.items(), key=operator.itemgetter(1))
        print sorted_edges
        return sorted_edges


    def find_stretch(self):
        pass


if __name__ == "__main__":
    graph = GraphGen(4, 1, True).get_graph()
    greedy = Greedy(graph, 2*2-1)
