from strategy_base import StrategyBase
from collections import Counter
import random

__author__ = 'Hector Azpurua'


class WinPrev(StrategyBase):
    def __init__(self):
        self.strategy_name = 'WinPrev'
        self.win_table = {
            "Skynet": {
                "Skynet": 0,
                "Xelnaga": 0.31,
                "NUSBot": 0.9
            },
            "Xelnaga": {
                "Skynet": 0.69,
                "Xelnaga": 0,
                "NUSBot": 0.3
            },
            "NUSBot": {
                "Skynet": 0.1,
                "Xelnaga": 0.7,
                "NUSBot": 0
            }
        }
        self.bot_list = ["Skynet", "Xelnaga", "NUSBot"]
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
        if len(opponent_bots) > 0:
            last = opponent_bots[-1]
            if last in self.win_table:
                b_val = 0
                for key, value in self.win_table[last].items():
                    if b_key is None or value > b_val:
                        b_key = key
                        b_val = value

        if b_key is None:
            b_key = random.choice(self.bot_list)

        return b_key
