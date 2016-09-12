import sys
import nash
import random_uniform
import frequentist
import reply_history
import reply_score
import win_prev
import e_greedy
import e_nash
import rotate
import unique

__author__ = 'Hector Azpurua'


class StrategySelector:

    strategies = {
        'nash': nash.Nash,                                  # plays nash equilibrium
        'random_uniform': random_uniform.RandomUniform,     # plays uniformly random
        'frequentist': frequentist.Frequentist,             # responds to most frequent choice (uses score chart)
        'freqhist': frequentist.HistoryFrequentist,         # responds to most frequent choice (uses history)
        'winprev': win_prev.WinPrev,                        # responds to last opponent choice (uses score chart)
        'replyscore': reply_score.ReplyLast,                # same as winprev, but faster
        'replyhist': reply_history.ReplyLast,               # responds to last opponent choice (uses history)
        'egreedy': e_greedy.EGreedy,                        # greedy w/ prob 1-e; explores w/ prob e
        'enash': e_nash.EpsilonNash,                        # nash w/ prob 1-e; frequentist w/ prob e
        'rotate': rotate.Rotate                             # selects sequentially
    }

    def __init__(self):
        self.choices = []
        pass

    def update_strategies(self, new_strat):
        for elem in new_strat.keys():
            if elem not in self.strategies:
                self.strategies[elem] = None

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
