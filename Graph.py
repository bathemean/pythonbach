import numpy as np
import pprint

pp = pprint.PrettyPrinter(depth=6)

class Graph(object):

    def __init__(self):
        self._G = {}
        self._V = []

    #def __iter__(self): return self._G.itervalues()

    def __str__(self):
        res = ""

        for v in self.get_vertices():
            adj = self._G[v]
            for w in adj:
                new_res = "(" + str(v) + "->" + str(w) + "=" + str(self.get_edge_weight(v,w)) + ")"
                if len(res) == 0:
                    res = new_res
                else:
                    res = res + ", " + new_res
        return res

    def add_vertex(self, vertex):
        self._G[vertex] = {}
        self._V.append(vertex)

    def add_edge(self, source, target, weight):
        self._G[source][target] = weight
        self._G[target][source] = weight

    def get_graph(self):
        return self._G
        
    def get_vertices(self):
        return self._V

    def get_edge_weight(self, source, target):
        w = self._G[source][target]
        return w

<<<<<<< HEAD
    def get_stretch(self):
        pass

    def get_density(self):
        pass

    def get_highest_degree(self):
        pass

    def get_cum_weight(self):
        pass

=======
    def test(self):
        return self._G
>>>>>>> f6324dd0bf3d272ac7cd8dd935e0d39bd62854d4

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


    print G.test()['1']
    A = {'s': {'u':10, 'x':5},
    	'u': {'v':1, 'x':2},
    	'v': {'y':4},
    	'x':{'u':3,'v':9,'y':2},
    	'y':{'s':7,'v':6}}
    #pp.pprint(A)
    #print(G)
