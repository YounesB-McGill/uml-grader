#!/usr/bin/env python3

import csv
import math
import numpy as np
import os
import scikitplot as skplt

from matplotlib import pyplot as plt, rc
from random import randint
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, roc_auc_score, roc_curve
from typing import List

CSV_FILE = "data/LG_grading_a2_final.csv"

TC_GUI_OUTPUT_FILE = "tc_output_final2.txt"

HIST_LOC = "figures/histograms_a2"

GRADE_DATA_LABELS = [
    "Human Classes", "Human Attributes", "Human Assocs",
    "Heuristic Classes", "Heuristic Attributes", "Heuristic Assocs",
    "TouchCore Classes", "TouchCore Attributes", "TouchCore Assocs",
]

# weights of classes, attributes, associations
CW = 13.5
AT = 6
AS = 10.5
TOT = CW + AT + AS


def get_data_from_csv():
    result = []
    with open(CSV_FILE) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='\t',
                                quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            result.append(row)
    return np.array(result)


data = get_data_from_csv()


def print_aucs(arrs: List[List[List[int]]]):
    a = [np.array([
            1., 0., 1., 1., 1., 1., 0., 1., 1., 0., 1., 0., 1., 1., 1., 1., 1.,
            1., 1., 1., 1., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
            0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
            1., 1., 1., 0., 0., 1., 1., 1., 0., 0., 1., 1., 1., 1., 1., 1., 1.,
            1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 1., 1., 1., 1.,
            0., 1., 1., 1., 1., 1., 1., 0., 1., 1., 1., 1., 1., 0., 1., 1., 1.,
            1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 1., 1., 1., 1., 1., 1.,
            1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 1., 1., 1.,
            1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 1.,
            1., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 1.]), 
        np.array([
            0.99999999, 0.00772525, 0.81298369, 0.99934435, 0.92444068,
            0.98533125, 0.8952006 , 0.85260627, 0.99903211, 0.85260627,
            0.98503916, 0.20477261, 0.99755715, 0.99165529, 0.99842453,
            0.98503916, 0.86753505, 0.99850074, 0.98031467, 0.99230478,
            0.95100732, 0.51918326, 0.84595841, 0.9955758 , 0.94696996,
            0.93588817, 0.85844227, 0.99758965, 0.9366941 , 0.99638892,
            0.99191196, 0.90071118, 0.89174479, 0.98990188, 0.86817098,
            0.99966066, 0.99060161, 0.14774588, 0.83306222, 0.99897557,
            0.99965043, 0.99534486, 0.99637228, 0.80514006, 0.99868446,
            0.95224276, 0.99942489, 0.99950952, 0.92581328, 0.90513568,
            0.87825553, 0.99321227, 0.96299095, 0.99263764, 0.49787474,
            0.90438348, 0.81854403, 0.8596234 , 0.95042033, 0.36179492,
            0.94157958, 0.96914182, 0.96353405, 0.64075503, 0.96625395,
            0.91162803, 0.99001124, 0.96308589, 0.99397395, 0.99723348,
            0.98285817, 0.7871091 , 0.99388325, 0.15555838, 0.97586065,
            0.72949416, 0.98386461, 0.44063352, 0.89374521, 0.97489488,
            0.03813973, 0.94974162, 0.95886355, 0.9654003 , 0.13930681,
            0.3305758 , 0.9954579 , 0.67690414, 0.97246475, 0.98893835,
            0.99359876, 0.97402544, 0.37716418, 0.96931805, 0.99874364,
            0.57991668, 0.94644425, 0.97338835, 0.54199546, 0.88969379,
            0.99999717, 0.99042778, 0.99077401, 0.98630324, 0.90823905,
            0.96296438, 0.67729692, 0.99997313, 0.93156203, 0.99145667,
            0.98309165, 0.97567031, 0.84158371, 0.96645148, 0.95640149,
            0.87361678, 0.74335703, 0.94383168, 0.69400719, 0.96923587,
            0.99238665, 0.79772092, 0.95239504, 0.96590156, 0.76847585,
            0.9996251 , 0.98779209, 0.97679223, 0.99628349, 0.96910453,
            0.90590191, 0.67477306, 0.69013539, 0.99777207, 0.99555471,
            0.99590808, 0.98447776, 0.9995678 , 0.99990614, 0.43288971,
            0.97197766, 0.99342868, 0.89624305, 0.75400718, 0.89788596,
            0.91872198, 0.98520536, 0.99148355, 0.89274607, 0.97876591,
            0.97309142, 0.75726347, 0.99106025, 0.99931261, 0.62985433,
            0.99871322, 0.94442072, 0.98570777, 0.96889669, 0.99229819,
            0.99839882, 0.53026455, 0.99421764, 0.97342904, 0.99080842,
            0.83373029, 0.40259452, 0.7232858 ])]
    for a in [a]: # arrs:
        print(roc_auc_score(a[0], a[1]))
        print(np.array(a[0]).shape, np.array(a[1]).shape)
        for v in a[1]:
            if v:
                v -= 0.01 * randint(1, 10)
                #break
        skplt.metrics.plot_roc(a[0], a[1], title=f"ROC Curves")


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
    #CW = AT = AS = 1
    totals = [(CW*cols[2][i] + AT*cols[3][i] + AS*cols[4][i])/TOT for i in range(len(cols[0]))]
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


def make_lg_plots(expected: List[float], predicted: List[float], num_letter_grades: int=5):
    """
    Make letter grade plots that show how many submissions were over/underrated, and to what extent.

    expected: list of grades given by human grader \\
    predicted: list of grades predicted by the classifier, in the same order \\
    num_letter_grades: the number of possible letter grades in the grading scheme considered, including the zero grade.
    Default is 5 (for A-F).
    """
    x = [i for i in range(-num_letter_grades + 1, num_letter_grades)]
    grades = [0 for i in range(2*num_letter_grades - 1)]
    for e, p in zip(expected, predicted):
        d = round(p - e)
        # shift from [-2 -1 0 1 2] to array indices
        grades[d + num_letter_grades - 1] += 1
    
    colors = make_letter_grade_colors(num_letter_grades)

    barWidth = 1
    plt.bar(x, grades, color=colors, width=barWidth)
    plt.xlabel("Difference from human grade")
    plt.ylabel("Number of submissions")
    plt.xticks(x)

    X_OFFSET_SD = 4.05
    X_OFFSET_DD = 4.2
    Y_OFFSET = 0.75

    for i, v in enumerate(grades):
        if 0 < v < 10:
            plt.text(i - X_OFFSET_SD, v + Y_OFFSET, v)
        elif v:
            plt.text(i - X_OFFSET_DD, v + Y_OFFSET, v)

    plt.show()


def make_lg_multiplots(expected: List[float], predicteds: List[List[float]], num_letter_grades: int=5):
    n = len(predicteds)
    x = [i for i in range(-num_letter_grades + 1, num_letter_grades)]
    x1 = [i-0.16 for i in range(-num_letter_grades + 1, num_letter_grades)]
    x2 = [i+0.16 for i in range(-num_letter_grades + 1, num_letter_grades)]
    grades = [[0 for i in range(2*num_letter_grades - 1)] for i in range(n)]

    for i, predicted in enumerate(predicteds):
        print(f"predicted[{i}]: {predicted}")
        for e, p in zip(expected, predicted):
            d = round(p - e)
            # shift from [-2 -1 0 1 2] to array indices
            grades[i][d + num_letter_grades - 1] += 1

    print(grades)

    grades[1][1] += 0.25
    grades[0][6] += 0.25
    
    colors = make_letter_grade_colors(num_letter_grades)

    barWidth = 1/(1.5*n)
    # can add patterns with hatch="///"
    plt.bar(x1, grades[0], color=colors, width=barWidth, edgecolor="black", lw=0.5)
    plt.bar(x2, grades[1], color=colors, width=barWidth, edgecolor="black", lw=0.5)
    plt.xlabel("Difference from human grade")
    plt.ylabel("Number of submissions")
    plt.xticks(x)

    X_OFFSET_SD = 4.05
    X_OFFSET_DD = 4.2
    X_OFFSET_MC = 0.16
    Y_OFFSET = 0.75

    for i in range(len(grades[0])):
        v1 = grades[0][i]
        v2 = grades[1][i]

        if v1 == v2:
            v = v1
            if 0 < v < 10:
                plt.text(i - X_OFFSET_SD, v + Y_OFFSET, v)
            elif v:
                plt.text(i - X_OFFSET_DD + 0.02, v + Y_OFFSET, v)
        else:
            if 0 < v1 < 10:
                plt.text(i - X_OFFSET_SD - X_OFFSET_MC - 0.04, v1 + Y_OFFSET, round(v1))
            elif v1:
                if v1 == 22:
                    plt.text(i - X_OFFSET_DD - X_OFFSET_MC + 0.02, v1 + Y_OFFSET, v1)
                else:
                    plt.text(i - X_OFFSET_DD - X_OFFSET_MC, v1 + Y_OFFSET, v1)
            if 0 < v2 < 10:
                plt.text(i - X_OFFSET_SD + X_OFFSET_MC - 0.02, v2 + Y_OFFSET, round(v2))
            elif v2:
                if v2 in [48, 30]:
                    plt.text(i - X_OFFSET_DD + X_OFFSET_MC + 0.02, v2 + Y_OFFSET, v2)
                else:
                    plt.text(i - X_OFFSET_DD + X_OFFSET_MC, v2 + Y_OFFSET, v2)

    plt.show()


def make_letter_grade_colors(num_letter_grades: int=5) -> List[str]:
    result = []

    possible_colors = [
        "#32a852",  # Green, Good
        "#edc911",  # Yellow, Off by one
        "#ff8f8f",  # Light red, off by 2
        "#b50707",  # Dark red, off by 3 or more
    ]

    for i in range(num_letter_grades):
        if i == 0:
            result.append(possible_colors[0])
        elif i < 4:
            result.insert(0, possible_colors[i])
            result.append(possible_colors[i])
        else:
            result.insert(0, possible_colors[-1])
            result.append(possible_colors[-1])

    return result


def make_grade_compare_scatter(data):
    grades = get_sorted_grades(data)
    
    heur_grades = (CW*grades[6] + AT*grades[7] + AS*grades[8]) / TOT
    tc_grades = (CW*grades[9] + AT*grades[10] + AS*grades[11]) / TOT

    grades[0][0] = heur_grades[0] = tc_grades[0] = 2

    r = range(len(grades[0]))
    size = 11
    plt.scatter(r, grades[0], s=size, color="green")
    plt.scatter(r, heur_grades, s=size, color="blue", marker="D")
    plt.scatter(r, tc_grades, s=size, color="red", marker="^")
    plt.ylim(0, 1.1)
    plt.xticks(np.arange(0, len(data)-1, 10))
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

    size = 10
    plt.scatter(x_axis, a[0], s=size, color="green")
    plt.scatter(x_axis, a[1], s=size, color="blue", marker="D")
    plt.scatter(x_axis, a[2], s=size, color="purple", marker="v")
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


def print_performance_metrics(y_true, y_pred):
    avg = "macro"  # micro is same as average

    m = 100  # to make publishing data easier
    f = "{:2.2f}"

    auc_pred = make_auc_pred(y_pred)

    print(f"{f.format(m * accuracy_score(y_true, y_pred))}\n"
          f"{f.format(m * precision_score(y_true, y_pred, average=avg, zero_division=0))}\n"
          f"{f.format(m * recall_score(y_true, y_pred, average=avg))}\n"
          f"{f.format(m * f1_score(y_true, y_pred, average=avg))}\n"
          f"{f.format(m * roc_auc_score(np.array(y_true), auc_pred, multi_class='ovr'))}\n")


def make_auc_pred(y_pred):
    result = []

    for v in y_pred:
        zc = np.zeros(5)
        zc[v] = 1
        result.append(zc)

    return result

if __name__ == "__main__":
    """
    Main entry point. Call the relevant function from above with the correct input here.
    """  
