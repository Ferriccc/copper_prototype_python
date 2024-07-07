import subprocess
from generic import generic
from variables import DIR_MAKE, EXCLUDE, SYM_MAKE, SYM_REMOVE, CHOWN_CMD
from utils import run


class symlinks(generic):

    def __init__(self, isApply: bool) -> None:
        super().__init__('symlinks', isApply)

    def getAllFiles(self, path: str) -> list[str]:
        res = subprocess.run(f"find {path} -xtype f",
                             shell=True,
                             stdout=subprocess.PIPE,
                             text=True,
                             check=True)
        res = res.stdout.strip().split('\n')
        return res

    def isExculed(self, path: str) -> bool:
        for name in EXCLUDE:
            if name in path:
                return True
        return False

    def unlink(self) -> bool:
        path = self.mainDir
        allFiles = self.getAllFiles(path)

        for file in allFiles:
            if self.isExculed(file):
                continue

            destPath = f"/{file[len(path):]}"
            cmd = SYM_REMOVE.replace("#1", destPath)
            run(cmd, self.isApply)

        return True

    def link(self) -> bool:
        path = self.mainDir
        allFiles = self.getAllFiles(path)

        for file in allFiles:
            if self.isExculed(file):
                continue

            srcPath = file
            destPath = f"/{file[len(path):]}"

            cmd = DIR_MAKE.replace("#1", f"$(dirname {destPath})")
            run(cmd, self.isApply)

            cmd = CHOWN_CMD.replace("#1", f"$(dirname {destPath})")
            run(cmd, self.isApply)

            cmd = SYM_MAKE.replace("#1", srcPath).replace("#2", destPath)
            run(cmd, self.isApply)

        return True
