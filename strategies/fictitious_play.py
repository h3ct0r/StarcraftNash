from strategy_base import StrategyBase

__author__ = 'Daniel Kneipp'


class FictitiousPlay(StrategyBase):

    def __init__(self):
        super(FictitiousPlay, self).__init__()
        self.strategy_name = 'Fictitious play'

    def get_next_bot(self):
        pass
