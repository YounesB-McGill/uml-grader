#!/usr/bin/env python3

import json
import re
import os
import pprint
import sys

from collections import Counter
from typing import Dict, List, Tuple


if len(sys.argv) < 2:
    print("Usage: ./heuristic_grader.py marking_scheme.json umple_files_dir [showExtras]")
    exit(-1)


MARKING_SCHEME_FILE = sys.argv[1]
SUBMISSIONS_LOC = "final_data/umple_files"  # "dataset/umple_files"

BASIC_TYPES = ["Boolean", "boolean", "Integer", "int", "Float", "float", "Double", "double", "String"]
UMPLE_KEYWORDS = ["class", "isA", "--", "association", "abstract"]

FREQ_THRESH = 3  # Number of occurences required to consider a word 'frequent'

frequent_extra_classes = Counter()
frequent_extra_attributes = Counter()

IDEAL_ASSOC_MULTS = []

FILE_MAPPINGS = dict((v, k) for k, v in {
    "0.cdm": "0_ideal_solution.ump",
    "1.cdm": "10_Assignment2.ump",
    "2.cdm": "11_main.ump",
    "3.cdm": "12_fantasybasket.ump",
    "4.cdm": "13_FantasyBasketBallUmple.ump",
    "5.cdm": "15_FantasyBasketball.ump",
    "6.cdm": "19_model.ump",
    "7.cdm": "1_FantasyBasketball.ump",
    "8.cdm": "20_a2.ump",
    "9.cdm": "21_UmpleCode.ump",
    "10.cdm": "22_umpleProgram.ump",
    "11.cdm": "24_FantasyBasketball.ump",
    "12.cdm": "25_model.ump",
    "13.cdm": "26_FantasyBasketBall.ump",
    "14.cdm": "28_a2.ump",
    "15.cdm": "29_FantasyBasketball.ump",
    "16.cdm": "2_FantasyBasketball.ump",
    "17.cdm": "31_FantasyLeague.ump",
    "18.cdm": "32_FancyBasketballGame.ump",
    "19.cdm": "33_FantasyBasketballGame.ump",
    "20.cdm": "34_assignment2umplecode.ump",
    "21.cdm": "35_fantasyBasketball.ump",
    "22.cdm": "36_fantasy.ump",
    "23.cdm": "37_FantasyBasketballModel.ump",
    "24.cdm": "38_FantasyBasketballCompetition.ump",
    "25.cdm": "39_fantacyBasketball.ump",
    "26.cdm": "40_main.ump",
    "27.cdm": "41_Assignment2Model.ump",
    "28.cdm": "42_FantasyBasketball.ump",
    "29.cdm": "43_model.ump",
    "30.cdm": "45_FantasyBasketball.ump",
    "31.cdm": "46_BasketballECSE321.ump",
    "32.cdm": "47_FantasyBasketballGame.ump",
    "33.cdm": "49_main.ump",
    "34.cdm": "4_FantasyBasketBallGame.ump",
    "35.cdm": "50_Umple_Code.ump",
    "36.cdm": "52_FantasyBasketBall.ump",
    "37.cdm": "56_Umple_Code.ump",
    "38.cdm": "57_FantasyBasketBall.ump",
    "39.cdm": "58_fantasyBasketball.ump",
    "40.cdm": "5_model.ump",
    "41.cdm": "60_FantasyBasketballGame.ump",
    "42.cdm": "61_main.ump",
    "43.cdm": "62_Umple.ump",
    "44.cdm": "63_FBL.ump",
    "45.cdm": "65_assignment2.ump",
    "46.cdm": "66_FantasyBasketballModelJava.ump",
    "47.cdm": "67_UmpleCode.ump",
    "48.cdm": "68_FBGS.ump",
    "49.cdm": "69_fantasybasketballmodel.ump",
    "50.cdm": "70_FantasyBasketballGame.ump",
    "51.cdm": "7_FantasyBasketballGame.ump",
    "52.cdm": "8_model.ump",
    "53.cdm": "9_BasketBall.ump",
}.items())

pp = pprint.PrettyPrinter(indent=2)


def get_all_submissions(path=None) -> Dict[str, str]:
    if path is None:
        path = SUBMISSIONS_LOC
    result = {}
    for filename in os.listdir(path):
        if filename.endswith(".ump"):
            with open(os.path.join(path, filename), "r") as f:
                result[filename] = f.read()
    return result


def get_probable_declared_classes(submission: str) -> List[str]:
    result = []
    submission = submission.replace("\t", "  ")
    chunks = submission.split("class")
    for c in chunks:
        c = re.sub(r"[^A-Za-z0-9 ]+", "", c)
        sc = c.split()
        if sc:
            result.append(sc[0].strip())
    return result


def get_probable_declared_attributes(submission: str) -> List[str]:
    result = set()
    submission_lines = submission.replace("\t", "  ").splitlines()
    classes = get_probable_declared_classes(submission)
    for line in submission_lines:
        if not any(m in line for m in UMPLE_KEYWORDS):
            words = re.sub(r"[^A-Za-z ]+", "", line).split()
            for word in words:
                if word not in classes and word not in BASIC_TYPES and word != "enum":
                    result.add(word)
    
    return list(result)


def get_association_multiplicities(umple_text: str, bidirectional=False) -> List[str]:
    result = []
    lines = umple_text.splitlines()
    for line in lines:
        if "--" in line:
            line = "".join(c for c in line if not c.isalpha())
            lhs, rhs = line.split("--")
            result.append(f"{lhs.split()[-1]}--{rhs.split()[0]}")
            if bidirectional:
                result.append(f"{rhs.split()[0]}--{lhs.split()[-1]}")
    return result


def get_n_classes(submission: str) -> int:
    n = submission.count("class")
    if "//$?[End_of_model]$?" in submission:
        n //= 2
    return n


def get_n_assoc(submission: str, max_assoc: int) -> int:
    # assuming all associations are converted to bidirectional
    return min(max_assoc, submission.count("--"))


def get_n_assoc_with_mult(submission: str, ideal_mult: List[str], max_assoc: int):
    result = 0

    submission_assocs = get_association_multiplicities(submission)

    for assoc in ideal_mult:
        if assoc in submission_assocs:
            result += 1
            submission_assocs.remove(assoc)  # prevent double counting

    return min(max_assoc, result)


def get_n_expected_classes(submission: str, expected_classes: List[List[str]], max_classes: int,
                           show_unmatched: bool=False) -> int:
    global frequent_extra_classes
    result = 0

    probable_declared_classes = get_probable_declared_classes(submission)
    unmatched_classes = []

    submission = submission.lower()

    for class_group in expected_classes:
        matched = False
        for class_name in class_group:
            if class_name.lower() in submission:
                matched = True
                result += 1
                submission.replace(class_name.lower(), "", 1)  # avoid double counting
                if class_name in probable_declared_classes:
                    probable_declared_classes.remove(class_name)
                break
        if not matched:
            unmatched_classes.append(class_group[0])

    frequent_extra_classes.update(probable_declared_classes)

    if show_unmatched and unmatched_classes:
        print(f"""Could not find these classes:\n{unmatched_classes}\nBut found these classes instead:\n{
               probable_declared_classes}\n""")

    return min(result, max_classes)


def get_n_expected_attributes(submission: str, expected_attributes: List[str]) -> int:
    global frequent_extra_attributes
    result = 0
    probable_declared_attributes = get_probable_declared_attributes(submission)
    submission = submission.lower()

    for attribute in expected_attributes:
        if attribute.lower() in submission:
            result += 1

            # prevent double counting
            submission = submission.replace(attribute.lower(), "", 1)

            if attribute in probable_declared_attributes:
                probable_declared_attributes.remove(attribute)

    frequent_extra_attributes.update(probable_declared_attributes)

    return min(result, len(expected_attributes))
    

def grade_submission(submission: Tuple[str, str], marking_scheme: Dict):
    name, text = submission
    # if name not in FILE_MAPPINGS:
    #     return

    expected_classes = marking_scheme["expectedClasses"]
    expected_attributes = marking_scheme["expectedAttributes"]
    max_exp_classes = marking_scheme["nClasses"]
    max_assoc = marking_scheme["nAssoc"]

    file_mapping = int(name.replace(".ump", ""))  # FILE_MAPPINGS[name]
    
    n_exp_cls = get_n_expected_classes(text, expected_classes, max_exp_classes, show_unmatched=False)
    n_exp_attr = get_n_expected_attributes(text, expected_attributes)
    n_assoc = get_n_assoc(text, max_assoc)
    n_mult = get_n_assoc_with_mult(text, IDEAL_ASSOC_MULTS, max_assoc)

    #print(f"{file_mapping},{n_exp_cls},{n_exp_attr},{n_assoc}")
    return [file_mapping, n_exp_cls, n_exp_attr, n_assoc, n_mult]


def grade_all_using_heuristic(marking_scheme_file: str, submission_path: str=None):
    global IDEAL_ASSOC_MULTS
    result = []

    with open(marking_scheme_file) as f:
        marking_scheme = json.load(f)

    submissions = get_all_submissions(submission_path)
    IDEAL_ASSOC_MULTS = get_association_multiplicities(submissions["0.ump"], bidirectional=True)
    
    for s in submissions.items():
        result.append(grade_submission(s, marking_scheme))

    result.sort(key=lambda x: x[0])

    for r in result:
        print(",".join(map(str, r)))

    return result


def show_most_frequent(ranking: Dict[str, int], thresh: int):
    print(json.dumps({k: v for k, v in sorted(
        {c: f for c, f in ranking.items() if f >= thresh}.items(), key=lambda item: -item[1])}, indent=2))


def debug():
    with open(os.path.join(SUBMISSIONS_LOC, "9_BasketBall.ump"), "r") as f:
        text = f.read()
    print(get_n_expected_attributes(text))
    grade_submission()


if __name__ == "__main__":
    "Main entry point."
    grade_all_using_heuristic(MARKING_SCHEME_FILE, sys.argv[2])

    if len(sys.argv) > 3 and "showextras" in sys.argv[3].lower():
        show_most_frequent(frequent_extra_classes, FREQ_THRESH)
        show_most_frequent(frequent_extra_attributes, FREQ_THRESH)    
