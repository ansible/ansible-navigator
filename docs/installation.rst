.. _installing_ansible_navigator:

Installing ansible-navigator with execution environment support
###############################################################

.. contents::
   :local:

Linux
*****

Requirements
============

* Either ``podman`` or ``Docker for Linux``
* Internet access (during initial installation)

Install the desired container engine for execution environment support
======================================================================

* Follow the ``podman`` installation instructions for the appropriate `Linux distribution <https://podman.io/getting-started/installation>`__.
* Follow the ``Docker for Linux`` installation instructions for the appropriate `Linux distribution <https://docs.docker.com/engine/install/>`__.

Install ansible-navigator
=============================

#. Install the python package manager using the system package installer (e.g.):

   .. code-block:: console

    sudo dnf install python3-pip

#. Install ansible-navigator:

   .. code-block:: console

    python3 -m pip install ansible-navigator --user

#. Add the installation path to the PATH (e.g.):

   .. code-block:: console

    echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.zshrc

#. Open a new terminal or refresh the PATH (e.g.):

   .. code-block:: console

    source ~/.zshrc

#. Launch ansible-navigator:

   .. code-block:: console

    ansible-navigator

#. ``ansible-navigator`` triggers a one-time download of the demo execution-environment image.

macOS
*****

Requirements
============

* Docker desktop for Mac
* macOS command line developer tools
* Internet access (during initial installation)

Install the desired container engine for execution environment support
======================================================================

* Follow the `Docker Desktop for Mac <https://hub.docker.com/editions/community/docker-ce-desktop-mac>`__ installation instructions

.. note::

   There is no convenient way to use ``ansible-navigator`` with ``podman`` on macOS.  Native source mounts from macOS through the ``podman`` machine into the execution environment are not currently available.

   See this `related issue <https://github.com/containers/podman/issues/8016>`__ for details.

Install ansible-navigator
=========================

#. Install the command line developer tools and proceed with the installation if prompted.

   .. code-block:: console

    xcode-select install

#. Install ansible-navigator:

   .. code-block:: console

    pip3 install ansible-navigator --user

#. Add the installation path to the PATH:

   .. code-block:: console

    echo 'export PATH=$HOME/Library/Python/3.8/bin:$PATH' >> ~/.zshrc

#. Open a new terminal or refresh the PATH:

   .. code-block:: console

    source ~/.zshrc

#. Launch ansible-navigator:

   .. code-block:: console

    ansible-navigator

#. ``ansible-navigator`` triggers a one-time download of the demo execution-environment image.


Windows with WSL2
*****************

Requirements
============

* Windows Subsystem for Linux 2
* Either ``podman`` or ``Docker Desktop for Windows``
* Internet access (during initial installation)

Setup WSL2 for Windows with Ubuntu
==================================

#. Install `WSL 2 <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`__.
#. Install the Ubuntu 20.04 LTS Linux distribution from the Microsoft store.
#. Open PowerShell and set the default WSL 2 distribution:

   .. code-block:: console

    wsl --set-default ubuntu

#. Launch the Ubuntu virtual machine from the Windows menu and complete the initial Ubuntu set-up.
#. From the Ubuntu terminal, create the ``/dev/mqueue`` directory:

   .. code-block:: console

    sudo mkdir /dev/mqueue


Install the desired container engine for execution environment support
======================================================================

* Installation instructions for ``podman`` on Ubuntu 20.04 LTS.

   .. note::

      The podman package is available in the official repositories for Ubuntu 20.10 and newer.
      Since interim releases of Ubuntu are not available on the Microsoft Store for WSL the
      `Kubic project <https://build.opensuse.org/package/show/devel:kubic:libcontainers:stable/podman>`__ package can be used.

   #. Update the ubuntu package index:

      .. code-block:: console

       sudo apt update

   #. Install system dependencies for ``podman``:

      .. code-block:: console

       apt-get install curl wget gnupg2

   #. Source the Ubuntu release:

      .. code-block:: console

       source /etc/os-release

   #. Add the ``podman`` repository:

     .. code-block:: console

      sudo sh -c "echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list"

   #. Download the GPG key:

     .. code-block:: console

      wget -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/xUbuntu_${VERSION_ID}/Release.key -O- | sudo apt-key add -

   #. Update using the new repository:

      .. code-block:: console

       sudo apt-get update

   #. Install ``podman``:

      .. code-block:: console

       sudo apt-get install podman

* Follow the `Docker Desktop for Windows <https://hub.docker.com/editions/community/docker-ce-desktop-windows>`__ installation instructions.

   * Be sure to complete the `Manage Docker as a non-root user <https://docs.docker.com/engine/install/linux-postinstall/>`__ steps.

Install ansible-navigator
=========================

From the Ubuntu terminal:
   #. Ensure the ``/dev/mqueue`` directory exists:

      .. code-block:: console

       sudo mkdir /dev/mqueue

   #. Install the python package manager:

      .. code-block:: console

       sudo apt install python3-pip

   #. Install ansible-navigator:

      .. code-block:: console

       python3 -m pip install ansible-navigator --user

   #. Add the installation path to the PATH:

      .. code-block:: console

       source ~/.profile

   #. Launch ansible-navigator:

      .. code-block:: console

       ansible-navigator

   #. ``ansible-navigator`` triggers a one-time download of the demo execution-environment image.
