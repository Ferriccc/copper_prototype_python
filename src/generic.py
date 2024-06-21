import json
from jsondiff import diff
from variables import SOURCE_DIRECTORY
from utils import getLastGeneration, run


class generic:
    currentDir: str
    pastDir: str
    attribute: str
    isApply: bool

    def __init__(self, attribute: str, isApply: bool) -> None:
        self.currentDir = SOURCE_DIRECTORY
        self.pastDir = f"{SOURCE_DIRECTORY}.tmp/{getLastGeneration()}/"
        self.attribute = attribute
        self.isApply = isApply

    def getDiffs(self):
        current = self.currentDir + self.attribute + ".json"
        past = self.pastDir + self.attribute + ".json"
        with open(current) as f:
            current = json.load(f)
        with open(past) as f:
            past = json.load(f)
        return [
            diff(past, current, syntax='explicit', marshal=True), current, past
        ]

    def getInsertedList(self):
        df = self.getDiffs()[0]
        if df == None:
            return None
        try:
            inserted = df['$update'][self.attribute]['$insert']  # type: ignore
            return inserted
        except:
            return None

    def getDeletedList(self):
        diffs = self.getDiffs()
        df = diffs[0]
        past = diffs[2]
        if df == None:
            return None
        try:
            deleted_indx = df['$update'][self.attribute][
                '$delete']  # type: ignore
            if (deleted_indx == None):
                return None
            deleted = []
            for indx in deleted_indx:
                deleted.append(past[self.attribute][indx])
            return deleted
        except:
            return None

    def revert(self, gen: str) -> bool:
        oldGenPath = f"{self.currentDir}.tmp/{gen}/"
        cmd = f"cp {oldGenPath}{self.attribute}.json {self.currentDir}{self.attribute}.json"
        return run(cmd, self.isApply)

    def handleDiff(self):
        raise NotImplementedError("Subclass must implement this method")
