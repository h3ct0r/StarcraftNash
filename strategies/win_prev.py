from strategy_base import StrategyBase
from config import Config
import scorechart
import random

__author__ = 'Hector Azpurua'


class WinPrev(StrategyBase):
    """
    Use previous knowledge to select the best strategy that
    beats the last selected bot
    """

    def __init__(self):
        StrategyBase.__init__(self)
        self.strategy_name = 'WinPrev'

        # loads score chart from file
        self.win_table = scorechart.from_file(
            Config.get_instance().get(Config.SCORECHART_FILE)
        )

        # forces zeros on diagonal to avoid responding with same bot
        # for choice in self.win_table.keys():
        #     self.win_table[choice][choice] = 0

        # print self.win_table

    def get_next_bot(self):
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

        b_key = None
        b_val = 0
        if len(opponent_bots) > 0:
            last = opponent_bots[-1]
            for key in self.win_table.keys():
                if last in self.win_table[key]:
                    value = self.win_table[key][last]
                    if b_key is None or value > b_val:
                        b_key = key
                        b_val = value

        if b_key is None:
            b_key = random.choice(self.bot_list)

        return b_key
