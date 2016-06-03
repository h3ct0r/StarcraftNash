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

