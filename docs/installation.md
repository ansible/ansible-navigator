<!-- cspell:ignore devel, kubic, libcontainers -->
# Installing ansible-navigator with execution environment support

```{contents}
:local:
```

## Linux

### Requirements

- Either [podman] or [Docker for Linux][Docker for Linux installation instructions]
- Internet access (during initial installation)

### Install the desired container engine for execution environment support

- Follow the [podman installation instructions] for the appropriate distribution.
- Follow the [Docker for Linux installation instructions] for the appropriate distribution.

### Install ansible-navigator

1. Install the python package manager using the system package installer (e.g.):

   ```
   sudo dnf install python3-pip
   ```

1. Install ansible-navigator:

   ```
   python3 -m pip install ansible-navigator --user
   ```

1. Add the installation path to the user shell initialization file (e.g.):

   ```
   echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.profile
   ```

1. Refresh the PATH (e.g.):

   ```
   source ~/.profile
   ```

1. Launch ansible-navigator:

   ```
   ansible-navigator
   ```

1. `ansible-navigator` triggers a one-time download of the demo execution-environment image.

## macOS

### Requirements

- [Docker Desktop for Mac]
- macOS command line developer tools
- Internet access (during initial installation)

### Install the desired container engine for execution environment support

- Follow the [Docker Desktop for Mac] installation instructions


```{note}
There is no convenient way to use `ansible-navigator` with [podman] on macOS.  Native source mounts from macOS through the [podman] machine into the execution environment are not currently available.

See this [related issue][macOS podman issue #8016] for details.
```

### Install ansible-navigator


1. Install the command line developer tools and proceed with the installation if prompted.

   ```
   xcode-select install
   ```

1. Install ansible-navigator:

   ```
   pip3 install ansible-navigator --user
   ```

1. Add the installation path to the PATH:

   ```
   echo 'export PATH=$HOME/Library/Python/3.8/bin:$PATH' >> ~/.zprofile
   ```

1. Refresh the PATH:

   ```
   source ~/.zprofile
   ```

1. Launch ansible-navigator:

   ```
   ansible-navigator
   ```

1. `ansible-navigator` triggers a one-time download of the demo execution-environment image.


## Windows with WSL2

### Requirements

- [Windows Subsystem for Linux 2]
- Either [podman] or [Docker Desktop for Windows]
- Internet access (during initial installation)

### Setup Windows Subsystem for Linux 2 with Ubuntu

1. Install [Windows Subsystem for Linux 2].
1. Install the [Ubuntu] 20.04 LTS Linux distribution from the Microsoft store.
1. Open PowerShell and set the default WSL 2 distribution:

   ```
   wsl --set-default ubuntu
   ```

1. Launch the Ubuntu] virtual machine from the Windows menu and complete the initial set-up.
1. From the Ubuntu terminal, create the `/dev/mqueue` directory:

   ```
   sudo mkdir /dev/mqueue
   ```

### Install the desired container engine for execution environment support


- Installation instructions for [podman] on Ubuntu 20.04 LTS.

   ```{note}
   The podman package is available in the official repositories for Ubuntu 20.10 and newer.
   Since interim releases of Ubuntu are not available on the Microsoft Store for WSL the
   [Kubic project] package can be used.
   ```

   1. Update the ubuntu package index:

      ```
      sudo apt update
      ```

   1. Install system dependencies for [podman]:

      ```
      apt-get install curl wget gnupg2
      ```

   1. Source the Ubuntu release:

      ```
      source /etc/os-release
      ```

   1. Add the podman repository:

      ```
      sudo sh -c "echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list"
      ```

   1. Download the GPG key:

      ```
      wget -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/xUbuntu_${VERSION_ID}/Release.key -O- | sudo apt-key add -
      ```

   1. Update using the new repository:

      ```
      sudo apt-get update
      ```

   1. Install podman:

      ```
      sudo apt-get install podman
      ```

- Follow the [Docker Desktop for Windows] installation instructions (if podman was not installed above)

   - Be sure to complete the [Manage Docker as a non-root user] steps.

### Install ansible-navigator

From the Ubuntu terminal:
   1. Ensure the `/dev/mqueue` directory exists:

      ```
      sudo mkdir /dev/mqueue
      ```

   1. Install the python package manager:

      ```
      sudo apt install python3-pip
      ```

   1. Install ansible-navigator:

      ```
      python3 -m pip install ansible-navigator --user
      ```

   1. Add the installation path to the user shell initialization file:

      ```
      echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.profile
      ```

   1. Refresh the PATH:

      ```
      source ~/.profile
      ```

   1. Launch ansible-navigator:

      ```
      ansible-navigator
      ```

   1. `ansible-navigator` triggers a one-time download of the demo execution-environment image.


[Docker Desktop for Mac]:
https://hub.docker.com/editions/community/docker-ce-desktop-mac
[Docker for Linux installation instructions]:
https://docs.docker.com/engine/install/
[Docker Desktop for Windows]:
https://hub.docker.com/editions/community/docker-ce-desktop-windows
[Kubic project]:
https://build.opensuse.org/package/show/devel:kubic:libcontainers:stable/podman
[Manage Docker as a non-root user]:
https://docs.docker.com/engine/install/linux-postinstall/
[macOS podman issue #8016]:
https://github.com/containers/podman/issues/8016
[podman]: https://podman.io/
[podman installation instructions]:
https://podman.io/getting-started/installation
[Ubuntu]: https://ubuntu.com
[Windows Subsystem for Linux 2]:
https://docs.microsoft.com/en-us/windows/wsl/install-win10
