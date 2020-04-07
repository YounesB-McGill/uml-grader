#!/usr/bin/env python3

import glob
import os
import pathlib
import shutil
import subprocess
import zipfile

# To avoid bloating this repository, make this point to your local umple executable
UMPLE_BIN = os.path.expanduser("~/umple/dev-tools/umple")

DATA_LOC = "dataset"
UMPLE_FILES_LOC = "dataset/umple_files"


def transform_ump_to_ecore():
    print(os.getcwd())
    for filename in os.listdir(UMPLE_FILES_LOC):
        cmd = f'{UMPLE_BIN} --generate Ecore {os.path.join(UMPLE_FILES_LOC, filename)}'
        print(cmd)
        # proc = run_process(f'{UMPLE_BIN} --generate Ecore "{filename}"')

        # if proc.returncode != 0:
        #     print(proc.stderr)


def extract_and_clean_data(path: str):
    for filename in os.listdir(path):
        if filename.endswith(".html"):
            os.remove(os.path.join(path, filename))

        # TODO Handle rar and 7z archives
        if filename.endswith(".zip"):
            print(f"Attempting to open {filename}")
            with zipfile.ZipFile(os.path.join(path, filename), 'r') as z:
                print(os.path.join(path, filename[:-4]))
                z.extractall(os.path.join(path, filename[:-4]))

    pathlib.Path(UMPLE_FILES_LOC).mkdir(parents=True, exist_ok=True)

    c = 0
    for filename in glob.iglob(DATA_LOC + "/**/*.ump", recursive=True):
        try:
            shutil.copy2(filename, UMPLE_FILES_LOC)
        except shutil.SameFileError:
            fn = filename.split(".")
            shutil.copy2(filename, f"{fn[0]}{c}.ump")
            c += 1


def run_process(cmd):
    """Runs the given process in a bash shell and captures its output. """
    return subprocess.run(
    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == "__main__":
    transform_ump_to_ecore()
