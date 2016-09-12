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

    def __init__(self):
        StrategyBase.__init__(self)
        self.strategy_name = 'Frequentist_refactor'

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

