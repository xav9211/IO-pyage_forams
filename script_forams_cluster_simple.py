#!/usr/bin/env python\r\n
# coding=utf-8
import matplotlib as mpl

mpl.use('pdf')

import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime
from timeit import default_timer as timer

import os


filename = 'TEST_RESULTS_FORAMS'
time_dict = []
GRIDS = [10, 20, 50, 100, 500, 800, 1000, 1200, 1500, 1800, 2000]


def run(file_pointer):
    time = []

    for _ in range(10):
        start = timer()
        os.system('python -m pyage.core.bootstrap pyage_foram.solutions.statistics')
        finish = timer()
        time.append(finish - start)
        file_pointer.write(str(finish - start) + " [s]\n")
        file_pointer.flush()

    average = [np.mean(time), np.std(time)]
    file_pointer.write("Average time: " + str(average[0]) + " [s]\n")
    file_pointer.write("Standard deviation: " + str(average[1]) + " [s]\n\n")
    file_pointer.flush()

    return average


def plot_time(plotfilename):
    temp = np.array(time_dict)
    x = temp[:, 0]
    y = temp[:, 1]
    std = temp[:, 2]

    plt.bar(x, y, yerr=std, color='r')
    plt.ylabel("time[s]")
    plt.xlabel("grid size")
    plt.savefig(plotfilename)
    plt.close()


if __name__ == '__main__':
    os.environ['STEP'] = str(900)
    f = open(
        os.path.normpath(
            "../results/2D/time_results_simple/time_results_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"),
        'w')
    f.write("=================================================\n")
    f.write("AVERAGE TIME FOR EACH EXECUTION OF THE SIMULATION WITH DIFFERENT GRID SIZES\n")
    f.write("=================================================\n\n")
    for grid in GRIDS:
        if os.path.isfile(filename + '.log'):
            os.remove(filename + '.log')

        f.write("GRID SIZE: " + str(grid) + "\n\n")
        os.environ['GRID_SIZE'] = str(grid)
        os.environ['FORAMS_POPULATION'] = str(8)  # The number of forams is fixed

        time_tmp = run(f)
        time_dict.append([grid, time_tmp[0], time_tmp[1]])

    f.close()

    plot_time(os.path.normpath(
        "../results/2D/time_results_simple/" + 'execution_time_comparison_' + datetime.now().strftime(
            "%Y%m%d_%H%M%S") + '.pdf'))
