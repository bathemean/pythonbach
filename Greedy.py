from __future__ import division
import operator
from Dijkstra import Dijkstra
from Graph import Graph
from GraphGen import GraphGen


class Greedy(object):
    def __init__(self, org_graph, r):
        """

        :param Graph graph: is the graph of which we want to find a spanner
        :param int r: is the dialation factor, it is the maximum stretch
        :return:
        """

        self.org_graph = org_graph
        self.sorted_edges = self.to_sorted_edges()
        self.r_factor = r
        self.spanner = Graph()
        self.make_spanner()
        pass

    def make_spanner(self):

        for edge, weight in self.sorted_edges:
            v, u = edge
            if not self.spanner.has_vertex(v):
                self.spanner.add_vertex(v)
            if not self.spanner.has_vertex(u):
                self.spanner.add_vertex(u)

            dijk = Dijkstra(self.spanner, v)
            if not u in dijk[0] or (self.r_factor * weight) < dijk[0][u]:
                self.spanner.add_edge(v, u, weight)
        pass

    def to_sorted_edges(self,):
        """
        Fetches graph and parses it into edges
        :param {} graph_dict:
        :return:
        """
        edges = {}
        for source_entry, entries in self.org_graph.get_graph().iteritems():
            for target_entry, weight in entries.iteritems():
                # We don't want to add matching edge going in the other direction
                if not (edges.has_key((source_entry, target_entry)) or edges.has_key((target_entry, source_entry))):
                    edges[(source_entry, target_entry)] = weight
        sorted_edges = sorted(edges.items(), key=operator.itemgetter(1))
        return sorted_edges

    def find_stretch(self):
        already_iterated = set()
        stretch = 0.0
        for source in self.org_graph.get_graph().iterkeys():
            for target in already_iterated:
                #print "This is the target", target
                #print already_iterated
                if target != source:
                    #print "yoloswarg"
                    graph_dijk_distance, graph_dijk_preds = Dijkstra(self.org_graph, source)
                    spanner_dijk_distance, spanner_dijk_preds = Dijkstra(self.spanner, source)

                    if spanner_dijk_distance[target] == 0:
                        print source, target
                    if graph_dijk_distance[target] == 0:
                        print self.org_graph.get_graph()[source][target]
                    #print graph_dijk_distance[target]
                    found_stretch = spanner_dijk_distance[target] / graph_dijk_distance[target]
                    #print "Found stretch", found_stretch
                    if found_stretch > stretch:
                        stretch = found_stretch

            already_iterated.add(source)
        return stretch

if __name__ == "__main__":
    graph = GraphGen(100, 1, True).get_graph()
#    print graph.get_density()
    dijk = Dijkstra(graph, "v0")
    greedy = Greedy(graph, 2*2-1)
    print "Spanner", greedy.spanner
    print "Density", greedy.spanner.get_density()
    print "Stretch", greedy.find_stretch()
    print "Weight", greedy.spanner.get_cum_weight()
