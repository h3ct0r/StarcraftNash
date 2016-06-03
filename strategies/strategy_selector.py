import sys
import nash
import random_uniform
import frequentist
import reply_last
import win_prev
import e_greedy
import rotate
import unique

__author__ = 'Hector Azpurua'


class StrategySelector:

    strategies = {
        'nash': nash.Nash,
        'random_uniform': random_uniform.RandomUniform,
        'frequentist': frequentist.Frequentist,
        'winprev': win_prev.WinPrev,
        'replylast': reply_last.ReplyLast,
        'egreedy': e_greedy.EGreedy,
        'rotate': rotate.Rotate
    }

    def __init__(self):
        self.choices = []
        pass

    def update_strategies(self, new_strat):
        for elem in new_strat.keys():
            if elem not in self.strategies:
                self.strategies[elem] = None

        #print 'Updated strategies:', self.strategies

    def set_unique_choices(self, choices):
        self.choices = choices

    def get_unique_choices(self):
        return self.choices

    def get_strategy(self, strategy):
        if strategy not in self.strategies.keys() or self.strategies[strategy] is None:
            # If the strategy is an opponent from the match list
            if strategy in self.choices or (strategy in self.strategies and self.strategies[strategy] is None):
                return unique.Unique(strategy)

            print >> sys.stderr, 'Strategy not in player list or in bot list:', strategy
            return None

        return self.strategies[strategy]()
