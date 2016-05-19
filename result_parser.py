import os
import re

__author__ = 'Hector Azpurua'


class ResultParser:
    def __init__(self, result_file):
        if not os.path.isfile(result_file):
            raise AttributeError('The input file does not exist ' + result_file)

        self.match_list = []
        self.file_path = result_file
        self.parse_file()

        pass

    def get_match_list(self):
        return self.match_list

    def parse_file(self):
        with open(self.file_path) as f:
            for line in f:
                segments = re.split(r'[\s]+', line)
                if len(segments) < 6:
                    continue
                self.match_list.append((segments[3], segments[4]))
        pass
