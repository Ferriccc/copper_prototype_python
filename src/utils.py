import subprocess
import os
from variables import SOURCE_DIRECTORY


def help():
    print("USAGE: setup.py [init 0 / apply {generation} / dry {generation}]")


def getLastGeneration() -> str:
    pastDir = f"{SOURCE_DIRECTORY}.tmp/"
    names = [int(name) for name in os.listdir(pastDir)]
    return str(max(names))


def run(cmd: str, isApply: bool) -> bool:
    print(f"Executing: {cmd}")
    if not isApply:
        return True
    res = subprocess.run(
        cmd,
        shell=True,
        check=False,
    )
    return res.returncode == 0


def makeSurePastExists(generation: str) -> bool:
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


def addNewGeneration(isApply: bool):
    lastGen = getLastGeneration()
    newGen = str(int(lastGen) + 1)
    newGenPath = f"{SOURCE_DIRECTORY}.tmp/{newGen}/"

    if isApply:
        os.makedirs(newGenPath, exist_ok=True)
    else:
        print(f"Executing inbuilt funtion to make dir {newGenPath}")

    for attribute in ['packages', 'services']:
        cmd = f"cp {SOURCE_DIRECTORY}{attribute}.json {newGenPath}{attribute}.json"
        run(cmd, isApply)


def showAllGens():
    commentFilePath = f'{SOURCE_DIRECTORY}.comment.txt'
    run(f"cat {commentFilePath}", True)


def addComment(comment: str):
    commentFilePath = f'{SOURCE_DIRECTORY}.comment.txt'
    lastGen = getLastGeneration()
    with open(commentFilePath, 'a') as f:
        f.write(f"{lastGen}: {comment}\n")
