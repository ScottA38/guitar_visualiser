from data import data_processor
from guitar_visualiser import Scale
import os

_data_processor = DataProcessor()

recognised = ["scale", "tuning", "note"]

os.chdir("data")
for item in os.listdir():
    if os.path.isdir(item) and item in recognised and item[0] != "_" and item[0] != ".":
        _data_processor.add_pair(item)

os.chdir("..")

source_data = _data_processor.objs


def scale_factory(obj):
    out = tuple()
    for rkey in obj['relativeKey']:
        out += tuple(Scale(obj['scaleName']), )
