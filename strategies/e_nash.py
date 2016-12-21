from strategy_base import StrategyBase
import nash
import frequentist
import random
from config import Config

__author__ = 'Anderson Tavares'


class EpsilonNash(StrategyBase):

    """
    Returns Nash-equilibria with probability (1-epsilon);
    Returns frequentist (exploitation) with probability epsilon.
    This is an epsilon-safe strategy
    """

    def __init__(self, strategy_name):
        """
        Initializes Epsilon-Nash strategy
        :param epsilon: probability of EXPLOITATION
        :return:
        """
        StrategyBase.__init__(self, strategy_name)
        # probability of exploitation (different of e-greedy which is exploration)
        self.epsilon = Config.get_instance().enash_exploitation

        # Nash equilibrium strategy
        self.nash = nash.Nash('Nash inside e-Nash')

        # exploitation strategy
        self.exploitation = frequentist.Frequentist('Frequentist inside e-Nash')

    def set_match_list(self, match_list):
        self.match_list = match_list
        self.nash.set_match_list(match_list)
        self.exploitation.set_match_list(match_list)

    def set_result_list(self, result_list):
        self.result_list = result_list
        self.nash.set_result_list(result_list)
        self.exploitation.set_result_list(result_list)

    def set_id(self, s_id):
        self.s_id = s_id
        self.nash.set_id(s_id)
        self.exploitation.set_id(s_id)

    def get_next_bot(self):
        """
        Uses Nash with prob. (1-epsilon); or Exploitation with prob. epsilon
        :return:
        """

        if random.random() < self.epsilon:
            return self.exploitation.get_next_bot()

        return self.nash.get_next_bot()
