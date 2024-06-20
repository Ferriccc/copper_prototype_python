#!/bin/python3

import os
import subprocess
import sys
from packages import packages
from services import services
from symlinks import symlinks
from variables import SOURCE_DIRECTORY


def help():
    print("USAGE: setup.py [init 0 / apply {generation} / dry {generation}]")


def make_sure_past_exists(generation: str) -> bool:
    pastDir = f'{SOURCE_DIRECTORY}.tmp/'
    if not os.path.exists(pastDir):
        print(
            "You forgot to run init command first time, run copper.py init to get started"
        )
        return False
    pastDir = f"{pastDir}{generation}/"
    if not os.path.exists(pastDir):
        print(
            "Provided generation does not exists, make sure to provide valid generation"
        )
        return False
    return True


def getLastGeneration() -> str:
    pastDir = f"{SOURCE_DIRECTORY}.tmp/"
    names = [int(name) for name in os.listdir(pastDir)]
    return str(max(names))


def main(isApply: bool) -> bool:
    lastGen = getLastGeneration()
    pkg = packages(SOURCE_DIRECTORY, lastGen, isApply)
    ser = services(SOURCE_DIRECTORY, lastGen, isApply)
    syml = symlinks(SOURCE_DIRECTORY, lastGen, isApply)

    if not pkg.handleDiff():
        return False
    if not ser.handleDiff():
        return False
    if not syml.handleDiff():
        return False

    return True


def addNewGeneration():
    lastGen = getLastGeneration()
    newGen = str(int(lastGen) + 1)
    newGenPath = f"{SOURCE_DIRECTORY}.tmp/{newGen}/"

    os.makedirs(newGenPath, exist_ok=True)

    for attribute in ['packages', 'services', 'symlinks']:
        subprocess.run(
            f"cp {SOURCE_DIRECTORY}{attribute}.json {newGenPath}{attribute}.json",
            shell=True,
            check=False)


def revertOldGeneration(generation: str):
    oldGenPath = f"{SOURCE_DIRECTORY}.tmp/{generation}/"
    for attribute in ['packages', 'services', 'symlinks']:
        subprocess.run(
            f"cp {oldGenPath}{attribute}.json {SOURCE_DIRECTORY}{attribute}.json",
            shell=True,
            check=False)


def init():
    pastDir = f'{SOURCE_DIRECTORY}.tmp/0/'
    os.makedirs(pastDir, exist_ok=True)

    pkg = packages(SOURCE_DIRECTORY, "0", True)
    ser = services(SOURCE_DIRECTORY, "0", True)
    syml = symlinks(SOURCE_DIRECTORY, "0", True)

    pkg.init()
    ser.init()
    syml.init()

    commentFilePath = f'{SOURCE_DIRECTORY}.comment.txt'
    with open(commentFilePath, 'w') as f:
        f.write('This file holds comments for all applied generations\n')


def addComment(comment: str):
    commentFilePath = f'{SOURCE_DIRECTORY}.comment.txt'
    lastGen = getLastGeneration()
    with open(commentFilePath, 'a') as f:
        f.write(f"{lastGen}: {comment}\n")


def showAllGens():
    commentFilePath = f'{SOURCE_DIRECTORY}.comment.txt'
    subprocess.run(f"cat {commentFilePath}", shell=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        help()
        sys.exit(1)

    if sys.argv[1] == "init":
        if (sys.argv[2] != "0"):
            help()
            sys.exit(1)
        init()
        sys.exit(0)

    if sys.argv[2] != "latest":
        if not make_sure_past_exists(sys.argv[2]):
            sys.exit(1)
        revertOldGeneration(sys.argv[2])

    if sys.argv[1] == "apply":
        comment = input(
            "Enter some comment for this generation so that you can find when changing generation: "
        )
        main(True)
        addNewGeneration()
        addComment(comment)
    elif sys.argv[1] == "dry":
        main(False)
    else:
        help()
