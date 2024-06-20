import json
from generic import generic
from variables import SOURCE_DIRECTORY

with open(f"{SOURCE_DIRECTORY}commands.json") as f:
    cmds = json.load(f)


class services(generic):

    def __init__(self, sourceDir: str, generation: str, isApply: bool) -> None:
        super().__init__(sourceDir, generation, 'services', isApply)

    def init(self) -> None:
        filePath = f"{self.pastDir}services.json"
        with open(filePath, 'w') as f:
            json.dump({'services': ["FIRST_ENTRY_DO_NOT_TOUCH_THIS"]},
                      f,
                      indent=4)

    def enable(self, x: str) -> bool:
        cmd = cmds["systemd_enable"].replace("#1", x)
        return self.run(cmd)

    def disable(self, x: str) -> bool:
        cmd = cmds["systemd_disable"].replace("#1", x)
        return self.run(cmd)

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
