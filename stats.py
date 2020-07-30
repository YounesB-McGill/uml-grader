#!/usr/bin/env python3

import csv
import numpy as np

from scipy.stats import spearmanr


CSV_FILE = "data/BC_grading_a2_final.csv"


def get_data_from_csv():
    result = []
    with open(CSV_FILE) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='\t',
                                quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            result.append(row)
    return np.array(result).astype(np.float)


data = get_data_from_csv()
dataT = np.transpose(data)

# calculate spearman's correlation
for i in range(2, len(dataT)):
    for j in range(i, len(dataT)):
        if i != j:
            corr, _ = spearmanr(dataT[i], dataT[j])
            print(i, j, corr)
