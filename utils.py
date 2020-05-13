#!/usr/bin/env python3

import csv
import math
import numpy as np
import os

from matplotlib import pyplot as plt, rc
from sklearn.metrics import roc_auc_score, roc_curve
from typing import List

CSV_FILE = "data/grading.csv"

TC_GUI_OUTPUT_FILE = "tc_output_final2.txt"

HIST_LOC = "figures/histograms_a2"

GRADE_DATA_LABELS = [
    "Human Classes", "Human Attributes", "Human Assocs",
    "Heuristic Classes", "Heuristic Attributes", "Heuristic Assocs",
    "TouchCore Classes", "TouchCore Attributes", "TouchCore Assocs",
]

# Expected, predicted
heur = np.transpose([
    [0, 1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	0],
    [0,	0],
    [1,	1],
    [1,	0],
    [1,	1],
    [0,	0],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	0],
    [1,	1],
    [1,	1],
    [1,	0],
    [1,	1],
    [0,	0],
    [1,	0],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	0],
    [1,	1],
    [1,	0],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	0],
    [1,	1],
    [1,	1],
    [0,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [0,	0],
])

tc = np.transpose([
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	0],
    [0,	0],
    [1,	1],
    [1,	0],
    [1,	1],
    [1,	0],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [0,	0],
    [1,	1],
    [1,	1],
    [1,	0],
    [1,	1],
    [1,	0],
    [0,	0],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	0],
    [1,	1],
    [1,	0],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	0],
    [1,	1],
    [1,	1],
    [1,	1],
    [0,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	1],
    [1,	0],
])

heur_final = np.transpose([
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 0],
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 0],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 0],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 0],
    [0, 0],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 0],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 1],
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 1],
    [0, 1],
    [1, 1],
    [1, 1],
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 0],
    [1, 1],
])

tc_final = np.transpose([
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 0],
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 0],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 0],
    [1, 1],
    [1, 1],
    [1, 0],
    [1, 1],
    [1, 1],
    [0, 0],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 0],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 1],
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 1],
    [0, 0],
    [1, 1],
    [1, 1],
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 0],
    [1, 1],
])

c = [
    0,
    3,
    -2,
    1,
    -2,
    -1,
    1,
    1,
    1,
    -4,
    0,
    0,
    0,
    0,
    -1,
    1,
    -1,
    -2,
    2,
    0,
    1,
    -2,
    -2,
    -1,
    0,
    1,
    1,
    4,
    -1,
    2,
    -1,
    1,
    0,
    1,
    2,
    1,
    1,
    -1,
    -1,
    0,
    0,
    -1,
    -1,
    0,
    0,
    1,
    0,
    -2,
    -1,
    1,
    1,
    2,
    -2,
    1,
    3,
    0,
    1,
    -2,
    2,
    2,
    0,
    2,
    1,
    0,
    1,
    1,
    2,
    1,
    3,
    0,
    3,
    3,
    1,
    0,
    1,
    0,
    0,
    -1,
    0,
    0,
    -1,
    0,
    6,
    -1,
    2,
    1,
    -1,
    3,
    1,
    -2,
    0,
    0,
    0,
    0,
    0,
    -3,
    -2,
    3,
    1,
    -1,
    -1,
    1,
    -1,
    0,
    0,
    2,
    -2,
    1,
    1,
    0,
    1,
    1,
    -1,
]

at = [
    -1,
    -1,
    0,
    1,
    2,
    1,
    -2,
    -2,
    2,
    1,
    2,
    -2,
    -1,
    -2,
    -3,
    -2,
    -1,
    -1,
    3,
    -1,
    -1,
    0,
    3,
    0,
    0,
    4,
    0,
    2,
    0,
    3,
    3,
    2,
    2,
    0,
    -2,
    0,
    -2,
    2,
    -1,
    -3,
    3,
    1,
    -2,
    0,
    1,
    -2,
    -2,
    3,
    -1,
    4,
    -1,
    -2,
    -2,
    -1,
    0,
    -1,
    0,
    0,
    -5,
    -3,
    1,
    2,
    -2,
    2,
    2,
    0,
    1,
    1,
    -2,
    2,
    0,
    0,
    -2,
    -1,
    -1,
    1,
    1,
    2,
    -4,
    -2,
    -1,
    1,
    1,
    0,
    -1,
    -1,
    -1,
    -2,
    1,
    1,
    2,
    -2,
    -2,
    2,
    -1,
    -2,
    1,
    -2,
    -1,
    0,
    -2,
    1,
    -2,
    -1,
    -2,
    -3,
    4,
    -2,
    -1,
    -4,
    1,
    4,
    1,
]

d_asc = [
    -2,
    0,
    3,
    4,
    0,
    -5,
    1,
    -2,
    2,
    2,
    4,
    3,
    6,
    6,
    0,
    1,
    6,
    6,
    7,
    5,
    5,
    -1,
    2,
    1,
    0,
    5,
    9,
    0,
    6,
    4,
    0,
    8,
    10,
    2,
    3,
    2,
    3,
    4,
    -3,
    -2,
    1,
    1,
    -2,
    3,
    9,
    5,
    2,
    3,
    0,
    2,
    -2,
    0,
    -2,
    0,
    4,
    10,
    -2,
    -1,
    2,
    5,
    6,
    4,
    -2,
    4,
    0,
    -4,
    6,
    7,
    -3,
    -1,
    -4,
    3,
    4,
    0,
    3,
    2,
    0,
    2,
    5,
    1,
    -1,
    1,
    5,
    -3,
    8,
    6,
    5,
    8,
    -2,
    6,
    1,
    7,
    -1,
    -3,
    6,
    0,
    8,
    2,
    2,
    4,
    -2,
    -1,
    3,
    3,
    4,
    3,
    7,
    7,
    1,
    0,
    6,
    5,
    9,
]

real_asc = [
    0.88,
    0.79,
    0.64,
    0.55,
    0.76,
    0.76,
    0.62,
    0.69,
    0.62,
    0.67,
    0.52,
    0.67,
    0.52,
    0.45,
    0.52,
    0.67,
    0.74,
    0.71,
    0.52,
    0.50,
    0.71,
    0.67,
    0.69,
    0.71,
    0.64,
    0.81,
    0.64,
    0.55,
    0.55,
    0.71,
    0.76,
    0.43,
    0.57,
    0.64,
    0.50,
    0.38,
    0.55,
    0.83,
    0.74,
    0.48,
    0.57,
    0.69,
    0.76,
    0.88,
    0.55,
    0.00,
    0.67,
    0.43,
    0.50,
    0.76,
    0.62,
    0.74,
    0.43,
    0.64,
    0.4,
    0.5,
    0.71,
    0.71,
    0.71,
    0.55,
    0.62,
    0.69,
    0.71,
    0.71,
    0.43,
    0.62,
    0.57,
    0.45,
    0.74,
    0.74,
    0.29,
    0.38,
    0.43,
    0.38,
    0.52,
    0.52,
    0.76,
    0.81,
    0.52,
    0.52,
    0.57,
    0.48,
    0.31,
    0.4,
    0.67,
    0.43,
    0.71,
    0.67,
    0.76,
    0.62,
    0.6,
    0.5,
    0.62,
    0.67,
    0.45,
    0.76,
    0.67,
    0.38,
    0.33,
    0.67,
    0.48,
    0.6,
    0.64,
    0.55,
    0.38,
    0.24,
    0.62,
    0.38,
    0.48,
    0.57,
    0.52,
    0.81,
    0.64,
]

asc_m = np.transpose([
    [19, 16],
    [19, 12],
    [18, 10],
    [17, 15],
    [18, 13],
    [13, 8],
    [16, 10],
    [15, 8],
    [17, 11],
    [18, 11],
    [16, 8],
    [19, 13],
    [18, 9],
    [17, 11],
    [12, 10],
    [17, 12],
    [25, 18],
    [23, 13],
    [19, 11],
    [17, 10],
    [22, 16],
    [15, 9],
    [19, 11],
    [18, 14],
    [15, 12],
    [25, 15],
    [25, 9],
    [13, 8],
    [19, 11],
    [21, 15],
    [18, 11],
    [18, 3],
    [24, 15],
    [17, 3],
    [15, 9],
    [11, 10],
    [16, 14],
    [25, 23],
    [15, 8],
    [10, 8],
    [15, 13],
    [18, 6],
    [16, 10],
    [25, 16],
    [22, 14],
    [5, 2],
    [18, 3],
    [13, 2],
    [12, 9],
    [20, 12],
    [13, 11],
    [18, 17],
    [8, 6],
    [15, 10],
    [14, 11],
    [22, 5],
    [15, 10],
    [16, 9],
    [19, 11],
    [18, 11],
    [21, 11],
    [21, 9],
    [15, 8],
    [21, 17],
    [10, 8],
    [11, 6],
    [20, 12],
    [18, 6],
    [15, 7],
    [17, 11],
    [3, 3],
    [12, 8],
    [14, 11],
    [9, 9],
    [15, 9],
    [14, 13],
    [18, 13],
    [21, 12],
    [17, 5],
    [13, 9],
    [13, 11],
    [13, 8],
    [12, 6],
    [7, 6],
    [25, 19],
    [16, 9],
    [22, 9],
    [25, 17],
    [16, 11],
    [21, 11],
    [15, 9],
    [19, 10],
    [14, 7],
    [13, 12],
    [17, 10],
    [18, 14],
    [25, 10],
    [11, 7],
    [10, 9],
    [20, 13],
    [10, 9],
    [13, 10],
    [18, 5],
    [16, 11],
    [13, 11],
    [9, 8],
    [22, 12],
    [16, 11],
    [13, 9],
    [14, 12],
    [18, 14],
    [25, 12],
    [24, 14],
])

def get_data_from_csv():
    result = []
    with open(CSV_FILE) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='\t',
                                quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            result.append(row)
    return np.array(result)


data = get_data_from_csv()  # 54 labeled submissions


def print_aucs(arrs: List[List[List[int]]]):
    for a in arrs:
        print(roc_auc_score(a[0], a[1]))


def make_scatter_plot(x, y):
    plt.scatter(x, y)
    plt.show()


def make_histograms(data, labels):
    cols = np.transpose(data)
    labels = iter(labels)

    for col in cols[2:].astype(np.float):
        # fixed bin size:
        bins = np.arange(0, 1, 0.05) # fixed bin size

        plt.xlim([min(col)-0.01, max(col)+0.01])

        plt.hist(col, bins=bins, alpha=0.5)
        plt.title(next(labels))
        plt.xlabel('variable X (bin size = 0.05)')
        plt.ylabel('count')

        plt.show()
        #exit()

def get_sorted_grades(data):
    """
    Extract grades from data and sort the entries from lowest to highest according to human grade.
    """
    cols = np.transpose(data).astype(np.float)

    human_grades = cols[2:5, 2:]/3
    totals = [(cols[2][i] + cols[3][i] + cols[4][i])/3 for i in range(len(cols[0]))]
    cols = np.transpose(np.insert(cols, 0, totals, axis=0))
    cols = np.transpose(cols[cols[:, 0].argsort()])

    return cols


def make_stacked_bar_plots(data, labels):
    """
    Make stacked bar plots. Based on python-graph-gallery.com template.
    """
    cols = get_sorted_grades(data)
    start_col = 3

    for label in labels:
        grades = cols[start_col:start_col + 3, 2:].astype(np.float)/3
                
        # y-axis in bold
        rc('font', weight='bold')
        
        # Values of each group (in different colors)
        bars1 = grades[0]
        bars2 = grades[1]
        bars3 = grades[2]
        
        # Heights of bars1 + bars2
        bars = np.add(bars1, bars2).tolist()
        
        # The position of the bars on the x-axis
        r = range(len(bars1))
        
        # Names of group and bar width
        names = range(1, len(bars1) + 1)
        barWidth = 1
        
        # Create bottom bars
        plt.bar(r, bars1, color='#9617D1', edgecolor='white', width=barWidth)
        # Create middle bars, on top of the first ones
        plt.bar(r, bars2, bottom=bars1, color='#4AA02C', edgecolor='white', width=barWidth)
        # Create top bars
        plt.bar(r, bars3, bottom=bars, color='#1752D1', edgecolor='white', width=barWidth)
        
        plt.title(f"{label} grading")
        plt.xticks(np.arange(0, len(data)-1, 5), np.arange(1, len(data)-1, 5), fontsize=6)
        plt.xlabel("Submission rank")
        plt.yticks(np.arange(0, 1.1, 0.1), [f"{math.floor(100*x)}%" for x in np.arange(0, 1.1, 0.1)], fontsize=7)
        plt.ylabel("Grade")
        plt.legend(["Classes", "Attributes", "Associations"], fontsize=7)
    
        plt.show()
        #plt.savefig(os.path.join(HIST_LOC, f"{label}.png"), format="png")
        
        # exit()

        start_col += 3


def make_grade_compare_scatter(data):
    grades = get_sorted_grades(data)
    
    heur_grades = (grades[6] + grades[7] + grades[8]) / 3
    tc_grades = (grades[9] + grades[10] + grades[11]) / 3

    r = range(len(grades[0]))
    plt.scatter(r, grades[0], color="green")
    plt.scatter(r, heur_grades, color="blue", marker="D")
    plt.scatter(r, tc_grades, color="red", marker="^")
    plt.xlabel("Submission rank")
    plt.ylabel("Grade")
    plt.legend(["Human", "Heuristic", "TouchCore"], fontsize=9)
    plt.show()


def make_assoc_grade_plt(data):
    real_asc = [25*v for v in data]

    a = [list(k) for k in zip(real_asc, asc_m[0], asc_m[1])]
    a.sort()

    a = np.transpose(a)

    x_axis = range(1, 114)

    # lin_comb = [1*s - 0.3*t for s, t in zip(a[1], a[2])]

    plt.scatter(x_axis, a[0], color="green")
    plt.scatter(x_axis, a[1], color="blue", marker="D")
    plt.scatter(x_axis, a[2], color="purple", marker="v")
    plt.xlabel("Submission rank by association grade")
    plt.ylabel("Number of associations deemed correct (Max 25)")
    plt.legend(["Human", "Count all assocs.", "Assocs. w/ correct mult."], fontsize=7)
    # plt.scatter(x_axis, lin_comb, color="purple")

    plt.show()


def cleanup_tc_gui_output(filename: str):
    clean_output = ""

    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        if "INFO" in line or "AWT-EventQueue-0" in line or "Jar URL" in line:
            continue  # skip useless line
        clean_output += line

    with open(filename, "w") as f:
        f.write(clean_output)





if __name__ == "__main__":
    print_aucs([heur_final, tc_final])
    # make_histograms(data, GRADE_DATA_LABELS)
    # make_stacked_bar_plots(data, ["Human", "Heuristic", "TouchCore"])

    # make_grade_compare_scatter(data)
    # make_assoc_grade_plt(real_asc)

    # cleanup_tc_gui_output(TC_GUI_OUTPUT_FILE)
    
    # print(len(real_asc), len(asc_m[0]))
    
    # make_scatter_plot(real_asc, asc_m[0])
    # make_scatter_plot(real_asc, asc_m[1])

    
