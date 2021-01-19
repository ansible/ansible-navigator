FROM quay.io/ansible/network-ee-sanity-tests:latest

ADD licenses $HOME/src/winston/licenses
ADD winston $HOME/src/winston/winston
ADD share $HOME/src/winston/share
ADD setup.* $HOME/src/winston/

RUN pip install $HOME/src/winston

# podman run -i -t -e TERM=${TERM} -v ${PWD}:${PWD}:z -w ${PWD} winston_img winston