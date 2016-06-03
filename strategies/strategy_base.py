from abc import ABCMeta, abstractmethod

__author__ = 'Hector Azpurua'


class StrategyBase(object):
    __metaclass__ = ABCMeta

    # static list so that every strategy can use the same bots
    bot_list = ["Skynet", "Xelnaga", "NUSBot"]


    def set_bot_list(self, b_list):
        self.bot_list = b_list

    @abstractmethod
    def set_id(self, s_id):
        pass

    @abstractmethod
    def get_name(self, s_id):
        pass

    @abstractmethod
    def get_next_bot(self):
        return ''

    #@abstractmethod
    def set_match_list(self, match_list):
        self.match_list = match_list

    #@abstractmethod
    def set_result_list(self, result_list):
        self.result_list = result_list

    def get_result_list(self):
        return self.result_list

    def get_match_list(self):
        return self.match_list

    def find_opponent_choice(self, match_number):
        opponent_choice = None
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
                opponent_choice = b_bot
            else:
                opponent_choice = a_bot

        return opponent_choice