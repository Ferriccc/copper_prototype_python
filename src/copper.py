#!/bin/python3

import os
import sys
from packages import packages
from services import services
from symlinks import symlinks
from variables import SOURCE_DIRECTORY
from utils import addNewGeneration, help, makeSurePastExists, addComment


def main(isApply: bool) -> bool:
    pkg = packages(isApply)
    ser = services(isApply)
    syml = symlinks(isApply)

    if not pkg.handleDiff():
        return False
    if not ser.handleDiff():
        return False

    if not syml.unlink():
        return False

    addNewGeneration(isApply)
    if not syml.makeCopy():
        return False

    if not syml.link():
        return False

    return True


def revertOldGeneration(isApply: bool, generation: str):
    pkg = packages(isApply)
    ser = services(isApply)
    syml = symlinks(isApply)

    pkg.revert(generation)
    ser.revert(generation)
    syml.revert(generation)

    main(isApply)


def init():
    pastDir = f'{SOURCE_DIRECTORY}.tmp/0/'
    os.makedirs(pastDir, exist_ok=True)

    pkg = packages(True)
    ser = services(True)

    pkg.init()
    ser.init()

    commentFilePath = f'{SOURCE_DIRECTORY}.comment.txt'
    with open(commentFilePath, 'w') as f:
        f.write('This file holds comments for all applied generations\n')


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
        revertOldGeneration(sys.argv[1] == "apply", sys.argv[2])
    elif not makeSurePastExists("0"):
        sys.exit(1)

    if sys.argv[1] == "apply":
        comment = input(
            "Enter some comment for this generation so that you can find when changing generation: "
        )
        main(True)
        addComment(comment)
    elif sys.argv[1] == "dry":
        main(False)
    else:
        help()
