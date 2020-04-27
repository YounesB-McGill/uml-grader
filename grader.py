#!/usr/bin/env python3

import glob
import os
import pathlib
import shutil
import subprocess
import zipfile

from pyunpack import Archive

# To avoid bloating this repository, make this point to your local umple executable
UMPLE_BIN = os.path.expanduser("~/umple/dev-tools/umple")

DATA_LOC = "dataset"
UMPLE_FILES_LOC = "dataset/umple_files"
TMP_LOC = "tmp/"


def transform_ump_to_ecore():
    for filename in os.listdir(UMPLE_FILES_LOC):
        cmd = f'{UMPLE_BIN} --generate Ecore {filename}'
        print(cmd)
        # proc = run_process(f'{UMPLE_BIN} --generate Ecore "{filename}"')

        # if proc.returncode != 0:
        #     print(proc.stderr)


def extract_and_clean_data(path: str):
    # Files already extracted
    # for filename in os.listdir(path):
    #     if filename.endswith(".html"):
    #         os.remove(os.path.join(path, filename))

    #     if filename.endswith((".zip", ".7z")) and not os.path.isdir(os.path.join(path, filename)):
    #         print(f"Attempting to open {filename}")
    #         Archive(os.path.join(path, filename)).extractall(os.path.join(path, "".join(filename.split(".")[:-1])))

    
    # pathlib.Path(UMPLE_FILES_LOC).mkdir(parents=True, exist_ok=True)
    # pathlib.Path(TMP_LOC).mkdir(parents=True, exist_ok=True)

    # Files already copied
    # n = 0
    # for filename in glob.iglob(DATA_LOC + "/**/*.ump", recursive=True):
    #     print(filename)
    #     fn = "".join("".join(filename.split("/")[-1]).split(".")[:-1])
    #     np = os.path.join(TMP_LOC, f"{n}_{fn}.ump")
    #     print(np)
    #     dest = shutil.copy2(filename, np)
    #     print()
    #     n += 1

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

    # Replace all unidirectional associations -> or <- with bidirectional ones --
    for filename in os.listdir(UMPLE_FILES_LOC):
        with open(os.path.join(UMPLE_FILES_LOC, filename), "r") as f:
            content = f.read()
        with open(os.path.join(UMPLE_FILES_LOC, filename), "w") as f:
            content = content.replace("<-", "--").replace("->", "--")
            f.write(content)


def run_process(cmd):
    """Runs the given process in a bash shell and captures its output. """
    return subprocess.run(
    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == "__main__":
    # shutil.rmtree(UMPLE_FILES_LOC, ignore_errors=True)
    # shutil.rmtree(TMP_LOC, ignore_errors=True)

    # extract_and_clean_data(DATA_LOC)
    transform_ump_to_ecore()
