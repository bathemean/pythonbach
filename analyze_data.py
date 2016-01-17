import pprint, os.path
import numpy as np
import matplotlib.pyplot as plt
import math

pp = pprint.PrettyPrinter(depth=6)



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

    # Initialie data dict
    data = {}
    for i in range(0, len(headers)):
        h = headers[i]
        if h == 'density':
            h = 'mdensity'

        data[h] = []

    for l in lines:
        for i in range(0, len(headers)):
            h = headers[i]
            if h == 'density':
                h = 'mdensity'

            data[h].append(l[i])

    return data

datas = []
def insert_data():

    ks = range(2, 20)
    vertices = range(25, 125, 5)
    densities = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    # Insert data into our data dict
    for k in ks:
        for d in densities:
            for v in vertices:
                meta = {'density': d, 'vertices': v, 'k': k}

                filenames = generate_filenames(meta)
                try:
                    datadict = {}
                    datadict['k'] = k
                    datadict['density'] = d
                    datadict['vertices'] = v

                    data = load_data_from_files(filenames)

                    for m in measurements:
                        datadict[m] = {'greedy': data['greedy'][m], 'tz': data['tz'][m]}

                    datas.append(datadict)
                except Exception as e:
                    break


def average_string_readings(data):

    # Convert list entries to floats
    floatlines = []
    for line in data:
        if not line == header:
            floatlines.append( [float(l) for l in line] )

    mean = np.mean(floatlines, axis=1)
    std = np.std(floatlines, axis=1)

    return mean, std

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

def select_dicts_by_metaranges(meta, category=None):
    k = meta['k']
    densities = meta['densities']
    vertices = meta['vertices']

    return_dicts = []

    for d in datas:
        if d['k'] >= k[0] and d['k'] <= k[1]:
            if d['vertices'] >= vertices[0] and d['vertices'] <= vertices[1]:
                if d['density'] >= densities[0] and d['density'] <= densities[1]:

                    if category == None:
                        return_dicts.append(d)
                    else:
                        vals = {'k': d['k'], 'density': d['density'], 'vertices': d['vertices']}
                        vals[category] = d[category]
                        return_dicts.append(vals)

    return return_dicts

def get_data(meta, variable, category):

    ds = select_dicts_by_metaranges(meta, category=category)

    x = []
    xs = {'greedy': [], 'tz': []}
    y = {'greedy': [], 'tz': []}
    for i in range(0, len(ds)):
        x.append(ds[i][variable])

        for j in range(0, len(ds[i][category]['greedy'])):
            xs['greedy'].append(ds[i][variable])

        for j in range(0, len(ds[i][category]['tz'])):
            xs['tz'].append(ds[i][variable])

        y['greedy'].append(ds[i][category]['greedy'])
        y['tz'].append(ds[i][category]['tz'])

    return x, xs, y

def normalize_data(y):
    tmp = []
    new_y = {}
    for vals in y['greedy']:
        tmp.append( [float(v)*100 for v in vals] )
    new_y['greedy'] = tmp

    tmp = []
    for vals in y['tz']:
        tmp.append( [float(v)*100 for v in vals] )
    new_y['tz'] = tmp

    return new_y

def plot_points(x, xs, y, xlabel, ylabel, filename, title=None):
    params = ['k', 'vertices', 'density']

    if float(y['greedy'][0][0]) < 0.1:
        y = normalize_data(y)

    plt.clf()

    if title == None:
        plt.title(ylabel + " som funktion af " + xlabel)
    else:
        plt.title(title)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    means = {}
    stds = {}
    for t in filetypes:
        means[t], stds[t] = average_string_readings(y[t])

    #print "means: " + str(means)
    #print "stddev: ", str(stds)

    greedy_point = '#585CFF'
    greedy_line = '#00049C'
    greedy_error = '#FF003D'

    tz_point = '#3DFF66'
    tz_line = '#00B226'
    tz_error = '#003D0D'

    # Put in error bars for deviation
    plt.errorbar(x, means['greedy'], stds['greedy'], linestyle='None', linewidth=2, marker='^', c=greedy_error)
    plt.errorbar(x, means['tz'], stds['tz'], linestyle='None', linewidth=2, marker='^', c=tz_error)

    # Put the datapoints in the back
    plt.scatter(xs['greedy'], y['greedy'], marker=".", s=50, c=greedy_point, edgecolor='none', label="Greedy datapoints")
    plt.scatter(xs['tz'], y['tz'], marker=".", s=50, c=tz_point, edgecolor='none', label="TZ datapoints" )

    # Put means on top of datapoints
    #plt.scatter(x, means['greedy'], marker="o", s=50, c=greedy_point, label="Greedy mean with deviation")
    #plt.scatter(x, means['tz'], marker="o", s=50, c=tz_point, label="TZ mean with deviation")

    # Finally add the plots on the top layer
    plt.plot(x, means['greedy'], label='Greedy mean', c=greedy_line, linewidth=2)
    plt.plot(x, means['tz'], label='TZ mean', c=tz_line, linewidth=2)


    xvals = [float(v) for v in x]
    x_min = min(x)
    x_max = max(xvals)

    yvals = []
    for t in filetypes:
        for vals in y[t]:
            for v in vals:
                yvals.append(float(v))

    y_min = min(yvals)
    y_max = max(yvals)


    plt.xlim([x_min-0.1, x_max+0.1])
    plt.ylim([y_min, y_max])

    plt.text(x_min-0.5, y_min-0.7, 'n=' + str(len(y['greedy'][0])))


    plt.legend(fontsize="xx-small", loc="upper left")

    #plt.show()
    if xlabel == 'density':
        xlabel = 'densities'

    if meta[xlabel][0] != meta[xlabel][1]:
        plt.savefig('plots/' + filename)
    #plt.savefig("plots/" + ylabel + "_"+ xlabel)

if __name__ == '__main__':

    # Select data source
    filepath = 'data200/'
    # Select data ranges (to be plotted)


    ## NO MORE SETUP
    insert_data()

    vs = range(25,45,5)

    params = ['k', 'vertices', 'density']
    for p in params:
        for m in measurements:
            for v in vs:
                for k in [2,3,4]:
                    meta = {'vertices': [v,v], 'k': [k,k], 'densities': [0.5, 1.0]}
                    filename = m + '_' + p + '_k_' + str(k) + '_v_' + str(v)
                    x, xs, y = get_data(meta, p, m)
                    plot_points(x, xs, y, p, m, filename)

    print "DING! Fries are done."
