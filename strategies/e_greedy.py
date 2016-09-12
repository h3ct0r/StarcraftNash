from strategy_base import StrategyBase
import random
from config import Config

__author__ = 'Hector Azpurua'  # refactored by Anderson


class EGreedy(StrategyBase):
    """
    Use the epsilon-greedy method for strategy selection:
    Chooses a random strategy (exploration) with probability epsilon
    and chooses the best known strategy with probability 1-epsilon
    """

    def __init__(self):
        """
        Initializes epsilon-greedy strategy selection method
        """

        StrategyBase.__init__(self)
        self.strategy_name = 'E-greedy'
        self.result_list = []
        self.match_list = []
        self.s_id = None
        self.epsilon = Config.get_instance().egreedy_exploration

    def get_next_bot(self):
        """
        Chooses a random strategy (exploration) with probability epsilon
        and chooses the best known strategy with probability 1-epsilon
        :return: str
        """

        scores = {choice: 0 for choice in self.bot_list}

        # chooses randomly when epsilon is matched and in first match
        if random.random() < self.epsilon or self.history_length() == 0:
            return random.choice(self.bot_list)

        # count scores and selects greedily
        for match in range(self.history_length()):
            my_choice = self.my_choice(match)
            scores[my_choice] += self.match_result(match)

        best_strategy = max(scores, key=scores.get)
        #print best_strategy, scores
        return best_strategy

