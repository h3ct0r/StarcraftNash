import sys
import nash
import random_uniform
import frequentist
import reply_last
import e_greedy
import e_nash
import rotate
import unique
import exp3
import ucb
import fictitious_play
import no_regret

__author__ = 'Hector Azpurua'


class StrategySelector:

    strategies = {
        'unique': unique.Unique,                            # choose always the same option
        'nash': nash.Nash,                                  # plays nash equilibrium
        'random_uniform': random_uniform.RandomUniform,     # plays uniformly random
        'frequentist': frequentist.Frequentist,             # responds to most frequent choice (uses score chart)
        'freqhist': frequentist.HistoryFrequentist,         # responds to most frequent choice (uses history)
        'replyscore': reply_last.PriorKnowledgeReplyLast,   # responds to last opponent choice (uses score chart)
        'replyhist': reply_last.NoPriorReplyLast,           # responds to last opponent choice (uses history)
        'egreedy': e_greedy.EGreedy,                        # greedy (regarding total score) w/ prob 1-e; explores w/ prob e
        'egreedyavg': e_greedy.EGreedyAverage,              # greedy (regarding average score) w/ prob 1-e; explores w/ prob e
        'ucb1': ucb.UCB1,                                   # uses UCB1 formula from Auer et. al. 2002
        'ucb1tuned': ucb.UCB1Tuned,                         # uses UCB1-Tuned formula from Auer et. al. 2002
        'exp3': exp3.Exp3,                                  # uses Exp3 algorithm from Auer et. al. 1995
        'enash': e_nash.EpsilonNash,                        # nash w/ prob 1-e; frequentist w/ prob e
        'rotate': rotate.Rotate,                            # selects sequentially
        'fictitious': fictitious_play.FictitiousPlay,       # fictitious play
        'noregret': no_regret.NoRegret                      # no-regret
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
        #if strategy.type not in self.strategies.keys() or self.strategies[strategy] is None:
        #    # If the strategy is an opponent from the match list
        #    if strategy in self.choices or (strategy in self.strategies and self.strategies[strategy] is None):
        #        return unique.Unique(strategy)

        #    print >> sys.stderr, 'Strategy not in player list or in bot list:', strategy
        #    return None

        if strategy.player_type not in self.strategies:
            raise Exception('Strategy not in player list or in bot list: ' + str(strategy))

        if strategy.config_tag_name is not None:
            try:
                s = self.strategies[strategy.player_type](strategy.player_name, strategy.config_tag_name)
            except TypeError:
                s = self.strategies[strategy.player_type](strategy.player_name)
                s.set_config_name(strategy.config_tag_name)
        else:
            s = self.strategies[strategy.player_type](strategy.player_name)

        return s

    @staticmethod
    def recreate_strategy(s):
        s_type = type(s)

        if hasattr(s, 'config_name') and s.config_name is not None:
            try:
                new_s = s_type(s.strategy_name, s.config_name)
            except TypeError:
                new_s = s_type(s.strategy_name)
                new_s.set_config_name(s.config_name)
        else:
            new_s = s_type(s.strategy_name)

        new_s.set_id(s.get_id())

        return new_s
