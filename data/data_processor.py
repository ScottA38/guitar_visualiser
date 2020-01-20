import os
import sys
import json

class DataProcessor:
    def __init__(self, *args):
        self.objs = {}
        if len(*args) > 0:
            for i, val in enumerate(*args):
                self.push_obj(val)

    def push_obj(self, src_path):
        assert os.path.exists(src_path), "Invalid file path given to DataProcessor.push_obj()"
        try:
            with open(src_path, 'r') as fp_json:
                obj = json.load(fp_json)
                self.objs.update({os.path.basename(src_path).split('.')[0]: obj})
        except BaseException as e:
            raise e

def json_only(elem):
    if elem.split('.')[-1] == "json":
        return True

def make_filepath(filename):
    rel = os.path.join(os.path.dirname(sys.argv[0]), "data", filename)
    return os.path.abspath(rel)
