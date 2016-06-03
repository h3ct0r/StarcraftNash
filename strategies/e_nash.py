from strategy_base import StrategyBase
import sys
import nash
import frequentist
import random
import config

__author__ = 'Anderson Tavares'


class EpsilonNash(StrategyBase):

    """
    Returns Nash-equilibria with probability (1-epsilon);
    Returns frequentist (exploitation) with probability epsilon.
    This is an epsilon-safe strategy
    """

    def __init__(self, epsilon=0.1):
        """
        Initializes Epsilon-Nash strategy
        :param epsilon: probability of EXPLOITATION
        :return:
        """
        StrategyBase.__init__(self)
        self.strategy_name = 'E-Nash'
        self.epsilon = epsilon      # probability of exploitation (different of e-greedy which is exploration)
        self.nash = nash.Nash()
        self.exploitation = frequentist.Frequentist()

    def set_match_list(self, match_list):
        self.match_list = match_list
        self.nash.match_list = match_list
        self.exploitation.match_list = match_list

    def set_result_list(self, result_list):
        self.result_list = result_list
        self.nash.result_list = result_list
        self.exploitation.result_list = result_list

    def set_id(self, s_id):
        self.s_id = s_id
        self.nash.s_id = s_id
        self.exploitation.s_id = s_id

    def get_next_bot(self):
        """
        Uses Nash with probability (1-epsilon); or Exploitation with prob. epsilon
        :return:
        """

        if random.random() < self.epsilon:
            print 'exploitation'
            return self.exploitation.get_next_bot()

        print 'safe'
        return self.nash.get_next_bot()
