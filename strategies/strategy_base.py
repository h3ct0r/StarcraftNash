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
        Returns the name of the opponent choice in the required match
        :param match_index: index (zero-based) of match,
        can be negative: -1 for previous match, -2 for second-last and so on
        :return:
        """
        if len(self.match_list) == 0:
            return None

        opponent_choice = None
        res = self.result_list[match_index]

        winner_choice, loser_choice = self.match_list[match_index]
        if res.upper() == 'A':
            a_bot = winner_choice
            b_bot = loser_choice
        else:
            a_bot = loser_choice
            b_bot = winner_choice

        if self.s_id == 'A':
            opponent_choice = b_bot
        else:
            opponent_choice = a_bot

        return opponent_choice
