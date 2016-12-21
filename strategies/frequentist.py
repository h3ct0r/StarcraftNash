from strategy_base import StrategyBase
from collections import Counter
from config import Config
import scorechart
import random

__author__ = 'Hector Azpurua'   # refactor by Anderson


class Frequentist(StrategyBase):
    """
    Tries to beat opponent by selecting the strategy that
    counters its most frequent choice.
    Queries a previously built score chart to determine best response to opponent
    """

    def __init__(self, strategy_name):
        StrategyBase.__init__(self, strategy_name)

        # uses score chart to determine best response
        self.score_chart = scorechart.from_file(
            Config.get_instance().get(Config.SCORECHART_FILE)
        )

    def get_name(self):
        return self.strategy_name

    def get_next_bot(self):
        """
        Returns the strategy that counters opponent's most
        frequent choice.
        Uses previous knowledge to find best response to opponent
        :return:
        """
        opponent_counter = {choice: 0 for choice in self.bot_list}

        for match_index in range(self.history_length()):
            opponent_counter[self.opponent_choice(match_index)] += 1

        most_common_opponent = max(opponent_counter, key=opponent_counter.get)

        # returns opponent's nemesis (i.e. the one that makes it perform worst)
        return min(self.score_chart[most_common_opponent], key=self.score_chart[most_common_opponent].get)

    def most_frequent_opponent_choice(self):
        """
        Returns the most frequent choice by the opponent
        :return:
        """
        opponent_counter = {choice: 0 for choice in self.bot_list}

        for match_index in range(self.history_length()):
            opponent_counter[self.opponent_choice(match_index)] += 1

        return max(opponent_counter, key=opponent_counter.get)


class HistoryFrequentist(Frequentist):
    """
    Tries to beat opponent by selecting the strategy that
    counters its most frequent choice.
    Queries previous match history to determine best response.
    """

    def __init__(self):
        Frequentist.__init__(self)
        self.strategy_name = 'HistoryFreq'

    def get_next_bot(self):
        """
       Returns the strategy that had most success
        against opponent's most frequent choice in previous matches
        :return:
        """
        most_common_opponent = self.most_frequent_opponent_choice()

        # no history present or could not count victories, chooses randomly
        if most_common_opponent is None:
            return random.choice(self.bot_list)

        # usage: win_count[strategy1][strategy2]
        win_count = self.calculate_score_table()

        # responds with opponent's nemesis, i.e the one that makes it perform worst
        return min(win_count[most_common_opponent], key=win_count[most_common_opponent].get)

