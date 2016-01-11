import math, copy, sys, random
from Graph import Graph, find_stretch
from Dijkstra import Dijkstra
from GraphGen import GraphGen
import numpy as np
import pprint

pp = pprint.PrettyPrinter(depth=10)

class ThorupZwick(object):

    def __init__(self, G, k):
        self.G = G
        self.V = self.G.get_vertices()
        self.k = k

        self.spanner = Graph()
        for v in self.V:
            self.spanner.add_vertex(v)

        self.partition()
        #pp.pprint("Partitions: " + str(self.A))

        delta = {}
        delta[k] = self.find_dists(k)
        for i in list(reversed(range(0,k))):
            delta[i] = self.find_dists(i)
            self.grow_shortest_tree(i, delta)


    def nonrand_partition(self):
        V = self.G.get_vertices()

        self.A = {}
        self.A[0] = copy.deepcopy(V)
        self.A[1] = ['1','2','3','4']
        self.A[2] = ['1','2']
        self.A[3] = ['1']
        self.A[4] = ['1']
        self.A[5] = []

    def partition(self):
        # Partitions
        n = len(self.V)
        double_margin = math.pow( n/math.log(n), (-1.0)/self.k )
        margin = sys.maxint * double_margin


        self.A = {}
        self.A[0] = copy.deepcopy(self.V)
        self.A[self.k] = []

        for i in range(1, self.k):
            self.A[i] = []

            for v in self.A[i-1]:
                rand = random.randrange(sys.maxint)
                if rand < margin:
                    self.A[i].append(v)

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

        return None

    def find_dists(self, i):

        if i == self.k:
            delta = {}
            for v in self.V:
                delta[v] = np.inf

            return delta

        # Add source vertex
        self.G.add_vertex('s')
        for w in self.A[i]:
            self.G.add_edge('s', w, 0)

        # Elements not in A[i]
        subset = self.complement_lists(self.A[0], self.A[i])

        # Find witnesses
        delta, path = Dijkstra(self.G.get_graph(), 's')
        #witnesses = self.find_witnesses(i, subset, path)

        # Cleanup the graph
        self.G.remove_vertex('s')

        return delta

    def grow_shortest_tree(self, i, delta):
        subset = self.complement_lists(self.A[i], self.A[i+1])

        for w in subset:
            new_delta, path = Dijkstra(self.G.get_graph(), w, limit=delta[i+1])
            for p in path:
                source = p
                target = path[p]

                weight = self.G.get_edge_weight(source, target)
                self.spanner.add_edge(source, target, weight)

    def get_spanner(self):
        return self.spanner

if __name__ == '__main__':
    '''
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
    '''

    for i in range(0, 100):
        print i
        graph = GraphGen(100, 1, True).get_graph()

        dijk = Dijkstra(graph, "v0")
        tz = ThorupZwick(graph, 5)
        #print "Density", tz.spanner.get_density()
        stretch = find_stretch(graph, tz.get_spanner())
        print "Stretch", stretch
        if stretch > 5:
            print "=========="
            break
        #print "Weight", tz.spanner.get_cum_weight()
