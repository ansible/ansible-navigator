FROM fedora:35

RUN dnf install gcc git python3.10 python3.8 python3-devel -y
RUN python3.10 -m ensurepip --upgrade

RUN git clone https://github.com/ansible/ansible-navigator.git

WORKDIR /ansible-navigator

RUN pip3.10 install -r test-requirements.txt
RUN pip3.10 install -r requirements.txt
RUN pip3.10 install tox

RUN git pull origin pull/841/head

RUN tox -e lint
