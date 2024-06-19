# Copper

**Copper** is a declarative way for managing Linux system configuration. It allows you to define your system configuration in a simple, human-readable format and apply it consistently across your systems.

## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Plans](#plans)

## Features

- **Declarative Syntax**: Define your system configuration in a clear and concise way.
- **Consistency**: Ensure consistent configuration across multiple systems.
- **Ease of Use**: Simple commands to apply and manage configurations.

## Features

- [Python 3](https://www.python.org/)
- [jsondiff](https://github.com/xlwings/jsondiff): A library to compute the difference between JSON objects.

## Installation

To install Copper, follow these steps:

```bash
# Clone the repository in your HOME directory
git clone https://github.com/yourusername/copper.git "$HOME/"
```
- Add the copper directory to your path for easier access.

## Usage

- On the first run make sure to run with argument init:
```bash
copper.py init
```
- Configure commands.json with respect to your linux distribution commands (see examples section for more details).
- Configure packages.json with all the packages that you need to install.
- Now you can declare system configuration using the provided files in the copper directory itself.

## Examples
- Take a look at my configuration at my [Linux-config](https://github.com/Ferriccc/Linux-configs) for example use.
- Copper can be a used dotfile manager as it can manage symlinks to files in declarative way, you can move all the dotfiles in a specific directory which copper will symlink to their repective locations using symlinks.json, you can then go ahead and also track dotfiles using some tool like git.
- Currently installed packages on your system can also be tracked with packages.json file.
- Systemd services can be enabled / disabled by just adding / removing their names in services.json file.

## Plans
- I am planning to add support for rollbacks so that if something breaks you can rollback to previous state of the system using copper
- Any suggestions / Feature requests are more than welcomed.
