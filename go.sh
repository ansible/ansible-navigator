#!/bin/sh

for run in {1..5}
do
    pre-commit run pylint --all-files -v | grep duration
    sleep 5
done