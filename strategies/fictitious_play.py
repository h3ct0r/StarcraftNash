from strategy_base import StrategyBase
from config import Config
import scorechart

__author__ = 'Daniel Kneipp'


class FictitiousPlay(StrategyBase):

    def __init__(self, strategy_name, config_name):
        super(FictitiousPlay, self).__init__(strategy_name)

        config = Config.get_instance()

        if config_name is None:
            raise Exception('Fictitious Play must have a configuration specified at the initialization time')

        self.set_config_name(config_name)

        # read score chart from a file
        self.score_chart = scorechart.from_file(
            config.get(Config.SCORECHART_FILE)
        )

        # get weights
        self.initial_weights = config.get(self.config_name)[Config.FICTITIOUS_INITIAL_WEIGHTS]
        self.running_weights = config.get(self.config_name)[Config.FICTITIOUS_RUNNING_WEIGHTS]

        # set counters
        # Note: self.bot_list can't be used here because it isn't initialized from the config file yet
        self.opponent_choice_counter = {choice_name: self.initial_weights[choice_name] for choice_name in
                                        config.get_bots()}
        self.count_sum = sum([x for _, x in self.opponent_choice_counter.items()])

    def get_next_bot(self):
        # finds opponent's last choice
        opponent_choice = self.opponent_choice(-1)

        # if there is a history of opponent's choices
        if opponent_choice is not None:
            # update counter
            self.opponent_choice_counter[opponent_choice] += self.running_weights[opponent_choice]
            self.count_sum += self.running_weights[opponent_choice]

        # update beliefs
        opponent_choice_beliefs = [(k, v/self.count_sum) for k, v in self.opponent_choice_counter.items()]

        # retrieve the most chosen bot
        likely_opponent_bot = max(opponent_choice_beliefs, key=lambda belief: belief[1])[0]

        # get the best response
        response = min(self.score_chart[likely_opponent_bot], key=self.score_chart[likely_opponent_bot].get)
        return response
