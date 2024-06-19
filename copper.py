#!/bin/python3

import json
import os
import sys
import subprocess
from jsondiff import delete, diff, insert

SCR_PATH = os.path.dirname(os.path.abspath(__file__))
CMDS = f'{SCR_PATH}/commands.json'

apply = 0  # this switches between dry_run / actual_apply mode
safe_mode = True  # this makes sure no command fails before applying new config

with open(CMDS) as f:
    cmds = json.load(f)


class generic:
    CURRENT = ""
    PAST = ""
    FILE = ""

    def __init__(self, current, past):
        self.CURRENT = current
        self.PAST = past
        pass

    def get_diffs(self):
        current = self.CURRENT + self.FILE + ".json"
        past = self.PAST + self.FILE + ".json"
        with open(current) as f:
            current = json.load(f)
        with open(past) as f:
            past = json.load(f)
        return [
            diff(past, current, syntax='explicit', marshal=True), current, past
        ]

    def get_inserted_list(self):
        df = self.get_diffs()[0]
        if df == None:
            return None
        try:
            inserted = df['$update'][self.FILE]['$insert']  # type: ignore
            return inserted
        except:
            return None

    def get_deleted_list(self):
        diffs = self.get_diffs()
        df = diffs[0]
        past = diffs[2]
        if df == None:
            return None
        try:
            deleted_indx = df['$update'][self.FILE]['$delete']  # type: ignore
            if (deleted_indx == None):
                return None
            deleted = []
            for indx in deleted_indx:
                deleted.append(past[self.FILE][indx])
            return deleted
        except:
            return None

    def handle_diff(self):
        raise NotImplementedError("Subclass must implement this method")


class packages(generic):

    def __init__(self, current, past):
        super().__init__(current, past)
        self.FILE = "packages"

    def install(self, x):
        cmd = cmds["install"].replace("#1", x)
        run(cmd)

    def uninstall(self, x):
        cmd = cmds["uninstall"].replace("#1", x)
        run(cmd)

    def clean(self):
        cmd = cmds["clean"]
        run(cmd, False)

    def handle_diff(self):
        inserted = self.get_inserted_list()
        if (inserted != None):
            for ele in inserted:
                self.install(ele[1])
        deleted = self.get_deleted_list()
        if (deleted != None):
            for ele in deleted:
                self.uninstall(ele)
        self.clean()


class systemd_services(generic):

    def __init__(self, current, past):
        super().__init__(current, past)
        self.FILE = "services"

    def enable(self, x):
        cmd = cmds["systemd_enable"].replace("#1", x)
        run(cmd)

    def disable(self, x):
        cmd = cmds["systemd_disable"].replace("#1", x)
        run(cmd)

    def handle_diff(self):
        inserted = self.get_inserted_list()
        if (inserted != None):
            for ele in inserted:
                self.enable(ele[1])
        deleted = self.get_deleted_list()
        if (deleted != None):
            for ele in deleted:
                self.disable(ele)


class symlinks(generic):

    def __init__(self, current, past):
        super().__init__(current, past)
        self.FILE = "symlinks"

    def make(self, x, y):
        cmd = cmds["symlink_make"].replace("#1", x).replace('#2', y)
        run(cmd)

    def remove(self, x):
        cmd = cmds["symlink_remove"].replace("#1", x)
        run(cmd)

    def handle_diff(self):
        inserted = self.get_inserted_list()
        if (inserted != None):
            for ele in inserted:
                key = list(ele[1].keys())[0]
                value = ele[1][key]
                self.make(key, value)
        deleted = self.get_deleted_list()
        if (deleted != None):
            for ele in deleted:
                key = list(ele.keys())[0]
                value = ele[key]
                self.remove(value)


def help():
    print("USAGE: setup.py [init / apply / dry]")
    sys.exit(1)


def make_sure_past_exists():
    PAST = f'{SCR_PATH}/.tmp/'
    if not os.path.exists(PAST):
        print(
            "You forgot to run init command first time, run copper.py init to get started"
        )
        sys.exit(1)


def main(CURRENT, PAST):
    pack = packages(CURRENT, PAST)
    serv = systemd_services(CURRENT, PAST)
    sym = symlinks(CURRENT, PAST)

    pack.handle_diff()
    sym.handle_diff()
    serv.handle_diff()

    if apply and safe_mode:
        run(f"cp {CURRENT}packages.json {PAST}packages.json")
        run(f"cp {CURRENT}services.json {PAST}services.json")
        run(f"cp {CURRENT}symlinks.json {PAST}symlinks.json")


def revert():
    global safe_mode
    global apply
    safe_mode = False

    CURRENT = f'{SCR_PATH}/'
    PAST = f'{SCR_PATH}/.tmp/'
    main(PAST, CURRENT)
    exit(1)


def run(cmd, check_flag=True):
    if apply:
        try:
            subprocess.run(cmd, shell=True, check=(safe_mode and check_flag))
        except:
            assert (safe_mode == True)
            print(
                f"Command failed: {cmd}, reverting to previous working config..."
            )
            revert()
    else:
        print(cmd)


def init():
    PAST = f'{SCR_PATH}/.tmp/'
    os.makedirs(PAST, exist_ok=True)

    file_path = f"{PAST}packages.json"
    with open(file_path, 'w') as f:
        json.dump({'packages': ["FIRST_ENTRY_DO_NOT_TOUCH_THIS"]}, f, indent=4)

    file_path = f"{PAST}services.json"
    with open(file_path, 'w') as f:
        json.dump({'services': ["FIRST_ENTRY_DO_NOT_TOUCH_THIS"]}, f, indent=4)

    file_path = f"{PAST}symlinks.json"
    with open(file_path, 'w') as f:
        json.dump(
            {
                'symlinks': [{
                    "FIRST_ENTRY_DO_NOT_TOUCH_THIS":
                    "FIRST_ENTRY_DO_NOT_TOUCH_THIS"
                }]
            },
            f,
            indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        help()

    if sys.argv[1] == "init":
        init()
        sys.exit(0)
    if sys.argv[1] == "apply":
        make_sure_past_exists()
        apply = 1
    elif sys.argv[1] == "dry":
        make_sure_past_exists()
        apply = 0
    else:
        help()

    CURRENT = f'{SCR_PATH}/'
    PAST = f'{SCR_PATH}/.tmp/'
    main(CURRENT, PAST)
