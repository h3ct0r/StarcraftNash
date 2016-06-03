from strategy_base import StrategyBase
from collections import Counter
import random

__author__ = 'Hector Azpurua'


class WinPrev(StrategyBase):
    """
    Use previous knowledge to select the best strategy that
    beats the last selected bot
    """

    def __init__(self):
        self.strategy_name = 'WinPrev'

        # Bot	    Xeln	Cruz	NUSB	Aiur	Skyn
        # Xelnaga	50,00%	26,00%	86,00%	73,00%	73,00%
        # CruzBot	74,00%	50,00%	80,00%	67,00%	16,00%
        # NUSBot	14,00%	20,00%	50,00%	74,00%	97,00%
        # Aiur	    27,00%	33,00%	26,00%	50,00%	79,00%
        # Skynet	27,00%	84,00%	3,00%	21,00%	50,00%

        self.win_table = {
            "Skynet": {
                "Skynet": 0,
                "Xelnaga": 0.27,
                "CruzBot": 0.84
            },
            "Xelnaga": {
                "Skynet": 0.73,
                "Xelnaga": 0,
                "CruzBot": 0.26
            },
            "CruzBot": {
                "Skynet": 0.16,
                "Xelnaga": 0.74,
                "CruzBot": 0
            }
        }

        self.result_list = []
        self.match_list = []
        self.s_id = None
        pass

    def get_name(self):
        return self.strategy_name

    def set_id(self, s_id):
        self.s_id = s_id
        pass

    def set_match_list(self, match_list):
        self.match_list = match_list
        pass

    def set_result_list(self, result_list):
        self.result_list = result_list

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
