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
        # initializes chance of each bot winning each other as zero
        # usage: win_count[me][adversary]
        win_count = {mine: {opponent: 0 for opponent in self.bot_list} for mine in self.bot_list}

        # updates win_count according to previous matches
        for winner_bot, loser_bot in self.match_list:
            # res = self.result_list[i]
            # winner_bot, loser_bot = self.match_list[i]

            win_count[winner_bot][loser_bot] += 1
            win_count[loser_bot][winner_bot] -= 1

        #print win_count

        # replies to opponent's last choice
        opponent_choice = self.find_opponent_choice(-1)

        # no history present or could not count victories, chooses randomly
        if opponent_choice is None:
            return random.choice(self.bot_list)

        # responds with opponent's nemesis, i.e the one that makes it perform worst
        return min(win_count[opponent_choice], key=win_count[opponent_choice].get)

