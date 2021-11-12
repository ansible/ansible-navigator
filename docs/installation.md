# Getting setup with execution environment support on:

## macOS

### Requirements

- Docker desktop for Mac
- macOS command line developer tools
- Internet access (during initial installation)

### Installation using `podman` as the container engine

- Until native source mounts from macOS through the `podman` machine into the execution environment is available, there is not a convenient way to use `podman` on macOS with `ansible-navigator` [Related](https://github.com/containers/podman/issues/8016)

### Installation using `Docker Desktop for Mac` as the container engine

- Install [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
- Open a terminal and enter `xcode-select install`, proceed with the command line developer tools installation if prompted
- Install ansible-navigator `pip3 install ansible-navigator --user`
- Add the installation path to the PATH (e.g. `echo 'export PATH=$HOME/Library/Python/3.8/bin:$PATH' >> ~/.zshrc`)
- Refresh the PATH (e.g. `source ~/.zshrc`)
- Launch ansible-navigator: `ansible-navigator`
- A one-time download of the demo execution-environment image will happen

## Windows with WSL2

### Requirements

- Windows Subsystem for Linux 2
- Either `podman` or Docker Desktop for Windows
- Internet access (during initial installation)

### Installation using `podman` as the container engine
- Install [WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
- Install the Ubuntu Linux distribution from the Microsoft store
- Open PowerShell and run `wsl --set-default ubuntu` to set the default WSL 2 distribution
- Launch the Ubuntu virtual machine from the Windows menu and complete the initial Ubuntu set-up
- From the Ubuntu terminal:
   - Update the ubuntu package index: `sudo apt update`
   - Install system dependencies for `podman`: `apt-get install curl wget gnupg2`
   - Source the Ubuntu release: `source /etc/os-release`
   - Add the `podman` repository: `sudo sh -c "echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list"`
   - Download the GPG key: `wget -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/xUbuntu_${VERSION_ID}/Release.key -O- | sudo apt-key add -`
   - Update using the new repository: `sudo apt-get update`
   - Install `podman`: `sudo apt-get install podman`
   - Create the `/dev/mqueue` directory: `sudo mkdir /dev/mqueue`
   - Continue to the `ansible-navigator` installation instructions below

### Installation using `Docker Desktop for Windows` as the container engine

- Install [WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
- Install the Ubuntu Linux distribution from the Microsoft store
- Open PowerShell and run `wsl --set-default ubuntu` to set the default WSL 2 distribution
- Install [Docker Desktop for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- Launch the Ubuntu virtual machine from the Windows menu and complete the initial Ubuntu set-up
- From the Ubuntu terminal:
   - Complete the [Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/) steps
   - Update the ubuntu package index: `sudo apt update`
   - Install the python package manager: `sudo apt install python3-pip`
   - Install ansible-navigator: `python3 -m pip install ansible-navigator`
   - Add the installation path to the PATH: `source ~/.profile`
   - Launch ansible-navigator: `ansible-navigator`
   - A one-time download of the demo execution-environment image will happen

### Install `ansible-navigator`
- From the Ubuntu terminal"
   - Install the python package manager: `sudo apt install python3-pip`
   - Install ansible-navigator: `python3 -m pip install ansible-navigator`
   - Add the installation path to the PATH: `source ~/.profile`
   - Launch ansible-navigator: `ansible-navigator`
   - A one-time download of the demo execution-environment image will happen