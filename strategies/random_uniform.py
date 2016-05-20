from strategy_base import StrategyBase
import random

__author__ = 'Hector Azpurua'


class Random(StrategyBase):
    def __init__(self):
        self.strategy_name = 'Random uniform'
        self.bots = ["Skynet", "Xelnaga", "NUSBot"]
        self.result_list = []
        pass

    def set_result_list(self, result_list):
        self.result_list = result_list

    def get_next_bot(self):
        bot = random.choice(self.bots)
        return bot
