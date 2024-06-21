# Copper

**Copper** is a declarative way for managing Linux system configuration. It allows you to define your system configuration in a simple, human-readable format and apply it consistently across your systems.

## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Updates](#updates)

## Features

- **Declarative Syntax**: Define your system configuration in a clear and concise way.
- **Consistency**: Ensure consistent configuration across multiple systems.
- **Ease of Use**: Simple commands to apply and manage configurations.
- **Safe**: You can revert to previous configuration in case something breaks in current configuration

## Dependencies

- [Python 3](https://www.python.org/)
- [jsondiff](https://github.com/xlwings/jsondiff): A library to compute the difference between JSON objects.

## Installation

To install Copper, follow these steps:

```bash
# Clone the repository in your HOME directory
git clone https://github.com/yourusername/copper.git "$HOME/"
```
- Add the copper/src directory to your path for easier access.

## Usage
- You need to make a source directory which then should be updated in variables.py file as variable source directory.
- Copper will treat the files located in source directory as if they are under / in real filesystem
- Source directory also holds your (packages / services).json files which you can edit to modify installed packages / enabled services.
- For tracking any file it should be place inside the source directory in same structured path as it is under / (root) in real filesystem, after that copper takes care of linking and tracking it automatically.

- Options
  - init (makes required directories for functioning)
  - dry {generation} (lists out all execution without actually executing it)
  - apply {generation} (actually apply the configuration) 
- On the first run make sure to run with argument init 0:
```bash
copper.py init 0
```
- For applying latest configuration:
```bash
copper.py apply latest
```
- For reverting to any previous configuration:
```bash
copper.py apply {generation number}
```
- All the generation are stored internally in provided sourceDirectory/.tmp/{generation}. Never touch this directory
- Configure src/variables.py with respect to your linux distribution commands.
- Now you are ready to declare your system configuration.

## Examples
- Take a look at my configuration at my [Linux-config](https://github.com/Ferriccc/my-linux-config) for example use.
- Copper can be used (but not limited as) a dotfile manager as it can manage symlinks to files in declarative way.
- Currently installed packages on your system can also be tracked with packages.json file.
- Systemd services can be enabled / disabled by just adding / removing their names in services.json file.

## Updates
- ~I am planning to add support for rollbacks so that if something breaks you can rollback to previous state of the system using copper~ (UPD: added!)
- Any suggestions / Feature requests are more than welcomed.
