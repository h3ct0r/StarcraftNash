from abc import ABCMeta, abstractmethod

__author__ = 'Hector Azpurua'


class StrategyBase(object):
    __metaclass__ = ABCMeta

    # codes for possible match results
    DEFEAT = -1
    DRAW = 0
    VICTORY = 1

    # static list so that every strategy can use the same bots
    # (the list is initialized here but can be changed at will with set_bot_list)
    bot_list = ["Skynet", "Xelnaga", "CruzBot"]

    def __init__(self):
        self.strategy_name = 'StrategyBase'
        self.result_list = []
        self.match_list = []
        self.s_id = None

    def set_bot_list(self, b_list):
        self.bot_list = b_list

    def set_id(self, s_id):
        self.s_id = s_id

    def get_id(self):
        return self.s_id

    def get_name(self):
        return self.strategy_name

    @abstractmethod
    def get_next_bot(self):
        return ''

    def get_match_list(self):
        return self.match_list

    def set_match_list(self, match_list):
        self.match_list = match_list

    def get_result_list(self):
        return self.result_list

    def set_result_list(self, result_list):
        self.result_list = result_list

    def calculate_score_table(self):
        """
        Returns a table with scores of each choice against each other
        Each victory is +1; loss is -1.
        A match with same participants does not change score
        :return: dict(dict) - usage: table[me][adversary]
        """
        # initializes scores of each bot against each other as zero
        # usage: table[me][adversary]
        table = {mine: {opponent: 0 for opponent in self.bot_list} for mine in self.bot_list}

        # updates win_count according to previous matches
        for winner_bot, loser_bot in self.match_list:
            # res = self.result_list[i]
            # winner_bot, loser_bot = self.match_list[i]

            table[winner_bot][loser_bot] += 1
            table[loser_bot][winner_bot] -= 1

        return table

    def history_length(self):
        """
        Returns the number of matches played (and recorded) so far
        :return: int
        """
        return len(self.match_list)

    def opponent_choice(self, match_index):
        """
        Returns the name of opponent choice in the required match
        :param match_index: index (zero-based) of match,
        can be negative: -1 for previous (most recent) match, -2 for second-last and so on
        :return:str
        """
        if len(self.match_list) == 0:
            return None

        res = self.result_list[match_index]

        winner_choice, loser_choice = self.match_list[match_index]

        if res.upper() == 'A':
            bot_a = winner_choice
            bot_b = loser_choice
        else:
            bot_a = loser_choice
            bot_b = winner_choice

        # opponent choice is B if I am A and vice-versa
        return bot_b if self.s_id == 'A' else bot_a

    def my_choice(self, match_index):
        """
        Returns the name of my choice in the required match
        :param match_index: index (zero-based) of match,
        can be negative: -1 for previous (most recent) match, -2 for second-last and so on
        :return:str
        """
        if len(self.match_list) == 0:
            return None

        res = self.result_list[match_index]

        winner_choice, loser_choice = self.match_list[match_index]

        if res.upper() == 'A':
            bot_a = winner_choice
            bot_b = loser_choice
        else:
            bot_a = loser_choice
            bot_b = winner_choice

        # opponent choice is B if I am A and vice-versa
        return bot_a if self.s_id == 'A' else bot_b

    def winner_choice(self, match_index):
        """
        Returns the name of the choice that won the required match
        or None if it was a draw
        :param match_index: index (zero-based) of match,
        can be negative: -1 for previous (most recent) match, -2 for second-last and so on
        :return:str
        """

        winner_choice, loser_choice = self.match_list[match_index]
        return winner_choice

    def match_result(self, match_index):
        """
        Returns a code for the result of the required match: DRAW = 0, VICTORY = 1 or DEFEAT = -1
        :param match_index: index (zero-based) of match,
        can be negative: -1 for previous (most recent) match, -2 for second-last and so on
        :return:int
        """

        if self.winner_choice(match_index) is None:
            return self.DRAW

        #elif self.my_choice(match_index) == self.winner_choice(match_index):
        #    return self.VICTORY

        elif self.get_id() == self.result_list[match_index]:
            return self.VICTORY

        else:
            return self.DEFEAT

