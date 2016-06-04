import os
import re
import random

__author__ = 'Hector Azpurua'


class ResultParser:
    def __init__(self, result_file):
        if not os.path.isfile(result_file):
            raise AttributeError('The input file does not exist ' + result_file)

        self.match_list = []
        self.file_path = result_file
        self.parse_file()

        pass

    def get_unique_opponents(self):
        if len(self.match_list) <= 0:
            return None

        elem_list = list(sum(self.match_list, ()))
        uniq_list = list(set(elem_list))

        return uniq_list

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

    def shuffle_match_list(self):
        """
        Shuffles match list
        :return:
        """
        random.shuffle(self.match_list)

    def analyse(self, bot1, bot2, first=0, last=None):
        """
        Analyses parsed results file and returns 2 lists suitable to plotting.
        The lists are filled according to matches of bot1 vs bot2
        First list contains the x values, for counting the matches played by the
        two bots.
        Second list contains the y values: 0 indicates victory of bot1 and 1 indicates
        its defeat in the corresponding match.

        :param bot1: name of first bot
        :param bot2: name of second bot
        :param first: number of first match to consider (ignores previous bot1 vs bot2 matches)
        :param last: number of last match to consider (ignores posterior bot1 vs bot2 matches)
        :return: list, list
        """

        if last is None:
            last = len(self.get_match_list())

        valid_matches = -1
        x_values = []
        y_values = []
        for winner, loser in self.get_match_list():

            if winner in [bot1, bot2] and loser in [bot1, bot2]:

                valid_matches += 1

                if valid_matches < first:
                    continue

                if valid_matches > last:
                    break

                x_values.append(valid_matches)

                # y=0 is bot1 and y=1 is bot2
                if winner == bot1:
                    y_values.append(0)
                else:
                    y_values.append(1)
        return x_values, y_values
