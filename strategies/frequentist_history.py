from strategy_base import StrategyBase
from collections import Counter
from config import Config
import scorechart
import random

__author__ = 'Hector Azpurua'


class Frequentist(StrategyBase):
    """
    Tries to beat opponent by selecting the strategy that
    counters its most frequent choice.
    Queries previous match history to determine best response.
    """

    def __init__(self):
        StrategyBase.__init__(self)
        self.strategy_name = 'Freq-hist'

    def get_name(self):
        return self.strategy_name

    # def set_id(self, s_id):
    #     self.s_id = s_id
    #
    # def set_match_list(self, match_list):
    #     self.match_list = match_list
    #
    # def set_result_list(self, result_list):
    #     self.result_list = result_list

    def get_next_bot(self):
        """
        Returns the strategy that counters opponent's most
        frequent choice
        :return:
        """
        opponent_bots = []
        opponent_counter = {}

        for i in xrange(len(self.result_list)):
            res = self.result_list[i]
            winner_bot, loser_bot = self.match_list[i]

            is_winner = False
            if res.upper() == self.s_id.upper():
                is_winner = True

            if res.upper() == 'A':
                a_bot = winner_bot
                b_bot = loser_bot
            else:
                a_bot = loser_bot
                b_bot = winner_bot

            if self.s_id == 'A':
                opponent = b_bot
                self_bot = a_bot
            else:
                opponent = a_bot
                self_bot = b_bot

            opponent_bots.append(opponent)

            if is_winner:
                if opponent not in opponent_counter:
                    opponent_counter[opponent] = {}
                if self_bot not in opponent_counter[opponent]:
                    opponent_counter[opponent][self_bot] = 1
                else:
                    opponent_counter[opponent][self_bot] += 1
            pass

        data = Counter(opponent_bots)
        most_common_opponent = None

        if len(data.most_common(1)) > 0:
            most_common_opponent = data.most_common(1)[0][0]

        b_key = None
        b_val = 0
        if most_common_opponent is not None and most_common_opponent in opponent_counter:
            for key, value in opponent_counter[most_common_opponent].items():
                if b_key is None or value > b_val:
                    b_key = key
                    b_val = value
            return b_key
        else:
            b_key = random.choice(self.bot_list)
            if Config.get_instance().verbose:
                print 'Freq-blind returning random...'

        return b_key
