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

    def gen_graph(self):
        for v in xrange(0, self.vertices):
            v = "v" + v.__str__()
            self.graph.add_vertex(v)




if __name__ == '__main__':
    print GraphGen(4, 1.0, True).gen_graph()
