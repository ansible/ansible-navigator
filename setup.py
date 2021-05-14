""" setup """
import glob
import os
from itertools import groupby
from operator import itemgetter

from setuptools import setup

# valid files in share to be copied
data_file_types = [".yml", ".py", ".json", ".md"]

# generate a [(dir, file),...] for all share files
file_pairs = [
    (x[0], y)
    for x in os.walk("share")
    for y in glob.glob(os.path.join(x[0], "**"))
    if os.path.isfile(y) and os.path.splitext(y)[1] in data_file_types
]

# group by dir [(dir, [files, file]),...]
# data_files specifies a sequence of (directory, files) pairs in the following way:
# setup(...,
#     data_files=[('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
#                 ('config', ['cfg/data.cfg'])],
#     )
# Each (directory, files) pair in the sequence specifies the installation directory
# and the files to install there.
data_file_list = [(k, list(list(zip(*g))[1])) for k, g in groupby(file_pairs, itemgetter(0))]

setup(data_files=data_file_list)
