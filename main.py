from GraphGen import GraphGen
from Greedy import Greedy
from ThorupZwick import ThorupZwick
import time

headers = 'weight,density,degree,runtime,stretch'
vertices = range(25, 425, 25)
densities = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
ks = range(2,10)

def run_experiments():

    for v in vertices:
        for k in ks:
            for d in densities:
                print " == Running experiments for vertices: " + str(v) + ", k: " + str(k) + ", d: " + str(d) + ". =="
                graph = GraphGen(v, d, True).get_graph()

                write_to_log('greedy', v, d, k, headers)
                write_to_log('tz', v, d, k, headers)

                grd = run_greedy(graph, k)
                write_to_log('greedy', v, d, k, grd)
                print "Greedy: " + grd

                for i in range(0, 11):
                    tz = run_tz(graph, k)
                    write_to_log('tz', v, d, k, tz)
                    print "TZ: " + tz


def run_greedy(graph, k):
    start_time = time.clock()

    greedy = Greedy(graph, k)
    spanner = greedy.get_spanner()

    end_time = time.clock()

    runtime = end_time - start_time

    metrics = spanner.get_csv_metrics(runtime, graph)
    return metrics

def run_tz(graph, k):
    start_time = time.clock()

    tz = ThorupZwick(graph, k)
    spanner = tz.get_spanner()

    end_time = time.clock()

    runtime = end_time - start_time

    metrics = spanner.get_csv_metrics(runtime, graph)
    return metrics

def write_to_log(alg, vertices, density, k, metrics):

    filepath = 'data/'
    filename = alg + "_density" + str(density) + "_vertices" + str(vertices) + "_k" + str(k) + ".csv"

    with open(filepath + filename, 'a+') as writer:
        writer.write(metrics + '\n')


if __name__ == '__main__':
    run_experiments()
