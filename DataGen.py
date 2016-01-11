from GraphGen import GraphGen
from Greedy import Greedy
from ThorupZwick import ThorupZwick


for v in xrange(25, 400, 25):
    for k in xrange(2, 10, 1):
        for d in xrange(7, 10, 1):
            dens_real = d * 0.1
            description_headers = "weight,density,highest degree,runtime,stretch\n"
            filename = "density" + dens_real.__str__() + "_vertices" + v.__str__() + "_k" + k.__str__() + ".csv"


            writerGreedy = open("datafiles/Greedy_" + filename, "a")
 #           writerTZ = open("datapoints/TZ_" + filename, "w", encoding="UTF-8")

            writerGreedy.write(description_headers)
#            writerTZ.write(description_headers)


            for i in xrange(0, 10, 1):
                generated_graph = GraphGen(v, dens_real, True).get_graph()

                greedy = Greedy(generated_graph, 2 * k - 1)
                #thorup_zwick = ThorupZwickSpanner(generated_graph)

                writerGreedy.write(greedy.get_csv_metrics() + "\n")
#                writerGreedy.write(thorup_zwick.get_csv_metrics())

            writerGreedy.close()
  #          writerTZ.close()

