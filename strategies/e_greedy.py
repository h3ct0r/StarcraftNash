from strategy_base import StrategyBase
import random

__author__ = 'Hector Azpurua'


class EGreedy(StrategyBase):
    """
    Use the e greedy function to search a good strategy
    based on a epsilon  probability of exploration and a e-1 probability of
    selecting the best know strategy
    """

    def __init__(self, epsilon=.1):
        """

        :param epsilon: probability of EXPLORATION
        :return:
        """
        self.strategy_name = 'E-greedy'
        self.result_list = []
        self.match_list = []
        self.s_id = None
        self.e = epsilon
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
        bot_wins = {}

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
                if self_bot not in bot_wins:
                    bot_wins[self_bot] = 1
                else:
                    bot_wins[self_bot] += 1
            pass

        if random.random() < self.e or len(bot_wins.keys()) <= 0:
            b_key = random.choice(self.bot_list)
        else:
            b_key = None
            b_value = 0
            for key in bot_wins.keys():
                value = bot_wins[key]
                if b_key is None or value > b_value:
                    b_key = key
                    b_value = value

        return b_key
