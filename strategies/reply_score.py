from strategy_base import StrategyBase
from config import Config
import scorechart
import random

__author__ = 'Anderson Tavares'


class ReplyLast(StrategyBase):
    """
    Selects the bot that would beat last opponent choice, querying a score chart
    """

    def __init__(self):
        StrategyBase.__init__(self)
        self.strategy_name = 'Reply-score'

        # loads score chart from file
        self.score_chart = scorechart.from_file(
            Config.get_instance().get(Config.SCORECHART_FILE)
        )
        # self.result_list = []
        # self.match_list = []
        # self.s_id = None

    def get_next_bot(self):

        # finds opponent's last choice
        opponent_choice = self.opponent_choice(-1)

        # no history present or could not count victories, chooses randomly
        if opponent_choice is None:
            return random.choice(self.bot_list)

        # responds with opponent's nemesis, i.e the one that makes it perform worst
        return min(self.score_chart[opponent_choice], key=self.score_chart[opponent_choice].get)

