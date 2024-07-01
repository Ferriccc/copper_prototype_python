import json
from generic import generic
from variables import SER_ENABLE, SER_DISABLE
from utils import run

defaultEntry = {'services': ["FIRST_ENTRY_DO_NOT_TOUCH_THIS"]}


class services(generic):

    def __init__(self, isApply: bool) -> None:
        super().__init__('services', isApply)

    def init(self) -> None:
        filePath = f"{self.mainDir}services.json"
        with open(filePath, 'w') as f:
            json.dump(defaultEntry, f, indent=4)

    def enable(self, x: str):
        cmd = SER_ENABLE.replace("#1", x)
        run(cmd, self.isApply)

    def disable(self, x: str):
        cmd = SER_DISABLE.replace("#1", x)
        run(cmd, self.isApply)

    def handleDiff(self):
        inserted = self.getInsertedList()
        if (inserted != None):
            for ele in inserted:
                self.enable(ele[1])

        deleted = self.getDeletedList()
        if (deleted != None):
            for ele in deleted:
                self.disable(ele)

        return True
