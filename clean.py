#!/usr/bin/env python3

import glob
import json
import re
import os
import pathlib
import shutil
import subprocess
import sys
import zipfile

from pyunpack import Archive
from typing import Dict

# To avoid bloating this repository, make this point to your local umple executable
UMPLE_BIN = os.path.expanduser("~/umple/dev-tools/umple")

DATA_LOC = "final_data/umple_files"  # "dataset"
UMPLE_FILES_LOC = "final_data/umple_files"  # "dataset/umple_files"
TMP_LOC = "tmp2/"


def transform_ump_to_ecore():
    for filename in os.listdir(UMPLE_FILES_LOC):
        cmd = f'{UMPLE_BIN} --generate Ecore ../umple_files/{filename}'
        print(cmd)
        # proc = run_process(f'{UMPLE_BIN} --generate Ecore "{filename}"')

        # if proc.returncode != 0:
        #     print(proc.stderr)


def anonymize_filenames(entries: Dict):
    for k in entries.keys():
        try:
            shutil.copy2(os.path.join(UMPLE_FILES_LOC, entries[k][1]),
                        os.path.join(UMPLE_FILES_LOC, f"{k}.ump"))
            os.remove(os.path.join(UMPLE_FILES_LOC, entries[k][1]))
        except:
            print(f"Failed to rename {k}")


def extract_and_clean_data(path: str):
    # Files already extracted
    for filename in os.listdir(path):
        if filename.endswith(".html"):
            os.remove(os.path.join(path, filename))

        if filename.endswith((".zip", ".7z")) and not os.path.isdir(os.path.join(path, filename)):
            print(f"Attempting to open {filename}")
            Archive(os.path.join(path, filename)).extractall(os.path.join(path, "".join(filename.split(".")[:-1])))

    
    pathlib.Path(UMPLE_FILES_LOC).mkdir(parents=True, exist_ok=True)
    pathlib.Path(TMP_LOC).mkdir(parents=True, exist_ok=True)

    # Files already copied
    n = 0
    for filename in glob.iglob(DATA_LOC + "/**/*.ump", recursive=True):
        print(filename)
        fn = "".join("".join(filename.split("/")[-1]).split(".")[:-1])
        np = os.path.join(TMP_LOC, f"{n}_{fn}.ump")
        print(np)
        dest = shutil.copy2(filename, np)
        print()
        n += 1

    n = 1  # 0 is the ideal submission
    for filename in os.listdir(TMP_LOC):
        # renumber files to avoid skipping deleted duplicates
        shutil.copy2(os.path.join(TMP_LOC, filename),
                     os.path.join(UMPLE_FILES_LOC, f'{n}_{"".join(filename.split("_")[1:])}'))
        n += 1

    print(f">>>>>>>>>>> n: {n}")

    # rename files to ensure none have spaces
    for filename in os.listdir(UMPLE_FILES_LOC):
        if " " in filename:
            os.rename(os.path.join(UMPLE_FILES_LOC, filename),
                      os.path.join(UMPLE_FILES_LOC, filename.replace(" ", "_")))


def clean_file(filename: str):
    """
    Clean the given Umple file.
    """
    # Replace all unidirectional associations -> or <- with bidirectional ones --
    if filename.endswith(".ump"):
        with open(filename, "r") as f:
            content = f.read()
        with open(filename, "w") as f:
            if "//$?[End_of_model]$?" in content:
                content = content.split("//$?[End_of_model]$?")[0]
            content = remove_comments(content)
            content = content.replace("<-", "--").replace("->", "--").replace("<@>", "-").replace("interface", "class")
            
            f.write(content)


def remove_comments(text: str) -> str:
    """
    Remove C-style comments (//... or /*...*/) from the given text.

    Adapted from Markus Jarderot, stackoverflow.com/questions/241327.
    """
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "
        else:
            return s
    
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


def run_process(cmd):
    """Runs the given process in a bash shell and captures its output. """
    return subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    """
    Main method used for extracting data from assignment and final exams.
    """
    shutil.rmtree(UMPLE_FILES_LOC, ignore_errors=True)
    shutil.rmtree(TMP_LOC, ignore_errors=True)

    extract_and_clean_data(DATA_LOC)
    with open("final_data/entries.json", "r") as f:
        entries = json.load(f)
    
    anonymize_filenames(entries)
    transform_ump_to_ecore()

    for i in range(1, 116):
        try:
            with open(f"{UMPLE_FILES_LOC}/{i}.ecore"): pass
        except:
            print(f"{i} not found")


if __name__ == "__main__":
    "Main entry point."
    if len(sys.argv) > 1:
        clean_file(sys.argv[1])
    else:
        print("Usage: ./clean.py input_file.ump")    
