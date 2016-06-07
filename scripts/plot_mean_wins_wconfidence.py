import matplotlib.pyplot as plt
import argparse
import os
import re
import csv
import numpy as np
import scipy as sp
import scipy.stats
import matplotlib.pyplot as plt

__author__ = 'Hector Azpurua'


def autolabel(ax, rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(
            rect.get_x()+rect.get_width()/2.,
            height + 2,
            '%d%%' % int(height),
            ha='center',
            va='bottom'
        )


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split('(\d+)', text)]


def get_ci(folder_path):

    if not os.path.exists(folder_path):
        raise Exception('Folder does not exist')

    if not os.path.isdir(folder_path):
        raise Exception('Path is not a folder')

    files = [x for x in os.listdir(folder_path) if os.path.isfile(folder_path+os.sep+x) and x.endswith('.csv')]
    files.sort(key=natural_keys)

    strategies_mean = {}

    for file in files:
        strategies = {}
        f = open(os.path.join(folder_path, file), 'rt')
        try:
            reader = list(csv.reader(f))
            keys = reader.pop(0)

            for i in xrange(len(reader)):
                key = keys[i]
                row = reader[i]
                for value in row:
                    if key not in strategies:
                        strategies[key] = []

                    value = float(value)
                    if value > 0:
                        strategies[key].append(value)
        finally:
            f.close()

        for k, v in strategies.items():
            if k not in strategies_mean:
                strategies_mean[k] = []
            strategies_mean[k].append(sum(v)/float(len(v)))

    strategies_ci = {}

    for key, value in strategies_mean.items():
        m, ml, mu = mean_confidence_interval(value)
        strategies_ci[key] = [m, ml, mu]

    return strategies_ci


def plot_ci(strategies_ci):
    n = []
    ci = []

    s_keys = strategies_ci.keys()

    for k in s_keys:
        v = strategies_ci[k]
        n.append(v[0])
        ci.append(v[2] - v[1])

    x = np.arange(len(n))
    fig, ax = plt.subplots()

    plt.grid(True)

    rects1 = plt.bar(x, n, color='#1D73AA', edgecolor='white', yerr=ci,
                     error_kw=dict(ecolor='crimson', lw=2, capsize=5, capthick=2))

    for bar in rects1:
        bar.set_hatch('//')

    plt.yticks(range(0, 101, 10))
    plt.xticks(x, n)
    ax.set_xticklabels(s_keys, rotation=35)
    plt.subplots_adjust(bottom=0.20)

    autolabel(ax, rects1)

    #plt.xlabel('Hexagon quantity')
    plt.ylabel('Mean win percent')
    #plt.title('Hexagons vs percentage of trajectory saved')


    x0, x1, y0, y1 = plt.axis()
    plt.axis((x0 - 0.2,
              x1 ,
              y0 ,
              y1 ))
    plt.show()
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Plots the mean wins of bots given a folder with the win table in CSV files'
    )

    parser.add_argument(
        '-i', '--input', help='Folder to search the CSV files', required=True
    )

    args = parser.parse_args()

    ci_dict = get_ci(args.input)
    plot_ci(ci_dict)


