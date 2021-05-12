""" setup """
import glob
import os
from itertools import groupby
from operator import itemgetter

from setuptools import setup

data_file_types = [".yml", ".py", ".json", ".md"]
file_pairs = [
    (x[0], y)
    for x in os.walk("share")
    for y in glob.glob(os.path.join(x[0], "**"))
    if os.path.isfile(y) and os.path.splitext(y)[1] in data_file_types
]
data_file_list = [(k, list(list(zip(*g))[1])) for k, g in groupby(file_pairs, itemgetter(0))]

setup(data_files=data_file_list)
