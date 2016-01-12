from __future__ import division
import math, copy, sys, random
from Dijkstra import Dijkstra
from Graph import Graph
from GraphGen import GraphGen
import numpy as np
import pprint

pp = pprint.PrettyPrinter(depth=10)


class ThorupZwick(object):
    def __init__(self, g, k):
        self.g = copy.deepcopy(g)
        self.v = copy.deepcopy(self.g.get_vertices())
        self.k = k

        self.spanner = Graph()
        for v in self.v:
            self.spanner.add_vertex(copy.deepcopy(v))

        self.partition()

        delta = {}
        delta[k] = self.find_dists(k)
        for t in list(reversed(range(0, k))):
            delta[t] = self.find_dists(t)
            self.grow_shortest_tree(t, delta)

    def partition(self):
        # Partitions
        n = len(self.v)
        double_margin = math.pow(n, (-1.0) / self.k)
        margin = sys.maxint * double_margin

        self.A = {}
        self.A[0] = copy.deepcopy(self.v)
        self.A[self.k] = []

        for j in range(1, self.k):
            self.A[j] = []

            for v in self.A[j - 1]:
                rand = random.randrange(sys.maxint)
                if rand < margin:
                    self.A[j].append(v)

    def complement_lists(self, l1, l2):
        ''' Elements of l1 not in l2 '''
        s2 = set(l2)
        l3 = [val for val in l1 if val not in s2]
        return l3

    def find_witnesses(self, i, vs, path):
        witnesses = {}
        for v in vs:
            w = self.find_witness(i, v, path)
            witnesses[v] = w

        return witnesses

    def find_witness(self, i, v, path):
        w = path[v]

        if w in self.A[i]:
            return w
        else:
            return self.find_witness(i, w, path)

    def find_dists(self, i_val):

        if i_val == self.k:
            delta = {}
            for v in self.v:
                delta[v] = np.inf

            return delta

        # Add source vertex
        self.g.add_vertex('s')
        for w in self.A[i_val]:
            self.g.add_edge('s', w, 0)

        # Elements not in A[i]
        subset = self.complement_lists(self.A[0], self.A[i_val])

        # Find witnesses
        delta, path = Dijkstra(self.g.get_graph(), 's')
        # witnesses = self.find_witnesses(i, subset, path)

        # Cleanup the graph
        self.g.remove_vertex('s')

        return delta

    def grow_shortest_tree(self, ai, delta):
        subset = self.complement_lists(self.A[ai], self.A[ai + 1])
        for w in subset:
            new_delta, path = Dijkstra(self.g.get_graph(), w, limit=delta[ai + 1])
            for p in path:
                source = p
                target = path[p]

                weight = self.g.get_edge_weight(source, target)
                self.spanner.add_edge(source, target, weight)

    def get_spanner(self):
        return self.spanner

    def find_stretch(self):
        already_iterated = set()
        stretch = 0.0
        for source in self.g.get_graph().iterkeys():
            for target in already_iterated:
                if target != source:
                    graph_dijk_distance, graph_dijk_preds = Dijkstra(self.g, source)
                    spanner_dijk_distance, spanner_dijk_preds = Dijkstra(self.spanner, source)

                    found_stretch = spanner_dijk_distance[target] / graph_dijk_distance[target]

                    if found_stretch > stretch:
                        stretch = found_stretch

            already_iterated.add(source)
        return stretch

    def get_csv_metrics(self, runtime):
        metrics = ",".join([self.spanner.get_cum_weight().__str__(),
                            self.spanner.get_density().__str__(),
                            self.spanner.get_highest_degree().__str__(),
                            runtime.__str__(),
                            self.find_stretch().__str__()])

        return metrics

    def nonrand_partition(self):
        V = self.g.get_vertices()

        self.A = {}
        self.A[0] = copy.deepcopy(V)
        self.A[1] = ['1', '2', '3', '4']
        self.A[2] = ['1', '2']
        self.A[3] = ['1']
        self.A[4] = ['1']
        self.A[5] = []


if __name__ == '__main__':

    G = Graph()
    G.add_vertex('1')
    G.add_vertex('2')
    G.add_vertex('3')
    G.add_vertex('4')
    G.add_edge('1', '2', 10)
    G.add_edge('1', '3', 20)
    G.add_edge('1', '4', 5)
    G.add_edge('2', '3', 30)
    G.add_edge('2', '4', 5)
    G.add_edge('3', '4', 5)
    TZ = ThorupZwick(G, 5)
    print TZ.get_csv_metrics(0)
    print Dijkstra(TZ.spanner, "1")
    print Dijkstra(G, "1")
"""
    for i in range(0, 100):
        print i
        graph = GraphGen(100, 1, True).get_graph()

        dijk = Dijkstra(graph, "v0")
        tz = ThorupZwick(graph, 5)
        # print "Density", tz.spanner.get_density()
        print "Stretch", stretch
        if stretch > 5:
            print "=========="
            break
            # print "Weight", tz.spanner.get_cum_weight()
"""