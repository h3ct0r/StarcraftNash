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
        # TODO: implement incremental average, instead of recalculating every time

        # initializes chance of each bot winning each other as zero
        win_count = {}
        for bot in self.bot_list:
            win_count[bot] = {opp: 0 for opp in self.bot_list}

        for winner_bot, loser_bot in self.match_list:
            # res = self.result_list[i]
            # winner_bot, loser_bot = self.match_list[i]

            # works with win_count instead of probabilities (temporarily)
            win_count[winner_bot][loser_bot] += 1
            win_count[loser_bot][winner_bot] -= 1

        # replies to opponent's last choice
        opponent_choice = self.find_opponent_choice(-1)

        # no history present or could not count victories, chooses randomly
        if opponent_choice is None:
            return random.choice(self.bot_list)

        # responds with opponent's nemesis, i.e the one which it performs worst
        return min(win_count[opponent_choice], key=win_count[opponent_choice].get)

