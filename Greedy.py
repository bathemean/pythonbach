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



    def get_csv_metrics(self, runtime):
        metrics = ",".join([self.spanner.get_cum_weight().__str__(),
                            self.spanner.get_density().__str__(),
                            self.spanner.get_highest_degree().__str__(),
                            runtime.__str__(),
                            self.find_stretch().__str__()])
        return metrics

    def get_spanner(self):
        return self.spanner

    def find_stretch(self):
        already_iterated = set()
        stretch = 0.0
        for source in self.org_graph.get_graph().iterkeys():
            for target in already_iterated:
                if target != source:
                    graph_dijk_distance, graph_dijk_preds = Dijkstra(self.org_graph, source)
                    spanner_dijk_distance, spanner_dijk_preds = Dijkstra(self.spanner, source)

                    found_stretch = spanner_dijk_distance[target] / graph_dijk_distance[target]

                    if found_stretch > stretch:
                        stretch = found_stretch

            already_iterated.add(source)
        return stretch

if __name__ == "__main__":
    pass
