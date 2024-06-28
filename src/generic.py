import json
from jsondiff import diff
from variables import MAIN_DIRECTORY, SOURCE_DIRECTORY, TMP_DIRECTORY
from utils import getLastGeneration, run


class generic:
    currentDir: str
    mainDir: str
    attribute: str
    isApply: bool

    def __init__(self, attribute: str, isApply: bool) -> None:
        self.currentDir = SOURCE_DIRECTORY
        self.mainDir = MAIN_DIRECTORY
        self.tmpDir = TMP_DIRECTORY
        self.attribute = attribute
        self.isApply = isApply

    def getDiffs(self):
        current = self.currentDir + self.attribute + ".json"
        past = self.mainDir + self.attribute + ".json"
        with open(current) as f:
            current = json.load(f)
        with open(past) as f:
            past = json.load(f)
        return [
            diff(past, current, syntax='explicit', marshal=True), current, past
        ]

    def getInsertedList(self):
        current = self.currentDir + self.attribute + ".json"
        with open(current) as f:
            current = json.load(f)
        return list(current[self.attribute])
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

    def handleDiff(self):
        raise NotImplementedError("Subclass must implement this method")
