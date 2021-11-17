# Installing ansible-navigator with execution environment support

[podman_url]: https://podman.io/

```{contents}
:local:
```

## Linux

[podman_install_url]: https://podman.io/getting-started/installation
[docker_for_linux_url]: https://docs.docker.com/engine/install/

### Requirements

- Either [podman][podman_url] or [Docker for Linux][docker_for_linux_url]
- Internet access (during initial installation)

### Install the desired container engine for execution environment support

- Follow the [podman installation instructions][podman_install_url] for the appropriate distribution.
- Follow the [Docker for Linux installation instructions][docker_for_linux_url] for the appropriate distribution.

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

[docker_for_mac_url]: https://hub.docker.com/editions/community/docker-ce-desktop-mac
[mac_podman_issue_url]: https://github.com/containers/podman/issues/8016

### Requirements

- [Docker desktop for Mac][docker_for_mac_url]
- macOS command line developer tools
- Internet access (during initial installation)

### Install the desired container engine for execution environment support

- Follow the [Docker Desktop for Mac][docker_for_mac_url] installation instructions


```{note}
There is no convenient way to use `ansible-navigator` with [podman][podman_url] on macOS.  Native source mounts from macOS through the [podman][podman_url] machine into the execution environment are not currently available.

See this [related issue][mac_podman_issue_url] for details.
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

[docker_desktop_for_windows_url]: https://hub.docker.com/editions/community/docker-ce-desktop-windows
[manage_docker_non_root_user_url]: https://docs.docker.com/engine/install/linux-postinstall/
[kubic_project_url]: https://build.opensuse.org/package/show/devel:kubic:libcontainers:stable/podman
[ubuntu_url]: https://ubuntu.com/
[wsl_2_install_url]: https://docs.microsoft.com/en-us/windows/wsl/install-win10

### Requirements

- [Windows Subsystem for Linux 2][wsl_2_install_url]
- Either [podman][podman_url] or [Docker Desktop for Windows][docker_desktop_for_windows_url]
- Internet access (during initial installation)

### Setup Windows Subsystem for Linux 2 with Ubuntu

1. Install [Windows Subsystem for Linux 2][wsl_2_install_url].
1. Install the [Ubuntu][ubuntu_url] 20.04 LTS Linux distribution from the Microsoft store.
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


- Installation instructions for [podman][podman_url] on Ubuntu 20.04 LTS.

   ```{note}
   The podman package is available in the official repositories for Ubuntu 20.10 and newer.
   Since interim releases of Ubuntu are not available on the Microsoft Store for WSL the
   [Kubic project][kubic_project_url] package can be used.
   ```

   1. Update the ubuntu package index:

      ```
      sudo apt update
      ```

   1. Install system dependencies for podman]:

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

- Follow the [Docker Desktop for Windows][docker_desktop_for_windows_url] installation instructions (if podman was not installed above)

   - Be sure to complete the [Manage Docker as a non-root user][manage_docker_non_root_user_url] steps.

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
