import sys
import nash
import random_uniform
import max_win_prev
import win_prev
import e_greedy
import unique_opponent

__author__ = 'Hector Azpurua'


class StrategySelector:

    strategies = {
        'nash': nash.Nash,
        'random_uniform': random_uniform.RandomUniform,
        'max_win_prev': max_win_prev.MaxWinPrev,
        'win_prev': win_prev.WinPrev,
        'egreedy': e_greedy.EGreedy
    }

    def __init__(self):
        self.opponent_list = []
        pass

    def set_unique_opponents(self, opponent_list):
        self.opponent_list = opponent_list

    def get_strategy(self, strategy):
        if strategy not in self.strategies.keys():
            # If the strategy is an opponent from the match list
            if strategy in self.opponent_list:
                return unique_opponent.UniqueOpponent(strategy)

            print >> sys.stderr, 'Strategy not in strategy list or in opponent list'
            return None

        return self.strategies[strategy]()
