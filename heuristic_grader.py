#!/usr/bin/env python3

import os
from typing import Dict, Tuple

SUBMISSIONS_LOC = "dataset/umple_files"

N_CLASSES = 7
N_ASSOC = 13

EXPECTED_CLASSES = [
    ["FantasyBasketball"],
    ["Match", "Game"],
    ["Team", "RealTeam", "RTeam"],
    ["VirtualTeam", "VTeam"],
    ["Player", "NbaPlayer"],
    ["PlayerStat", "Stat"],
    ["VirtualScore", "VScore"],
]

EXPECTED_ATTRIBUTES = [
    "season", "matchId", "season", "name", "score", "ranking", "name", "budget",
    "first", "last", "id", "salary",
    "points", "assists", "rebounds", "score",
]

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


def get_all_submissions() -> Dict[str, str]:
    result = {}
    for filename in os.listdir(SUBMISSIONS_LOC):
        if filename.endswith(".ump"):
            with open(os.path.join(SUBMISSIONS_LOC, filename), "r") as f:
                result[filename] = f.read()
    return result


def get_n_classes(submission: str) -> int:
    n = submission.count("class")
    if "//$?[End_of_model]$?" in submission:
        n //= 2
    return n


def get_n_assoc(submission: str) -> int:
    # assuming all associations are converted to bidirectional
    return submission.count("--")


def get_n_expected_classes(submission: str) -> int:
    result = 0
    submission = submission.lower()

    for class_group in EXPECTED_CLASSES:
        for class_name in class_group:
            if class_name.lower() in submission:
                result += 1
                break

    return result


def get_n_expected_attributes(submission: str) -> int:
    result = 0
    submission = submission.lower()

    for attribute in EXPECTED_ATTRIBUTES:
        if attribute.lower() in submission:
            result += 1
            # print(f"Found expected attribute: {attribute}")

            # prevent double counting
            submission = submission.replace(attribute.lower(), "", 1)

    return result
    

def grade_submission(submission: Tuple[str, str]):
    name, text = submission
    if name not in FILE_MAPPINGS:
        return
    
    file_mapping = FILE_MAPPINGS[name]
    n_classes = get_n_classes(text)
    n_assoc = get_n_assoc(text)
    n_exp_cls = get_n_expected_classes(text)
    n_exp_attr = get_n_expected_attributes(text)

    print(f"{file_mapping},{n_classes},{n_assoc},{n_exp_cls},{n_exp_attr}")


def grade_all_using_heuristic():
    submissions = get_all_submissions()
    for s in submissions.items():
        grade_submission(s)


def debug():
    with open(os.path.join(SUBMISSIONS_LOC, "9_BasketBall.ump"), "r") as f:
        text = f.read()
    print(get_n_expected_attributes(text))
    grade_submission()


if __name__ == "__main__":
    grade_all_using_heuristic()
    #debug()
