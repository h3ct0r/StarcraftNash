import sys
import nash
import random_uniform
import skynet
import xelnaga
import nusbot

__author__ = 'Hector Azpurua'


class StrategySelector:

    strategies = {
        'nash': nash.Nash,
        'random_uniform': random_uniform.Random,
        'max_win_prev': None,
        'win_prev': None,
        'skynet': skynet.Skynet,
        'xelnaga': xelnaga.Xelnaga,
        'nusbot': nusbot.Nusbot
    }

    def __init__(self):
        pass

    def get_strategy(self, strategy):
        if strategy not in self.strategies.keys():
            print >> sys.stderr, 'Strategy not in strategy list'
            return None

        return self.strategies[strategy]()
