# Getting setup with execution environment support on:

## macOS

### Requirements

- Docker desktop for Mac
- macOS command line developer tools
- Internet Access (during initial installation)

### Installation

- Install [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
- Open a terminal and enter `xcode-select install`, proceed with the command line developer tools installation if prompted
- Install ansible-navigator `pip3 install ansible-navigator --user`
- Add the installation path to the PATH (e.g. `echo 'export PATH=$HOME/Library/Python/3.8/bin:$PATH' >> ~/.zshrc`)
- Refresh the PATH (e.g. `source ~/.zshrc`)
- Launch ansible-navigator: `ansible-navigator`
- A one-time download of the demo execution-environment image will happen

## Windows 10

### Requirements

- Windows Subsystem for Linux 2
- Docker Desktop for Windows
- Internet Access (during initial installation)

### Installation

- Install [WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
- Install the Ubuntu Linux distribution from the Microsoft store
- Open PowerShell and run `wsl --set-default ubuntu` to set the default WSL 2 distribution
- Install [Docker Desktop for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- Launch the Ubuntu virtual machine from the Windows menu and complete the initial Ubuntu set-up
- From the Ubuntu terminal:
   - Complete the "Manage Docker as a non-root user" steps https://docs.docker.com/engine/install/linux-postinstall/
   - Update the ubuntu package index: `sudo apt update`
   - Install the python package manager: `sudo apt install python3-pip`
   - Install ansible-navigator: `pip install ansible-navigator`
   - Add the installation path to the PATH: `source ~/.profile`
   - Launch ansible-navigator: `ansible-navigator`
   - A one-time download of the demo execution-environment image will happen
