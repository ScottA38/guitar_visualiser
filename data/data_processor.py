import json


class DataProcessor:

    primaries = ["scales", "tunings"]

    def __init__(self, in_file)
        with open(in_file, 'r') as data_file:
            self.data = json.load(data_file)

        for key in self.data.keys():
            assert key in DataProcessor.primaries

        if "tunings" in self.data.keys():
            if "open" in self.data["tunings"].keys():
                #ensuring consistent data structure for tunings
                assert "roots" in self.data["tunings"].keys()
                for tuning in self.data["tunings"].values():
                    assert isinstance(tuning, str)
                    if
