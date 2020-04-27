#!/usr/bin/env python3

import math
import os
import pprint

from typing import Dict


TC_FILE = "data/tc_grade_output.txt"

GRADE_DENOMINATOR = 76  # Assignment is out of 76 marks
N_CLASSES = 7
N_ATTRIB = 16
N_ASSOC = 13
CLASS_WEIGHT = 2  # in points
ATTRIB_WEIGHT = 1
ASSOC_WEIGHT = 1


def get_tc_output_from_file(filename: str) -> Dict[int, str]:
    result = {}
    with open(filename, "r") as f:
        content = f.read()

    gradings = content.split("out/")
    for g in gradings:
        if g:
            f, c = g.split(".cdm")
            result[f] = c
    
    return result


def get_n_matched_classes(feedback: str) -> int:
    """
    Return the number of matched classes in the feedback of a single submission.
    """
    return max(0, N_CLASSES - feedback.count("Missing class") - feedback.count("Matched Class for")) 


def get_n_matched_attributes(feedback: str) -> int:
    """
    Return the number of matched attributes in the feedback of a single submission.
    """
    return math.ceil(max(0, N_ATTRIB - feedback.count("Attribute missing") - 0.5*feedback.count("Attribute Misplaced")))


def get_n_matched_associations(feedback: str) -> int:
    """
    Return the number of matched associations in the feedback of a single submission.
    """
    total_matches = feedback.count("Matched")
    class_matches = feedback.count("Class Matched")
    attr_matches = feedback.count("Attribute Match")

    return max(0, total_matches - class_matches - attr_matches)


def get_tc_grade(feedback: str, n_assoc: int=0) -> float:
    stated_marks = float(feedback.split("Final result:")[1].strip())
    if not n_assoc:
        n_assoc = get_n_matched_associations(feedback)
    return stated_marks + ASSOC_WEIGHT * n_assoc - CLASS_WEIGHT * feedback.count("Matched Class for")


def show_touchcore_grading():
    tc_output = get_tc_output_from_file(TC_FILE)
    for k in sorted(tc_output.keys(), key=int):
        feedback = tc_output[k]

        classes = get_n_matched_classes(feedback)
        attrib = get_n_matched_attributes(feedback)
        assoc = get_n_matched_associations(feedback)
        grade = get_tc_grade(feedback, assoc)

        #print(f"{k},{classes},{attrib},{assoc},{grade}")
        print(attrib)



if __name__ == "__main__":
    # pp = pprint.PrettyPrinter(width=120)
    # pp.pprint(get_tc_output_from_file(TC_FILE))
    show_touchcore_grading()
