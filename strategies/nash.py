from strategy_base import StrategyBase
import sys
import random
import config

__author__ = 'Hector Azpurua'


class Nash(StrategyBase):

    def __init__(self, strategy_name):
        self.strategy_name = strategy_name
        self.probabilities = None

        #self.bot_list = ["Skynet", "Xelnaga", "NUSBot"]
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
        if self.probabilities is None:
            self.probabilities = config.Config.get_instance().get_bots()

        prob = sum(self.probabilities.values())
        # for key in self.probabilities.keys():
        #     prob += self.probabilities[key]

        if not(0.99 <= prob <= 1.0):
            print >> sys.stderr, "Sum of probabilities is not 1", prob
            print >> sys.stderr, self.probabilities
            #return None

        rand_n = random.uniform(0, prob)

        prob = 0
        bot_keys = self.probabilities.keys()

        for i in xrange(len(bot_keys)):
            key = bot_keys[i]
            prob += self.probabilities[key]
            if rand_n < prob or (i >= len(bot_keys)-1):
                return key

        print >> sys.stderr, "Something strange happened, a bot wasn't selected by Nash Eq", prob, rand_n
        print >> sys.stderr, self.probabilities

        return None
