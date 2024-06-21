import json
from generic import generic
from variables import SER_ENABLE, SER_DISABLE
from utils import run

defaultEntry = {'services': ["FIRST_ENTRY_DO_NOT_TOUCH_THIS"]}


class services(generic):

    def __init__(self, isApply: bool) -> None:
        super().__init__('services', isApply)

    def init(self) -> None:
        filePath = f"{self.pastDir}services.json"
        with open(filePath, 'w') as f:
            json.dump(defaultEntry, f, indent=4)
        filePath = f"{self.currentDir}services.json"
        with open(filePath, 'w') as f:
            json.dump(defaultEntry, f, indent=4)

    def enable(self, x: str) -> bool:
        cmd = SER_ENABLE.replace("#1", x)
        return run(cmd, self.isApply)

    def disable(self, x: str) -> bool:
        cmd = SER_DISABLE.replace("#1", x)
        return run(cmd, self.isApply)

    def handleDiff(self) -> bool:
        inserted = self.getInsertedList()
        if (inserted != None):
            for ele in inserted:
                if not self.enable(ele[1]):
                    return False

        deleted = self.getDeletedList()
        if (deleted != None):
            for ele in deleted:
                if not self.disable(ele):
                    return False

        return True
