<!-- cspell:ignore devel, kubic, libcontainers -->

# Installing ansible-navigator with execution environment support

[TOC]

## Linux

### Requirements

- Either [podman] or [Docker for
  Linux][docker for linux installation instructions]
- Internet access (during initial installation)

### Install the desired container engine for execution environment support

- Follow the [podman installation instructions] for the appropriate
  distribution.
- Follow the [Docker for Linux installation instructions] for the appropriate
  distribution.

### Install ansible-navigator

1.  Install the python package manager using the system package installer
    (e.g.):

    ```bash
    sudo dnf install python3-pip
    ```

2.  Install ansible-navigator:

    ```bash
    python3 -m pip install ansible-navigator --user
    ```

3.  Add the installation path to the user shell initialization file (e.g.):

    ```bash
    echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.profile
    ```

4.  Refresh the PATH (e.g.):

    ```bash
    source ~/.profile
    ```

5.  Launch ansible-navigator:

    ```bash
    ansible-navigator
    ```

6.  `ansible-navigator` triggers a one-time download of the demo
    execution-environment image.

## macOS

### Requirements (macos)

- [Docker Desktop for Mac]
- macOS command line developer tools
- Internet access (during initial installation)

### Install the desired container engine for execution environment support (macos)

- Follow the [Docker Desktop for Mac] installation instructions

!!! notice

    There is no convenient way to use `ansible-navigator` with [podman] on
    macOS.  Native source mounts from macOS through the [podman] machine into
    the execution environment are not currently available.

    See this [related issue][macOS podman issue #8016] for details.

### Install ansible-navigator (macos)

1.  Install the command line developer tools and proceed with the installation
    if prompted.

    ```bash
    xcode-select --install
    ```

2.  Install ansible-navigator:

    ```bash
    pip3 install ansible-navigator --user
    ```

3.  Add the installation path to the PATH, using the installed Python version:

    ```bash
    echo 'export PATH=$HOME/Library/Python/3.9/bin:$PATH' >> ~/.zprofile
    ```

4.  Refresh the PATH:

    ```bash
    source ~/.zprofile
    ```

5.  Launch ansible-navigator:

    ```bash
    ansible-navigator
    ```

6.  `ansible-navigator` triggers a one-time download of the demo
    execution-environment image.

## Windows with WSL2

### Requirements (windows)

- [Windows Subsystem for Linux 2]
- Either [podman] or [Docker Desktop for Windows]
- Internet access (during initial installation)

### Setup Windows Subsystem for Linux 2 with Ubuntu

1.  Install [Windows Subsystem for Linux 2].
1.  Install the [Ubuntu] 20.04 LTS Linux distribution from the Microsoft store.
1.  Open PowerShell and set the default WSL 2 distribution:

    ```bash
    wsl --set-default ubuntu
    ```

1.  Launch the Ubuntu] virtual machine from the Windows menu and complete the
    initial set-up.
1.  From the Ubuntu terminal, create the `/dev/mqueue` directory:

    ```bash
    sudo mkdir /dev/mqueue
    ```

### Install the desired container engine for execution environment support (windows)

- Installation instructions for [podman] on Ubuntu 20.04 LTS.

  !!! notice

      The podman package is available in the official repositories for Ubuntu 20.10 and newer.
      Since interim releases of Ubuntu are not available on the Microsoft Store for WSL the
      [Kubic project] package can be used.

  1.  Update the ubuntu package index:

      ```bash
      sudo apt update
      ```

  1.  Install system dependencies for [podman]:

      ```bash
      apt-get install curl wget gnupg2
      ```

  1.  Source the Ubuntu release:

      ```bash
      source /etc/os-release
      ```

  1.  Add the podman repository:

      ```bash
      sudo sh -c "echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list"
      ```

  1.  Download the GPG key:

      ```bash
      wget -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/xUbuntu_${VERSION_ID}/Release.key -O- | sudo apt-key add -
      ```

  1.  Update using the new repository:

      ```bash
      sudo apt-get update
      ```

  1.  Install podman:

      ```bash
      sudo apt-get install podman
      ```

- Follow the [Docker Desktop for Windows] installation instructions (if podman
  was not installed above)

  - Be sure to complete the [Manage Docker as a non-root user] steps.

### Install ansible-navigator (windows)

From the Ubuntu terminal:

1.  Ensure the `/dev/mqueue` directory exists:

    ```bash
    sudo mkdir /dev/mqueue
    ```

1.  Install the python package manager:

    ```bash
    sudo apt install python3-pip
    ```

1.  Install ansible-navigator:

    ```bash
    python3 -m pip install ansible-navigator --user
    ```

1.  Add the installation path to the user shell initialization file:

    ```bash
    echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.profile
    ```

1.  Refresh the PATH:

    ```bash
    source ~/.profile
    ```

1.  Launch ansible-navigator:

    ```bash
    ansible-navigator
    ```

1.  `ansible-navigator` triggers a one-time download of the demo
    execution-environment image.

[docker desktop for mac]:
  https://hub.docker.com/editions/community/docker-ce-desktop-mac
[docker for linux installation instructions]:
  https://docs.docker.com/engine/install/
[docker desktop for windows]:
  https://hub.docker.com/editions/community/docker-ce-desktop-windows
[manage docker as a non-root user]:
  https://docs.docker.com/engine/install/linux-postinstall/
[podman]: https://podman.io/
[podman installation instructions]:
  https://podman.io/getting-started/installation
[ubuntu]: https://ubuntu.com
[windows subsystem for linux 2]:
  https://docs.microsoft.com/en-us/windows/wsl/install-win10
