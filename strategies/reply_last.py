from strategy_base import StrategyBase
from collections import Counter
import random

__author__ = 'Anderson Tavares'


class ReplyLast(StrategyBase):
    """
    Similar to WinPrev (selects the bot that would beat last opponent choice)
    but has no prior table; i.e. builds statistics
    based on history
    """

    def __init__(self):
        self.strategy_name = 'ReplyLast'
        self.result_list = []
        self.match_list = []
        self.s_id = None
        pass

    def get_next_bot(self):
        # usage: win_count[me][adversary]
        win_count = self.calculate_score_table()

        # finds opponent's last choice
        opponent_choice = self.find_opponent_choice(-1)

        # no history present or could not count victories, chooses randomly
        if opponent_choice is None:
            return random.choice(self.bot_list)

        # responds with opponent's nemesis, i.e the one that makes it perform worst
        return min(win_count[opponent_choice], key=win_count[opponent_choice].get)

