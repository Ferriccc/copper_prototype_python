# warn: only change the home directory path
# all your config changes should be in SOURCE_DIRECTORY
# SOURCE_DIRECTORY should be a direct sub directory of some path, which already exists in your system
# below are some recommended paths
SOURCE_DIRECTORY = "/home/shrey/configs/"
MAIN_DIRECTORY = "/home/shrey/.copper/"
INTERMEDIATE_DIRECTORY = "/home/shrey/.copperInter/"
TMP_DIRECTORY = "/home/shrey/.copperTmp/"

# append the names of files / directories that you want to be excluded in linking to real filesystem
EXCLUDE = [
    'packages.json', 'services.json', 'README.md', '.git', '.comment.txt',
    'denv'
]

# install & uninstall commands for your package manager #N will act as a placeholder
# e.g. sudo apt install #1, here #1 will be replaced by the first argument passed (some package name)
INSTALL = "paru -S --noconfirm --needed #1"
UNINSTALL = "paru -R --noconfirm #1"

# commands to enable / disable systemd services (mostly you don't need to change this)
SER_ENABLE = "sudo systemctl enable --now #1"
SER_DISABLE = "sudo systemctl disable --now #1"

# commands to make / remove symlinks (mostly you don't need to change this)
SYM_MAKE = "sudo cp -asrf #1 #2"
SYM_REMOVE = "sudo rm -rf #1"
