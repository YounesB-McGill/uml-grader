#!/usr/bin/env python3

import csv
import math
import numpy as np

from matplotlib import pyplot as plt, rc
from sklearn.metrics import roc_auc_score, roc_curve

CSV_FILE = "data/grading.csv"

GRADE_DATA_LABELS = [
    "Human Classes", "Human Attributes", "Human Assocs",
    "Heuristic Classes", "Heuristic Attributes", "Heuristic Assocs",
    "TouchCore Classes", "TouchCore Attributes", "TouchCore Assocs",
]

# Expected, predicted
heur = np.transpose([
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 1],
    [1, 1],
    [1, 1],
    [0, 1],
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
    [0, 1],
    [1, 1],
    [1, 1],
    [1, 0],
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
])

tc = np.transpose([
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [0, 1],
    [1, 1],
    [1, 1],
    [0, 0],
    [1, 1],
    [0, 0],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 1],
    [1, 0],
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
    [1, 0],
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


def print_aucs():
    print(roc_auc_score(heur[0], heur[1]))
    print(roc_auc_score(tc[0], tc[1]))


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


def make_stacked_bar_plots(data, labels):
    """
    Make stacked bar plots. Based on python-graph-gallery.com template.
    """
    cols = np.transpose(data)
    start_col = 2

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
        plt.bar(r, bars1, color='#7f6d5f', edgecolor='white', width=barWidth)
        # Create middle bars, on top of the first ones
        plt.bar(r, bars2, bottom=bars1, color='#557f2d', edgecolor='white', width=barWidth)
        # Create top bars
        plt.bar(r, bars3, bottom=bars, color='#2d7f5e', edgecolor='white', width=barWidth)
        
        plt.title(labels)
        plt.xticks(np.arange(0, 54, 2), np.arange(1, 54, 2), fontsize=7)
        plt.xlabel("submission id")
        plt.yticks(np.arange(0, 1.1, 0.1), [f"{math.floor(100*x)}%" for x in np.arange(0, 1.1, 0.1)], fontsize=7)
        plt.ylabel("grade")
    
        # Show graphic
        plt.show()

        start_col += 3
        exit()



if __name__ == "__main__":
    # print_aucs()
    # make_histograms(data, GRADE_DATA_LABELS)
    make_stacked_bar_plots(data, ["Human", "Heuristic", "TouchCore"])

