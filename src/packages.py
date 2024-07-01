import json
from generic import generic
from variables import INSTALL, UNINSTALL
from utils import run

defaultEntry = {'packages': ["FIRST_ENTRY_DO_NOT_TOUCH_THIS"]}


class packages(generic):

    def __init__(self, isApply: bool) -> None:
        super().__init__("packages", isApply)

    def init(self) -> None:
        filePath = f"{self.mainDir}packages.json"
        with open(filePath, 'w') as f:
            json.dump(defaultEntry, f, indent=4)

    def install(self, x: str):
        cmd = INSTALL.replace("#1", x)
        run(cmd, self.isApply)

    def uninstall(self, x: str):
        cmd = UNINSTALL.replace("#1", x)
        run(cmd, self.isApply)

    def handleDiff(self):
        inserted = self.getInsertedList()
        if (inserted != None):
            for ele in inserted:
                self.install(ele[1])

        deleted = self.getDeletedList()
        if (deleted != None):
            for ele in deleted:
                self.uninstall(ele)
