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

    def __init__(self, strategy_name):
        """
        Initializes epsilon-greedy strategy selection method
        """

        StrategyBase.__init__(self, strategy_name)
        self.result_list = []
        self.match_list = []
        self.s_id = None
        self.epsilon = Config.get_instance().egreedy_exploration

    def calculate_scores(self):
        """
        Returns a dict {choice: score} with the total score attained
        by each choice
        :return:
        """
        #TODO: do this incrementally
        scores = {choice: 0 for choice in self.bot_list}

        for match in range(self.history_length()):
            my_choice = self.my_choice(match)
            scores[my_choice] += self.match_result(match)

        return scores

    def get_next_bot(self):
        """
        Chooses a random strategy (exploration) with probability epsilon
        and chooses the best known strategy with probability 1-epsilon
        :return: str
        """

        # chooses randomly when epsilon is matched and in first match
        if random.random() < self.epsilon or self.history_length() == 0:
            return random.choice(self.bot_list)

        # count scores and selects greedily
        scores = self.calculate_scores()

        best_strategy = max(scores, key=scores.get)
        #print best_strategy, scores
        return best_strategy


class EGreedyAverage(EGreedy):
    """
    Use the epsilon-greedy method for strategy selection:
    Chooses a random strategy (exploration) with probability epsilon
    and chooses the best known strategy (regarding average score)
    with probability 1-epsilon
    """

    def __init__(self):
        """
        Initializes epsilon-greedy strategy selection method
        """

        EGreedy.__init__(self)
        self.strategy_name = 'E-greedy-avg'
        self.epsilon = Config.get_instance().egreedy_exploration

        # overrides bot_list with bandit choices
        self.bot_list = Config.get_instance().get_bandit_choices()

    def get_next_bot(self):
        """
        Chooses a random strategy (exploration) with probability epsilon
        and chooses the best known strategy with probability 1-epsilon
        :return: str
        """

        # chooses randomly when epsilon is matched and in first match
        if random.random() < self.epsilon or self.history_length() == 0:
            return random.choice(self.bot_list)

        # count scores and selects greedily
        scores = self.calculate_scores()

        average_scores = {choice: float(score) / self.history_length() for choice, score in scores.iteritems()}
        best_strategy = max(average_scores, key=scores.get)
        #print best_strategy, scores
        return best_strategy


