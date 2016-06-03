from strategy_base import StrategyBase
import random_uniform

__author__ = 'Hector Azpurua'


class Unique(StrategyBase):
    """
    Selects the same strategy every time
    """

    def __init__(self, strategy_name):
        self.strategy_name = strategy_name
        self.result_list = []
        self.match_list = []
        self.s_id = None
        pass

    def get_next_bot(self):
        """
        Always returns the same bot (configured in __init__)
        :return:
        """
        return self.strategy_name
