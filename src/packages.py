import json
from generic import generic
from variables import SOURCE_DIRECTORY

with open(f"{SOURCE_DIRECTORY}commands.json") as f:
    cmds = json.load(f)


class packages(generic):

    def __init__(self, sourceDir: str, generation: str, isApply: bool) -> None:
        super().__init__(sourceDir, generation, "packages", isApply)

    def init(self) -> None:
        filePath = f"{self.pastDir}packages.json"
        with open(filePath, 'w') as f:
            json.dump({'packages': ["FIRST_ENTRY_DO_NOT_TOUCH_THIS"]},
                      f,
                      indent=4)

    def install(self, x: str) -> bool:
        cmd = cmds["install"].replace("#1", x)
        return self.run(cmd)

    def uninstall(self, x: str) -> bool:
        cmd = cmds["uninstall"].replace("#1", x)
        return self.run(cmd)

    def clean(self) -> bool:
        cmd = cmds["clean"]
        return self.run(cmd)

    def handleDiff(self) -> bool:
        inserted = self.getInsertedList()
        if (inserted != None):
            for ele in inserted:
                if not self.install(ele[1]):
                    return False

        deleted = self.getDeletedList()
        if (deleted != None):
            for ele in deleted:
                if not self.uninstall(ele):
                    return False

        return True
