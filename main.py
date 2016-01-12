import os
from Dijkstra import Dijkstra
from GraphGen import GraphGen
from Greedy import Greedy
from ThorupZwick import ThorupZwick
import time

headers = 'weight,density,degree,runtime,stretch'
vertices = range(25, 1425, 25)
densities = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
ks = range(2,10)

def run_experiments():

    for v in vertices:
        for k in ks:
            for d in densities:
                print " == Running experiments for vertices: " + str(v) + ", k: " + str(k) + ", d: " + str(d) + ". =="
                graph = GraphGen(v, d, True).get_graph()

                write_to_log('tz', v, d, k, headers)

                itera = range(0, 10)
                for ite in itera:
                    try:
                        matrics, tz = run_tz(graph, k)
                    except KeyError:
                        itera.insert(0, ite)
                        print "Retrying TZ"
                        continue
                    write_to_log('tz', v, d, k, matrics)
                    print "TZ: " + matrics
                    # Greedy in bottom, so it's only run when TZ is run/not failing
                    if v < 450:
                        write_to_log('greedy', v, d, k, headers)
                        grd = run_greedy(graph, k)
                        write_to_log('greedy', v, d, k, grd)
                        print "Greedy: " + grd


def run_greedy(graph, k):
    start_time = time.clock()

    greedy = Greedy(graph, 2*k-1)

    end_time = time.clock()

    runtime = end_time - start_time

    metrics = greedy.get_csv_metrics(runtime)
    return metrics

def run_tz(graph, k):
    start_time = time.clock()

    tz = ThorupZwick(graph, k)

    end_time = time.clock()

    runtime = end_time - start_time

    metrics = tz.get_csv_metrics(runtime)
    return metrics, tz

def write_to_log(alg, vertices, density, k, metrics):

    filepath = 'data/'
    filename = alg + "_density" + str(density) + "_vertices" + str(vertices) + "_k" + str(k) + ".csv"

    with open(filepath + filename, 'a+') as writer:
        writer.write(metrics + '\n')

def write_to_status_log(log_string):
    pass


if __name__ == '__main__':
    run_experiments()

    #G = GraphGen(200, 1.0, True).get_graph()
    #grd = Greedy(G, 5)
    #print grd
