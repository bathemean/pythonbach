from random import Random
import sys
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
        for v in xrange(0, self.vertices):
            v = "v" + v.__str__()
            self.graph.add_vertex(v)
            for u in self.graph.get_vertices():
                if margin >= rand.randint(0, sys.maxint) and v != u:
                    self.graph.add_edge(v, u, rand.randint(0, 999))

    def get_graph(self):
        return self.graph

    def __str__(self):
        return self.graph.__str__()


if __name__ == '__main__':
    gen = GraphGen(4, 0.8, True)
    gen.gen_graph()
    print gen
