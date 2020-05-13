#!/usr/bin/env python3

import json
import os
import openpyxl
import pprint

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from typing import Dict, List

UML_FILE_LOC = "../ECSE223_FinalExam_W20/DomainModeling"
FEEDBACK_LOC = "../ECSE223_FinalExam_W20/Q2"
STUDENT_ENTRIES_FILE = "final_data/entries.json"
MARKING_SCHEME_TEMPLATE = f"{FEEDBACK_LOC}/0Lastname-Firstname-ECSE223-W2020-Final-Q2.xlsx"

CLASS_CELLS = [
    "A2", "A6", "A12", "A15", "A18", "A22", "A28", "A31", "A34", "A38",
    "D2", "D6", "D11", "D19", "D25", "D28", "D32", "D36"
]

ATTRIB_CELLS = [
    "A13", "A13", "A25", "A26",
    "D4", "D8", "D14", "D16", "D21"
]

ASSOC_CELLS = [
    "A3", "A4", "A7", "A8", "A9", "A10", "A19", "A20", "A35", "A36", "A39", "A40", 
    "D9", "D17", "D22", "D23", "D30", "D34", "D39", "D40" 
]

MARKING_SCHEME_WORKSHEET = openpyxl.load_workbook(MARKING_SCHEME_TEMPLATE, data_only=True)["Semantics"]

# declared here to allow setting MAX__POINTS below
def get_cell_sum(worksheet: Worksheet, cells: List[str]) -> float:
    """Return the sum of the indicated cells in the given worksheet, shifted down if needed."""
    result = 0
    shift = 0
    if worksheet["B1"].value is None: shift = 1
    for cell in cells:
        c = f"{cell[0]}{int(cell[1:]) + shift}"  # assume cols don't exceed Z, else use regex
        if worksheet[c].value: result += float(worksheet[c].value)
    return result

ADDITIONAL_ATTRIB_DEDUCTION = 1.5  # graders can increase attribute deduction by this amount

# negative sign since they are deductions
MAX_CLASS_POINTS = -get_cell_sum(MARKING_SCHEME_WORKSHEET, CLASS_CELLS)
MAX_ATTRIB_POINTS = -get_cell_sum(MARKING_SCHEME_WORKSHEET, ATTRIB_CELLS) + ADDITIONAL_ATTRIB_DEDUCTION
MAX_ASSOC_POINTS = -get_cell_sum(MARKING_SCHEME_WORKSHEET, ASSOC_CELLS)
MAX_CAA_POINTS = MAX_CLASS_POINTS + MAX_ATTRIB_POINTS + MAX_ASSOC_POINTS

pp = pprint.PrettyPrinter(width=120)


def make_student_entries() -> Dict[int, List[str]]:
    """
    Entries in form 1: ["FirstLast", "FL.uml", "FL.xlsx"]
    """
    result = {}
    i = 1
    for filename in os.listdir(FEEDBACK_LOC):
        if filename[0] in [".", "0"]:  # skip template and hidden temp files
            continue
        name = "".join(filename.replace("-ECSE223-W2020-Final-Q2.xlsx", "").split("-")[::-1])
        result[i] = [name, "", filename]
        i += 1

    for i in result.keys():
        target_name = result[i][0].lower()
        for filename in os.listdir(UML_FILE_LOC):
            if "ump" in filename:
                name = filename.split(" - ")[1].replace(" ", "").lower()
                if name == target_name or name in target_name or target_name in name:
                    result[i][1] = filename
                    break

    pp.pprint(result)
    return result


def save_to_json(content, filename: str):
    with open(filename, "w") as f:
        json.dump(content, f, indent=2)


def read_from_json(filename: str) -> Dict:
    with open(filename, "r") as f:
        return json.load(f)


def extract_manual_grades_from_feedback_files(entries: Dict, feedback_loc: str) -> Dict:
    """
    Add the class, attribute, association, and total grade to each entry.
    """
    for i in range(1, len(entries) + 1):
    #for i in range(55,56):
        entry = entries[f"{i}"]
        feedback_file = entry[2]
        
        excel_file = openpyxl.load_workbook(os.path.join(feedback_loc, feedback_file), data_only=True)
        summary_page: Worksheet = excel_file["Summary"]
        semantics_page: Worksheet = excel_file["Semantics"]
        syntax_page: Worksheet = excel_file["Syntax"]

        total_points = float(summary_page["A1"].value)
        max_points = float(summary_page["B1"].value)
        total_grade = total_points / max_points

        class_marks = get_class_marks(semantics_page)
        attrib_marks = get_attrib_marks(semantics_page)
        assoc_marks = get_assoc_marks(semantics_page)
        caa_grade = (MAX_CLASS_POINTS*class_marks + MAX_ATTRIB_POINTS*attrib_marks + MAX_ASSOC_POINTS*assoc_marks
            ) / MAX_CAA_POINTS

        print(f"{i},{class_marks:.2f},{attrib_marks:.2f},{assoc_marks:.2f},{caa_grade:.2f},{total_grade:.2f}")

    return entries


# adding get_cell_sum() since it is negative
def get_class_marks(semantics_page: Worksheet) -> float:
    return (MAX_CLASS_POINTS + get_cell_sum(semantics_page, CLASS_CELLS)) / MAX_CLASS_POINTS


def get_attrib_marks(semantics_page: Worksheet) -> float:
    return (MAX_ATTRIB_POINTS + get_cell_sum(semantics_page, ATTRIB_CELLS)) / MAX_ATTRIB_POINTS


def get_assoc_marks(semantics_page: Worksheet) -> float:
    return (MAX_ASSOC_POINTS + get_cell_sum(semantics_page, ASSOC_CELLS)) / MAX_ASSOC_POINTS


if __name__ == "__main__":
    # save_to_json(make_student_entries(), STUDENT_ENTRIES_FILE + ".new")  # avoid overwriting file by mistake
    extract_manual_grades_from_feedback_files(read_from_json(STUDENT_ENTRIES_FILE), FEEDBACK_LOC)

