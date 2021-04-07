#!/bin/bash -xe

LSBDISTCODENAME=$(lsb_release -cs)

# For ubuntu bionic, install podman
if [ $LSBDISTCODENAME == 'bionic' ]; then
    . /etc/os-release
    echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
    curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key | sudo apt-key add -
    sudo apt-get update
    sudo apt-get -y upgrade
    sudo apt-get -y install podman
    systemctl --user restart dbus
fi
