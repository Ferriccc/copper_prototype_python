# Copper

**Copper** is a declarative way for managing Linux system configuration. It allows you to define your system configuration in a simple, human-readable format and apply it consistently across your systems.

## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration File](#configuration-file)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

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
- Now you can declare system configuration using the provided files in the copper directory itself.
