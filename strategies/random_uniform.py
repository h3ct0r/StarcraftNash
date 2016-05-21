from strategy_base import StrategyBase
import random

__author__ = 'Hector Azpurua'


class Random(StrategyBase):
    def __init__(self):
        self.strategy_name = 'Random uniform'
        self.bot_list = ["Skynet", "Xelnaga", "NUSBot"]
        self.result_list = []
        self.match_list = []
        self.s_id = None
        pass

    def set_strategy_id(self, s_id):
        self.s_id = s_id
        pass

    def set_match_list(self, match_list):
        self.match_list = match_list
        pass

    def set_result_list(self, result_list):
        self.result_list = result_list

    def get_next_bot(self):
        bot = random.choice(self.bots_list)
        return bot
