from strategy_base import StrategyBase
import random
import math
from config import Config

__author__ = 'Anderson'


def categorical_draw(probabilities):
    """
    Selects an option with a roulette-like process
    :param probabilities:
    :return:
    """
    z = random.random()
    cum_prob = 0.0

    for choice, prob in probabilities.iteritems():
        cum_prob += prob
        if cum_prob > z:
            return choice

    return probabilities.keys()[-1]  # I think code should not reach here


class Exp3(StrategyBase):
    """
    Use the Exp3 method for strategy selection.
    The method is from the paper:
    Gambling in a rigged casino: the adversarial multi-armed bandit problem

    This implementation is an adaption of:
    https://github.com/johnmyleswhite/BanditsBook/blob/master/python/algorithms/exp3/exp3.py
    """

    def __init__(self):
        """
        Initializes epsilon-greedy strategy selection method
        """

        StrategyBase.__init__(self)
        self.strategy_name = 'Exp3'
        self.gamma = 0.1
        self.weights = {choice: 1.0 for choice in self.bot_list}

    def get_next_bot(self):
        """
        Selects a bot according to the Exp3 algorithm
        :return:
        """
        n_arms = len(self.weights)
        total_weight = sum(self.weights.values())

        probs = {choice: 0.0 for choice in self.bot_list}

        for arm in self.bot_list:
            probs[arm] = (1 - self.gamma) * (self.weights[arm] / total_weight)
            probs[arm] += self.gamma * (1.0 / float(n_arms))

        return categorical_draw(probs)

    def update(self, chosen_arm, reward):
        n_arms = len(self.weights)
        total_weight = sum(self.weights.values())

        probs = {choice: 0.0 for choice in self.bot_list}

        for arm in self.bot_list:
            probs[arm] = (1 - self.gamma) * (self.weights[arm] / total_weight)
            probs[arm] += self.gamma * (1.0 / float(n_arms))

        x = reward / probs[chosen_arm]

        growth_factor = math.exp((self.gamma / n_arms) * x)

        self.weights[chosen_arm] *= growth_factor


