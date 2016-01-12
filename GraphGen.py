from random import Random
import sys
from Dijkstra import Dijkstra
from Graph import Graph

class GraphGen(object):
    def __init__(self, vertices, density, is_weighted):
        if density <= 0.0:
            Exception("Density too low")
        elif vertices < 2:
            Exception("Too few vertices")
        elif density > 1.0:
            density = 1.0

        self.vertices = vertices
        self.density = density
        self.is_weighted = is_weighted
        self.graph = Graph()
        self.gen_graph()

    def gen_graph(self):
        rand = Random()
        margin = self.density * sys.maxint

        coherent = False
        while not coherent:
            self.graph = Graph()
            for v in xrange(0, self.vertices):
                v = "v" + v.__str__()
                self.graph.add_vertex(v)
                for u in self.graph.get_vertices():
                    if margin >= rand.randint(0, sys.maxint) and v != u:
                        self.graph.add_edge(v, u, rand.randint(1, 999))
            if len(Dijkstra(self.graph, "v0")[0]) == self.vertices:
                coherent = True


    def get_graph(self):
        return self.graph

    def __str__(self):
        return self.graph.__str__()

    def string_graph(self):
        string_graph = Graph()
        string_graph.add_vertex("v0")
        string_graph.add_vertex("v1")
        string_graph.add_vertex("v2")
        string_graph.add_vertex("v3")
        string_graph.add_edge("v0", "v1", 410)
        string_graph.add_edge("v0", "v2", 81)
        string_graph.add_edge("v0", "v3", 321)
        string_graph.add_edge("v1", "v2", 337)
        string_graph.add_edge("v1", "v3", 125)
        string_graph.add_edge("v2", "v3", 733)

        return string_graph

if __name__ == '__main__':
    gen = GraphGen(4, 0.8, True)
    gen.gen_graph()
#    print gen
