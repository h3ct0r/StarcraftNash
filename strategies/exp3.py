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

    print 'Warning: categorical_draw reached its end'
    return probabilities.keys()[-1]  # I think code should not reach here


class Exp3(StrategyBase):
    """
    Use the Exp3 method for strategy selection.
    The method is from the paper:
    Gambling in a rigged casino: the adversarial multi-armed bandit problem

    This implementation is an adaptation of:
    https://github.com/johnmyleswhite/BanditsBook/blob/master/python/algorithms/exp3/exp3.py
    """

    def __init__(self):
        """
        Initializes Exp3
        """

        StrategyBase.__init__(self)
        self.strategy_name = 'Exp3'

        # overrides bot_list with bandit choices
        self.bot_list = Config.get_instance().get_bandit_choices()

        self.gamma = Config.get_instance().exp3_gamma
        self.alpha = 1
        #self.weights = {choice: 1.0 for choice in self.bot_list}
        self.weights = {choice: 0.0 for choice in self.bot_list}

    def prepare(self):
        """
        Erases statistics
        :return:
        """
        #self.weights = {choice: 1.0 for choice in self.bot_list}
        self.weights = {choice: 0.0 for choice in self.bot_list}

    def prob_factor(self, weight):
        """
        Uses the probability factor formula of Exp3
        :param weight:
        :return:
        """
        return (1 + self.alpha) ** weight
    def get_next_bot(self):
        """
        Selects a bot according to the Exp3 algorithm
        :return:
        """
        # updates weights with result from previous match
        self.update()

        # performs selection
        n_arms = len(self.weights)
        #total_weight = sum(self.weights.values())
        total_prob_factor = sum(self.prob_factor(w) for w in self.weights.values())

        probs = {choice: 0.0 for choice in self.bot_list}

        for arm in self.bot_list:
            #probs[arm] = (1 - self.gamma) * (self.weights[arm] / total_weight)
            #probs[arm] += self.gamma * (1.0 / float(n_arms))
            pre_prob = self.prob_factor(self.weights[arm]) / total_prob_factor

            # mixes pre_prob with an uniform distribution
            # gamma is the 'fraction' of uniform that gets mixed in
            probs[arm] = (1 - self.gamma) * pre_prob + self.gamma / float(n_arms)

        return categorical_draw(probs)

    def update(self):
        """
        Updates the weight of the chosen arm according to the received reward
        :return:
        """
        if self.my_choice(-1) is None:  # skips on first match
            return

        chosen_arm = self.my_choice(-1)
        reward = self.match_result(-1)

        n_arms = len(self.weights)
        #total_weight = sum(self.weights.values())
        total_prob_factor = sum(self.prob_factor(w) for w in self.weights.values())

        # rescales reward to [0,1], the original is either -1 or 1
        scaled_rwd = (reward + 1) / 2

        pre_prob = self.prob_factor(self.weights[chosen_arm]) / total_prob_factor

        prob_of_chosen_arm = (1 - self.gamma) * pre_prob + self.gamma / n_arms
        #prob_of_chosen_arm = (1 - self.gamma) * (self.weights[chosen_arm] / total_weight) \
        #                     + self.gamma * (1.0 / float(n_arms))

        #x = reward / prob_of_chosen_arm  # probs[chosen_arm]
        mixed_rwd = (self.gamma / n_arms) * (reward / prob_of_chosen_arm)   # probs[chosen_arm]

        #growth_factor = math.exp((self.gamma / n_arms) * x)
        #self.weights[chosen_arm] *= growth_factor
        self.weights[chosen_arm] += mixed_rwd


