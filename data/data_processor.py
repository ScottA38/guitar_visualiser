from json_schema_validator.schema import Schema
from json_schema_validator.validator import Validator
import os
import sys
import json

class DataProcessor:

    def __init__(self):
        self._validator = Validator()
        self.objs = {}

    def add_pair(self, dirname):
        try:
            json_path = os.path.realpath(os.path.join(dirname, dirname + "s.json" ))
            schema_path = os.path.realpath(os.path.join(dirname, dirname + "_schema.json" ))
            with open(schema_path, 'r') as fp_schema:
                with open(json_path, 'r') as fp_json:
                    schema_obj = Schema(json.load(fp_schema))
                    obj = json.load(fp_json)
                    assert Validator.validate(schema_obj, obj), "JSON document failed schema validation"
                    self.objs.update({dirname: obj})
        except BaseException as e:
            raise e
