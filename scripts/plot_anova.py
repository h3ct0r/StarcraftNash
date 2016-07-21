import argparse
import os
import re
import csv
import operator
import numpy as np
import scipy as sp
import scipy.stats
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

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

def anova(data_dict):

    means_per_strat = {}
    join_vals = []
    join_group = []

    for key, v in data_dict.items():
        means_per_strat[key] = []
        for key2, v2 in v.items():
            mean = sum(v2)/float(len(v2))
            print key, key2, mean
            means_per_strat[key].append(mean)
            join_vals.append(mean)
            join_group.append(key)
            #means_per_strat[key] = sum(v2)/float(len(v2))

    sorted_ci = sorted(means_per_strat.items(), key=operator.itemgetter(1))
    s_keys, s_values = zip(*sorted_ci)

    print 's_keys:', s_keys
    print 's_values:', s_values    

    res = scipy.stats.f_oneway(*s_values)
    statistic = res[0]
    pvalue = res[1]

    print 'ANOVA Analysis: F value:', statistic, 'P value:', pvalue

    join_vals = np.asarray(join_vals)
    join_group = np.asarray(join_group)

    #print join_vals
    #print join_group

    for i in xrange(len(join_group)):
        v = join_group[i]
        if v == 'E-greedy':
            join_group[i] = r'$\alpha$-greedy'
        elif v == 'E-Nash':
            join_group[i] = r'$\epsilon$-Nash'
        elif v == 'Reply-score':
            join_group[i] = 'Replay last'
        elif v == 'Xelnaga':
            join_group[i] = 'Single choice'

    #mc = MultiComparison(np.asarray(s_values), np.asarray(s_keys))
    #result = mc.tukeyhsd()

    tukey = pairwise_tukeyhsd(endog=join_vals, groups=join_group, alpha=0.1)

    # #tukey.plot_simultaneous()    # Plot group confidence intervals
    # #plt.vlines(x=49.57,ymin=-0.5,ymax=4.5, color="red")

    print tukey.summary()              # See test summary

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
    strategies_per_strat = {}

    for file in files:
        strategies = {}
        f = open(os.path.join(folder_path, file), 'rt')
        try:
            reader = list(csv.reader(f))
            keys = reader.pop(0)

            for i in xrange(len(reader)):
                key = keys[i]
                row = reader[i]
                for j in xrange(len(row)):
                    value = row[j]
                    if key not in strategies:
                        strategies[key] = []

                    if key not in strategies_per_strat:
                        strategies_per_strat[key] = {}

                    value = float(value)
                    if value > 0:
                        strategies[key].append(value)
                        key2 = keys[j]
                        if key2 not in strategies_per_strat[key]:
                            strategies_per_strat[key][key2] = []
                        strategies_per_strat[key][key2].append(value)

        finally:
            f.close()

        for k, v in strategies.items():
            if k not in strategies_mean:
                strategies_mean[k] = []
            strategies_mean[k].append(sum(v)/float(len(v)))


    #print 'strategies_per_strat:', strategies_per_strat
    anova(strategies_per_strat)

    strategies_mean_per_strat = {}

    for key, v in strategies_per_strat.items():
        strategies_mean_per_strat[key] = {}
        for key2, v2 in v.items():
            strategies_mean_per_strat[key][key2] = sum(v2)/float(len(v2))

    #print 'strategies_mean_per_strat:', strategies_mean_per_strat

    strategies_ci = {}

    for key, value in strategies_mean.items():
        m, ml, mu = mean_confidence_interval(value)
        strategies_ci[key] = [m, ml, mu]

    return strategies_ci


def plot_ci(strategies_ci):

    n = []
    ci = []

    sorted_ci = sorted(strategies_ci.items(), key=operator.itemgetter(1))
    s_keys, s_values = zip(*sorted_ci)

    s_keys = list(s_keys)

    # Clean keys
    for i, v in enumerate(s_keys):
        if v == 'E-greedy':
            s_keys[i] = r'$\alpha$-greedy'
        elif v == 'E-Nash':
            s_keys[i] = r'$\epsilon$-Nash'
        elif v == 'Reply-score':
            s_keys[i] = 'Replay last'
        elif v == 'Xelnaga':
            s_keys[i] = 'Single choice'

    for v in s_values:
        n.append(v[0])
        ci.append(v[2] - v[1])

    x = np.arange(len(n))
    fig, ax = plt.subplots()

    rects1 = plt.bar(x, n, color='#1D73AA', edgecolor='white', yerr=ci,
                     error_kw=dict(ecolor='crimson', lw=2, capsize=5, capthick=2))

    for bar in rects1:
        bar.set_hatch('//')

    #plt.yticks(range(0, 101, 10))
    plt.xticks(x, n)
    ax.set_xticklabels(s_keys, rotation=35)
    plt.subplots_adjust(bottom=0.20)
    plt.grid(True)
    ax.set_axisbelow(True)

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


