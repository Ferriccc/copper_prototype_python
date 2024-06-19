#!/bin/python3

import json
import os
import sys
import subprocess
from jsondiff import diff

HOME = os.path.expanduser('~')
CMDS = f'{HOME}/copper/commands.json'
CURRENT = f'{HOME}/copper/'
PAST = f'{HOME}/copper/.tmp/'
apply = 0

with open(CMDS) as f:
    cmds = json.load(f)


def run(cmd, chk=True):
    if apply:
        subprocess.run(cmd, shell=True, check=chk)
    else:
        print(cmd)


def init():
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

    file_path = f"{PAST}routines.json"
    with open(file_path, 'w') as f:
        json.dump({'routines': ["FIRST_ENTRY_DO_NOT_TOUCH_THIS"]}, f, indent=4)


class packages:

    def __init__(self):
        pass

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
        current = CURRENT + 'packages.json'
        past = PAST + 'packages.json'

        with open(current) as f:
            current = json.load(f)
        with open(past) as f:
            past = json.load(f)

        df = diff(past, current, syntax='explicit', marshal=True)
        if df == None:
            return

        try:
            inserted = df['$update']['packages']['$insert']  # type: ignore
            if (inserted != None):
                for ele in inserted:
                    self.install(ele[1])
        except:
            pass
        try:
            deleted = df['$update']['packages']['$delete']  # type: ignore
            if (deleted != None):
                for indx in deleted:
                    self.uninstall(past['packages'][indx])
        except:
            pass

        self.clean()


class systemd_services:

    def __init__(self):
        pass

    def enable(self, x):
        cmd = cmds["systemd_enable"].replace("#1", x)
        run(cmd)

    def disable(self, x):
        cmd = cmds["systemd_disable"].replace("#1", x)
        run(cmd)

    def handle_diff(self):
        current = CURRENT + 'services.json'
        past = PAST + 'services.json'

        with open(current) as f:
            current = json.load(f)
        with open(past) as f:
            past = json.load(f)

        df = diff(past, current, syntax='explicit', marshal=True)
        if df == None:
            return

        try:
            inserted = df['$update']['services']['$insert']  # type: ignore
            if (inserted != None):
                for ele in inserted:
                    self.enable(ele[1])
        except:
            pass
        try:
            deleted = df['$update']['services']['$delete']  # type: ignore
            if (deleted != None):
                for indx in deleted:
                    self.disable(past['services'][indx])
        except:
            pass


class symlinks:

    def __init__(self):
        pass

    def make(self, x, y):
        cmd = cmds["symlink_make"].replace("#1", x).replace('#2', y)
        run(cmd)

    def remove(self, x):
        cmd = cmds["symlink_remove"].replace("#1", x)
        run(cmd)

    def handle_diff(self):
        current = CURRENT + 'symlinks.json'
        past = PAST + 'symlinks.json'

        with open(current) as f:
            current = json.load(f)
        with open(past) as f:
            past = json.load(f)

        df = diff(past, current, syntax='explicit', marshal=True)
        if df == None:
            return

        try:
            inserted = df['$update']['symlinks']['$insert']  # type: ignore
            if (inserted != None):
                for ele in inserted:
                    key = list(ele[1].keys())[0]
                    value = ele[1][key]
                    self.make(key, value)
        except:
            pass
        try:
            deleted = df['$update']['symlinks']['$delete']  # type: ignore
            if (deleted != None):
                for indx in deleted:
                    key = list(past['symlinks'][indx].keys())[0]
                    value = past['symlinks'][indx][key]
                    self.remove(value)
        except:
            pass


class routines:

    def __init__(self):
        pass

    def handle_diff(self):
        current = CURRENT + 'routines.json'
        past = PAST + 'routines.json'

        with open(current) as f:
            current = json.load(f)
        with open(past) as f:
            past = json.load(f)

        df = diff(past, current, syntax='explicit', marshal=True)
        if df == None:
            return

        try:
            inserted = df['$update']['routines']['$insert']  # type: ignore
            if (inserted != None):
                for ele in inserted:
                    run(ele[1], False)
        except:
            pass


def help():
    print("USAGE: setup.py [init / apply / dry]")
    sys.exit(1)


if len(sys.argv) < 2:
    help()

if sys.argv[1] != "init":
    if not (os.path.exists(PAST) and os.path.isdir(PAST)):
        print(
            "You forgot to run init command first time, make sure to run init command on first run!"
        )
        sys.exit(1)
elif sys.argv[1] == "init":
    init()
    sys.exit(0)

if sys.argv[1] == "apply":
    apply = 1
elif sys.argv[1] == "dry":
    apply = 0
else:
    help()

pack = packages()
serv = systemd_services()
sym = symlinks()
rou = routines()

pack.handle_diff()
sym.handle_diff()
serv.handle_diff()
rou.handle_diff()

if apply:
    run(f"cp {CURRENT}packages.json {PAST}packages.json")
    run(f"cp {CURRENT}services.json {PAST}services.json")
    run(f"cp {CURRENT}symlinks.json {PAST}symlinks.json")
    run(f"cp {CURRENT}routines.json {PAST}routines.json")
