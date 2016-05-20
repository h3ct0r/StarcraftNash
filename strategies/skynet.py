from strategy_base import StrategyBase
import random_uniform

__author__ = 'Hector Azpurua'


class Skynet(StrategyBase):
    def __init__(self):
        self.strategy_name = 'Skynet'
        self.bots = ["Skynet", "Xelnaga", "NUSBot"]
        self.result_list = []
        pass

    def set_result_list(self, result_list):
        self.result_list = result_list

    def get_next_bot(self):
        return self.bots[0]
