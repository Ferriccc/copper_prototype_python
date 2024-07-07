#!/bin/python3

import os
import sys
from packages import packages
from services import services
from symlinks import symlinks
from variables import MAIN_DIRECTORY, SOURCE_DIRECTORY, TMP_DIRECTORY
from utils import addNewGeneration, help, makeSurePastExists, revert


def main(isApply: bool):
    pkg = packages(isApply)
    ser = services(isApply)
    syml = symlinks(isApply)

    syml.unlink()

    addNewGeneration(isApply)

    pkg.handleDiff()
    ser.handleDiff()
    syml.link()


def init():
    os.makedirs(SOURCE_DIRECTORY, exist_ok=True)
    os.makedirs(MAIN_DIRECTORY, exist_ok=True)
    os.makedirs(TMP_DIRECTORY, exist_ok=True)

    pkg = packages(True)
    ser = services(True)

    pkg.init()
    ser.init()


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
        if not makeSurePastExists(sys.argv[2]):
            sys.exit(1)
        revert(sys.argv[2], sys.argv[1] == "apply")
    elif not makeSurePastExists("-1"):
        sys.exit(1)

    if sys.argv[1] == "apply":
        main(True)
    elif sys.argv[1] == "dry":
        main(False)
    else:
        help()
