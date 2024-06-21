import subprocess
from generic import generic
from variables import EXCLUDE, SYM_MAKE, SYM_REMOVE
from utils import getLastGeneration, run


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
        lastGen = getLastGeneration()
        path = f"{self.currentDir}.tmp/{lastGen}/"
        prefix = f"{self.currentDir}.tmp/{lastGen}"
        allFiles = self.getAllFiles(path)

        for file in allFiles:
            if self.isExculed(file):
                continue

            srcPath = file
            assert (srcPath.startswith(prefix))
            destPath = srcPath[len(prefix):]
            cmd = SYM_REMOVE.replace("#1", destPath)

            if not run(cmd, self.isApply):
                return False

        return True

    def link(self) -> bool:
        lastGen = getLastGeneration()
        path = f"{self.currentDir}.tmp/{lastGen}/"
        prefix = f"{self.currentDir}.tmp/{lastGen}"
        allFiles = self.getAllFiles(path)

        for file in allFiles:
            if self.isExculed(file):
                continue

            srcPath = file
            assert (srcPath.startswith(prefix))
            destPath = srcPath[len(prefix):]
            cmd = SYM_MAKE.replace("#1", srcPath).replace("#2", destPath)

            if not run(cmd, self.isApply):
                return False

        return True

    def makeCopy(self) -> bool:
        newGen = getLastGeneration()
        path = f"{self.currentDir}"
        newPrefix = f"{self.currentDir}.tmp/{newGen}/"
        allFiles = self.getAllFiles(path)

        for file in allFiles:
            if self.isExculed(file) or ".tmp" in file:
                continue

            srcPath = file
            assert (srcPath.startswith(path))
            destPath = newPrefix + srcPath[len(path):]
            cmd = f"mkdir -p \"$(dirname {destPath})\""
            if not run(cmd, self.isApply):
                return False
            cmd = f"cp {srcPath} {destPath}"
            if not run(cmd, self.isApply):
                return False

        return True

    def revert(self, gen: str) -> bool:
        path = f"{self.currentDir}.tmp/{gen}/"
        newPrefix = f"{self.currentDir}"

        oldFiles = self.getAllFiles(newPrefix)
        for file in oldFiles:
            if self.isExculed(file) or ".tmp" in file:
                continue
            cmd = SYM_REMOVE.replace("#1", file)
            run(cmd, self.isApply)

        allFiles = self.getAllFiles(path)

        for file in allFiles:
            if self.isExculed(file):
                continue

            srcPath = file
            assert (srcPath.startswith(path))
            destPath = newPrefix + srcPath[len(path):]
            cmd = f"mkdir -p \"$(dirname {destPath})\""
            if not run(cmd, self.isApply):
                return False
            cmd = f"cp {srcPath} {destPath}"
            if not run(cmd, self.isApply):
                return False

        return True
