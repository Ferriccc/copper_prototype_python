import subprocess
import os
from variables import SOURCE_DIRECTORY, TMP_DIRECTORY, MAIN_DIRECTORY


def help():
    print("USAGE: setup.py [init 0 / apply {generation} / dry {generation}]")


def getLastGeneration() -> str:
    pastDir = TMP_DIRECTORY
    names = [int(name) for name in os.listdir(pastDir)]
    return str(max(names)) if len(names) > 0 else "0"


def run(cmd: str, isApply: bool):
    print(f"Executing: {cmd}")
    if not isApply:
        return True
    res = subprocess.run(
        cmd,
        shell=True,
        check=False,
    )


def makeSurePastExists(generation: str) -> bool:
    pastDir = MAIN_DIRECTORY
    if not os.path.exists(pastDir):
        print(
            "You forgot to run init command first time, run copper.py init to get started"
        )
        return False
    if (generation == "-1"):
        return True
    pastDir = f"{TMP_DIRECTORY}{generation}/"
    if not os.path.exists(pastDir):
        print(
            "Provided generation does not exists, make sure to provide valid generation"
        )
        return False
    return True


def addNewGeneration(isApply: bool):
    run(f"rm -rf {MAIN_DIRECTORY}", isApply)

    gen = str(int(getLastGeneration()) + 1)
    run(f"cp -r {SOURCE_DIRECTORY} {TMP_DIRECTORY}{gen}/", isApply)
    run(f"cp -r {SOURCE_DIRECTORY} {MAIN_DIRECTORY}", isApply)


def revert(gen: str, isApply: bool):
    assert (makeSurePastExists(gen))
    run(f"rm -rf {SOURCE_DIRECTORY}", isApply)
    run(f"cp -r {TMP_DIRECTORY}{gen}/ {SOURCE_DIRECTORY}", isApply)


# def showAllGens():
#     commentFilePath = f'{SOURCE_DIRECTORY}.comment.txt'
#     run(f"cat {commentFilePath}", True)

# def addComment(comment: str):
#     commentFilePath = f'{SOURCE_DIRECTORY}.comment.txt'
#     lastGen = getLastGeneration()
#     with open(commentFilePath, 'a') as f:
#         f.write(f"{lastGen}: {comment}\n")
