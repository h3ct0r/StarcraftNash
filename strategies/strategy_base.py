from abc import ABCMeta, abstractmethod

__author__ = 'Hector Azpurua'


class StrategyBase(object):
    __metaclass__ = ABCMeta

    # static list so that every strategy can use the same bots
    bot_list = ["Skynet", "Xelnaga", "NUSBot"]

    def __init__(self):
        self.strategy_name = 'StrategyBase'
        self.result_list = []
        self.match_list = []
        self.s_id = None

    def set_bot_list(self, b_list):
        self.bot_list = b_list

    def set_id(self, s_id):
        self.s_id = s_id

    def get_id(self):
        return self.s_id

    def get_name(self):
        return self.strategy_name

    @abstractmethod
    def get_next_bot(self):
        return ''

    def get_match_list(self):
        return self.match_list

    def set_match_list(self, match_list):
        self.match_list = match_list

    def get_result_list(self):
        return self.result_list

    def set_result_list(self, result_list):
        self.result_list = result_list

    def find_opponent_choice(self, match_index):
        """
        Returns the name of opponent choice in the required match
        :param match_index: index (zero-based) of match,
        can be negative: -1 for previous match, -2 for second-last and so on
        :return:str
        """
        if len(self.match_list) == 0:
            return None

        res = self.result_list[match_index]

        winner_choice, loser_choice = self.match_list[match_index]

        if res.upper() == 'A':
            bot_a = winner_choice
            bot_b = loser_choice
        else:
            bot_a = loser_choice
            bot_b = winner_choice

        # opponent choice is B if I am A and vice-versa
        return bot_b if self.s_id == 'A' else bot_a
