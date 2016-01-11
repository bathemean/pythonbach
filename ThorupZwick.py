import math, copy, sys, random
from Graph import Graph
from Dijkstra import Dijkstra

class ThorupZwick(object):

    def __init__(self, G, k):
        self._G = G
        self._k = k

        self.partition()
        print "Partitions: " + str(self._A)
        self.find_witness(2, 1)


    def partition(self):
        V = G.get_vertices()
        # Partitions
        n = len(V)
        double_margin = math.pow( n/math.log(n), (-1.0)/self._k )
        margin = sys.maxint * double_margin


        self._A = {}
        self._A[0] = copy.deepcopy(V)
        self._A[self._k] = []

        for i in range(1, self._k-1):
            self._A[i] = []

            for v in self._A[i-1]:
                rand = random.randrange(sys.maxint)
                if rand < margin:
                    self._A[i].append(v)

    def intersect_dicts(d1, d2):
        d = {x:d1[x] for x in d1 if x in d2}
    def find_witness(self, i, v):
        # Add source vertex
        self._G.add_vertex('0')
        for w in self._A[i]:
            self._G.add_edge('0', w, 0)

        delta, path = Dijkstra(self._G.get_graph(), '0')
        print "Deltas: " + str(delta)

        subset = {}

    def find_dists(i):
        pass

if __name__ == '__main__':
    G = Graph()

    G.add_vertex('1')
    G.add_vertex('2')
    G.add_vertex('3')
    G.add_vertex('4')

    G.add_edge('1','2',10)
    G.add_edge('1','3',15)
    G.add_edge('1','4',45)
    G.add_edge('2','3',30)
    G.add_edge('2','4',50)
    G.add_edge('3','4',20)

    TZ = ThorupZwick(G, 5)
