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

        # initializes chance of each bot winning each other as zero
        self.win_count = {}
        for bot in self.bot_list:
            self.win_count[bot] = {opp: 0 for opp in self.bot_list}
            #self.win_count[bot][bot] = .5

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
        # TODO: implement incremental average, instead of recalculating every time
        opponent_bots = []
        opponent_counter = {}

        # erases win_probabilites, temporarily
        for bot in self.bot_list:
            self.win_count[bot] = {opp: 0 for opp in self.bot_list}

        for winner_bot, loser_bot in self.match_list:
            # res = self.result_list[i]
            # winner_bot, loser_bot = self.match_list[i]

            # works with win_count instead of probabilities (temporarily)
            self.win_count[winner_bot][loser_bot] += 1
            self.win_count[loser_bot][winner_bot] -= 1

        # replies to opponent's last choice
        opponent = None
        if len(self.match_list) > 0:
            res = self.result_list[-1]
            is_winner = (res.upper() == self.s_id.upper())

            # black magic copied from winprev =/
            winner_bot, loser_bot = self.match_list[-1]
            if res.upper() == 'A':
                a_bot = winner_bot
                b_bot = loser_bot
            else:
                a_bot = loser_bot
                b_bot = winner_bot

            if self.s_id == 'A':
                opponent = b_bot
            else:
                opponent = a_bot

            # responds with opponent's nemesis, i.e the one which it performs worst
            return min(self.win_count[opponent], key=self.win_count[opponent].get)

        # no history present or could not count victories, chooses randomly
        return random.choice(self.bot_list)
