import json
from generic import generic
from variables import SOURCE_DIRECTORY

with open(f"{SOURCE_DIRECTORY}commands.json") as f:
    cmds = json.load(f)


class symlinks(generic):

    def __init__(self, sourceDir: str, generation: str, isApply: bool) -> None:
        super().__init__(sourceDir, generation, 'symlinks', isApply)

    def init(self) -> None:
        filePath = f"{self.pastDir}symlinks.json"
        with open(filePath, 'w') as f:
            json.dump(
                {
                    'symlinks': [{
                        "FIRST_ENTRY_DO_NOT_TOUCH_THIS":
                        "FIRST_ENTRY_DO_NOT_TOUCH_THIS"
                    }]
                },
                f,
                indent=4)

    def make(self, x: str, y: str) -> bool:
        cmd = cmds["symlink_make"].replace("#1", x).replace('#2', y)
        return self.run(cmd)

    def remove(self, x: str) -> bool:
        cmd = cmds["symlink_remove"].replace("#1", x)
        return self.run(cmd)

    def handleDiff(self) -> bool:
        inserted = self.getInsertedList()
        if (inserted != None):
            for ele in inserted:
                key = list(ele[1].keys())[0]
                value = ele[1][key]
                if not self.make(key, value):
                    return False

        deleted = self.getDeletedList()
        if (deleted != None):
            for ele in deleted:
                key = list(ele.keys())[0]
                value = ele[key]
                if not self.remove(value):
                    return False

        return True
