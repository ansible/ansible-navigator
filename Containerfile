FROM ubuntu:20.04

RUN apt update -y && apt upgrade -y
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt install git software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa


RUN apt install python3.10 python3.8 python3-pip -y

RUN git clone https://github.com/ansible/ansible-navigator.git

WORKDIR /ansible-navigator

RUN pip install tox

RUN tox -e lint
