#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import scikitplot as skplt

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from typing import List


CSV_FILE = "data/grading.csv"

AUC_OUTPUT_LOC = "figures/"

K = 10  # The 'k' for k-fold cross validation

classifiers = [
    LogisticRegression(C=1e5, max_iter=2000),
    GaussianNB(var_smoothing=0.1),
    RandomForestClassifier(),
    # Also gives same results for 3, 5, 7, 12
    KNeighborsClassifier(n_neighbors=2),
    DecisionTreeClassifier()
]

expected = []
predicted = []

output = {}
probas = {}


def get_data_from_csv():
    result = []
    with open(CSV_FILE) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='\t',
                                quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            result.append(row)
    return np.array(result)


data = get_data_from_csv()  # 54 labeled submissions


def train_model(model, x_train, y_train):
    """
    Train given model to find the relationship y = f(x) and return that model.
    """
    model.fit(np.array(x_train).astype(np.float),
              np.array(y_train).astype(np.float))
    return model


def evaluate(model, x_test, y_test, data_name: str):
    """
    Evaluate trained model on test set. y_test is the expected outcome. 
    """
    global expected
    global predicted
    global output
    global probas

    x_test = np.array(x_test).astype(np.float)
    y_test = np.array(y_test).astype(np.float)
    pred = model.predict(x_test)
    acc = accuracy_score(y_test, pred)
    # print(f"Expected: {y_test}\nActual:   {pred}\nAccuracy: {acc}\n")

    expected.extend(y_test)
    predicted.extend(pred)

    model_name = type(model).__name__
    if model_name not in output:
        output[model_name] = {
            "heuristic": {"expected": [], "predicted": []},
            "heuristicAndTouchcore": {"expected": [], "predicted": []}
        }
    if model_name not in probas:
        probas[model_name] = {
            "heuristic": [],
            "heuristicAndTouchcore": []
        }

    output[model_name][data_name]["expected"].extend(y_test)
    output[model_name][data_name]["predicted"].extend(pred)

    probas[model_name][data_name].extend(model.predict_proba(x_test))

    return acc


def evaluate_all(training_data, test_data):
    # Predict label given heuristic
    x_train = []
    y_train = []
    for e in training_data:
        x_train.append(e[5:8])
        y_train.append(e[1])

    x_test = []
    y_test = []
    for e in test_data:
        x_test.append(e[5:8])
        y_test.append(e[1])

    for clf in classifiers:
        model = train_model(clf, x_train, y_train)
        evaluate(model, x_test, y_test, "heuristic")

    # Predict label given heuristic and TC
    x_train = []
    y_train = []
    for e in training_data:
        x_train.append(e[5:])
        y_train.append(e[1])

    x_test = []
    y_test = []
    for e in test_data:
        x_test.append(e[5:])
        y_test.append(e[1])

    for clf in classifiers:
        model = train_model(clf, x_train, y_train)
        evaluate(model, x_test, y_test, "heuristicAndTouchcore")


def k_fold():
    kf = KFold(n_splits=K)
    for train, test in kf.split(data):
        # use data[train] and data[test] to access the data rows. Both are full rows.
        evaluate_all(data[train], data[test])


def print_results():
    cols: List[str] = ["Expected"]
    # expected is always the same
    exp = output[type(classifiers[0]).__name__]["heuristic"]["expected"]
    preds: List[List[int]] = []
    prbs = []

    for clf in classifiers:
        model_name = type(clf).__name__
        for data_name in ["heuristic", "heuristicAndTouchcore"]:
            cols.append(f"{model_name}_{data_name}")
            preds.append(output[model_name][data_name]["predicted"])
            prbs.append(probas[model_name][data_name])

    print(",".join(cols))

    for p in zip(exp, *preds):
        for v in p:
            print(f"{v},", end="")
        print()

    for c, p in zip(cols[1:], preds):
        print(f"AUC of {c}: {roc_auc_score(exp, p)}")
    
    for clf in classifiers:
        model_name = type(clf).__name__
        for data_name in ["heuristic", "heuristicAndTouchcore"]:
            save_auc(f"{model_name}_{data_name}", exp, np.array(probas[model_name][data_name]))


def print_importances():
    print(classifiers[0].coef_)
    # print(classifiers[1].coef_)
    print(classifiers[2].feature_importances_)
    # print(classifiers[3])
    print(classifiers[4].feature_importances_)


def save_auc(name, expected, predicted):
    skplt.metrics.plot_roc(expected, predicted)
    plt.savefig(os.path.join(AUC_OUTPUT_LOC, f"{name}.png"), format="png")


def debug():
    x_train = []
    y_train = []
    for e in data:
        x_train.append(e[5:8])
        y_train.append(e[1])

    for clf in classifiers:
        model = train_model(clf, x_train, y_train)
        x_test = np.array([[1, 1, 1]])
        print(x_test, model.predict(x_test))


if __name__ == "__main__":
    k_fold()
    print_results()
    print_importances()
