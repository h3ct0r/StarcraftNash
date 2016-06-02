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

    def update_strategies(self, new_strat):
        for elem in new_strat.keys():
            if elem not in self.strategies:
                self.strategies[elem] = None

        print 'Updated strategies:', self.strategies

    def set_unique_opponents(self, opponent_list):
        self.opponent_list = opponent_list

    def get_unique_opponents(self):
        return self.opponent_list

    def get_strategy(self, strategy):
        if strategy not in self.strategies.keys() or self.strategies[strategy] is None:
            # If the strategy is an opponent from the match list
            if strategy in self.opponent_list or (strategy in self.strategies and self.strategies[strategy] is None):
                return unique_opponent.UniqueOpponent(strategy)

            print >> sys.stderr, 'Strategy not in strategy list or in opponent list:', strategy
            return None

        return self.strategies[strategy]()
