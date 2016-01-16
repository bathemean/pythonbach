import pprint, os.path
import numpy as np
import matplotlib.pyplot as plt
import math

pp = pprint.PrettyPrinter(depth=6)

ks = range(2, 10)
vertices = range(5, 9, 1)
densities = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

filepath = 'data/'
filetypes = ['tz', 'greedy']
filemetas = ['_density', '_vertices', '_k']

#measurements = ['density', 'weight', 'highest degree', 'runtime']

header = ['weight','density','degree','runtime','stretch']
measurements = ['weight','mdensity','degree','runtime','stretch']

measurements_string = 'weight,mdensity,degree,runtime,stretch'

def generate_filenames(meta):
    density = meta['density']
    vertices = meta['vertices']
    k = meta['k']

    #for t in filetypes:
    names = {}
    for t in filetypes:
        names[t] = filepath + t + '_density' + str(density) + '_vertices' + str(vertices) + '_k' + str(k) + '.csv'

    return names

def load_data_from_files(filenames):

    print filenames
    data = {}

    for t in filetypes:
        n = filenames[t]
        data[t] = load_data_from_file(n)
    return data


def load_data_from_file(filename):

    datafile = open(filename, 'r')

    if os.path.getsize(filename) == 0:
        raise Exception("File empty")

    headers = datafile.readline()
    # Remove trailing newline, and split string into a list over commas
    headers = headers[0:len(headers)-1].split(',')

    lines = datafile.readlines()
    # Remove trailing newline, and split string into a list over commas
    lines = [ line[0:len(line)-1].split(",") for line in lines]

    mean = average_string_readings(lines)

    data = {}

    for i in range(0, len(headers)):
        h = headers[i]
        if h == 'density':
            h = 'mdensity'
        data[h] = mean[i]
    return data


def average_string_readings(data):

    # Convert list entries to floats
    floatlines = []
    for line in data:
        if not line == header:
            floatlines.append( [float(l) for l in line] )

    mean = np.mean(floatlines, axis=0)

    return mean


dicts = []

'''
    dicts = [
        {'k': z,
            'weights': [{'G': x, 'TZ': y}],
            'degree': [{'G': x, 'TZ': y}]
        },
        {'vertices': z,
            'weights': [{'G': x, 'TZ': y}],
            'degree': [{'G': x, 'TZ': y}]
        }
    ]
'''

def initialize_results_dicts():
    for k in ks:
        new_dict = {}
        new_dict['k'] = k

        dicts.append(new_dict)

    for v in vertices:
        new_dict = {}
        new_dict['vertices'] = v

        dicts.append(new_dict)

    for d in densities:
        new_dict = {}
        new_dict['density'] = d

        dicts.append(new_dict)

    for d in dicts:
        for m in measurements:
            entry = {}
            for t in filetypes:
                entry[t] = np.NaN
            d[m] = entry



def select_dicts_by_meta(meta):

    density = meta['density']
    vertices = meta['vertices']
    k = meta['k']

    return_dicts = []

    for d in dicts:
        if 'k' in d and d['k'] == k:
            return_dicts.append(d)

        if 'vertices' in d and d['vertices'] == vertices:
            return_dicts.append(d)

        if 'density' in d and d['density'] == density:
            return_dicts.append(d)

    return return_dicts

def select_dicts_by_metaword(word):

    return_dicts = []

    for d in dicts:
        if word in d:
            return_dicts.append(d)

    return return_dicts

def insert_into_dicts(meta, data):
    idicts = select_dicts_by_meta(meta)

    for d in idicts:
        for m in measurements:
            for t in filetypes:
                d[m][t] = data[t][m]

def plot_points():
    params = ['k', 'vertices', 'density']

    for p in params:
        data = select_dicts_by_metaword(p)
        for m in measurements:
            greedy = []
            tz = []

            for d in data:
                greedy.append(d[m]['greedy'])
                tz.append(d[m]['tz'])

            plt.clf()

            plt.title(m + " som funktion af " + p)
            plt.xlabel(p)
            plt.ylabel(m)

            if p == 'k':
                x = ks
            elif p == 'vertices':
                x = vertices
            else:
                x = densities


            # Put the datapoints in the back
            plt.scatter(x, greedy, marker=".", c="#70CC80", label="Greedy datapoints")
            plt.scatter(x, tz, marker=".", c="lightsteelsky", label="TZ datapoints", )

            # Put in error bars for deviation
            plt.errorbar(x, greedy_mean, greedy_dev, linestyle='None', marker='^', c="#809984")
            plt.errorbar(x, tz_mean, tz_dev, linestyle='None', marker='^', c="lightbluesky")

            # Put means on top of datapoints
            plt.scatter(x, greedy_mean, marker="o", c="#809984", label="Greedy mean with deviation")
            plt.scatter(x, tz_mean, marker="o", c="lightbluesky", label="TZ mean with deviation")

            # Finally add the plots on the top layer
            plt.plot(x, greedy, label='Greedy', c="#809984")
            plt.plot(x, tz, label='TZ', c="lightbluesky")

            max_greedy = max(greedy)
            max_tz = max(tz)
            y_lim = max_greedy if max_tz < max_greedy else max_tz

            #plt.axes([0, int(math.ceil(max(y_lim))), 0, int(math.ceil(max(x)))])
            plt.legend()


            plt.savefig("plots/" + p + "_"+ m)

if __name__ == '__main__':

    initialize_results_dicts()

    '''
    for k in ks:
        for d in densities:
            for v in vertices:
                meta = {'density': d, 'vertices': v, 'k': k}

                filenames = generate_filenames(meta)
                try:
                    data = load_data_from_files(filenames)
                    insert_into_dicts(meta, data)
                except Exception as e:
                    break
    '''
    meta1 = {'density': 0.5, 'vertices': 25, 'k': 2}
    filenames = generate_filenames(meta1)
    data1 = load_data_from_files(filenames)
    insert_into_dicts(meta1, data1)

    meta1 = {'density': 0.6, 'vertices': 25, 'k': 2}
    filenames = generate_filenames(meta1)
    data1 = load_data_from_files(filenames)
    insert_into_dicts(meta1, data1)


    ds = select_dicts_by_metaword('density')

    plot_points()
    #pp.pprint(ds)
    #pp.pprint(len(ds))
