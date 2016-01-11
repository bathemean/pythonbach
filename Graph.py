import numpy as np
import pprint

class Graph(object):

    def __init__(self):
        self._G = {}
        self._V = []

    def __str__(self):
        res = ""

        for v in self.get_vertices():
            adj = self._G[v]
            for w in adj:
                new_res = "(" + str(v) + "->" + str(w) + "=" + str(self.get_edge_weight(v,w)) + ")"
                res = res + ", " + new_res
        return res

    def add_vertex(self, vertex):
        self._G[vertex] = {}
        self._V.append(vertex)

    def add_edge(self, source, target, weight):
        self._G[source][target] = weight
        self._G[target][source] = weight

    def get_vertices(self):
        return self._V

    def get_edge_weight(self, source, target):
        w = self._G[source][target]
        return w

    def get_stretch(self):
        pass

    def get_density(self):
        pass

    def get_highest_degree(self):
        pass

    def get_cum_weight(self):
        pass


if __name__ == '__main__':

    G = Graph()

    G.add_vertex(1)
    G.add_vertex(2)

    G.add_edge(1,2,100)

    print(G)
