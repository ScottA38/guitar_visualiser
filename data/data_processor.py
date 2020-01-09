from json_schema_validator.shortcuts import *
import os
import sys

os.chdir("data")

in_tests = (("scale_schema.json", "scales.json"), ("tunings_schema.json", "tunings.json"))

for test in in_tests:
    print(f"Validating {test}", end="\n\n\n")
    try:
        schema = open(test[0], 'r').read()
        json = open(test[1], 'r').read()
        validate(schema, json)
        print(f"'{test[0]}' successfully validated json data: '{test[1]}'")
    except BaseException as e:
        raise e
# class DataProcessor:
#
#     primaries = ["scales", "tunings"]
#
#     def __init__(self, in_file)
#         with open(in_file, 'r') as data_file:
#             self.data = json.load(data_file)
#
#         for key in self.data.keys():
#             assert key in DataProcessor.primaries
#
#         if "tunings" in self.data.keys():
#             if "open" in self.data["tunings"].keys():
#                 #ensuring consistent data structure for tunings
#                 assert "roots" in self.data["tunings"].keys()
#                 for tuning in self.data["tunings"].values():
#                     assert isinstance(tuning, str)
#                     if
