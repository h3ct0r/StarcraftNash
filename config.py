import os
import xml.etree.ElementTree as ET
import math

__author__ = 'Anderson Tavares'


def str_to_bool(value):
    return value.lower() == 'true'


class Config(object):
    """
    Class that handles configurations of an experiment
    """

    instance = None
    default_bots = {"Skynet": .33, "Xelnaga": .33, "NUSBot": .33}

    # parameter names (also tag names in .xml)
    BOTS = 'bots'
    PLAYERS = 'players'
    SCORECHART_FILE = 'scorechart-file'
    # IS_TOURNAMENT = 'tournament'

    E_GREEDY_EXPLORATION = 'egreedy-exploration'
    E_NASH_EXPLOITATION = 'enash-exploitation'
    SHUFFLE_MATCH_LIST = 'shuffle-match-list'
    RANDOM_SEED = 'random-seed'
    REPETITIONS = 'repetitions'
    NUM_MATCHES = 'num-matches'
    MATCH_POOL_FILE = 'match-pool-file'
    ROUND_ROBIN = 'round-robin'
    OUTPUT_SPREADSHEET = 'output-spreadsheet'
    OUTPUT_INTERMEDIATE = 'output-intermediate'
    VERBOSE = 'verbose'
    PLOT = 'plot'

    # xml tag names
    CHOICES_FIELD = 'choices'
    PARAMETERS_FIELD = 'parameters'

    @staticmethod
    def get_instance():
        """
        Returns the (singleton) instance of Config object
        :return: Config
        """
        if Config.instance is None:
            Config.instance = Config()
        return Config.instance

    def __init__(self, ):
        # dir of config file needed coz' path to server is relative
        # self.cfgdir = os.path.dirname(os.path.realpath(cfgpath))

        # stores values of parameters (initialized with defaults)
        self.data = {
            self.BOTS: self.default_bots,       # dict of choices (and their nash probabilities)
            self.PLAYERS: [],                   # list of players
            self.E_GREEDY_EXPLORATION: .1,
            self.E_NASH_EXPLOITATION: .1,
            self.VERBOSE: True,
            self.SHUFFLE_MATCH_LIST: False,
            self.RANDOM_SEED: None,
            self.REPETITIONS: 1,
            self.NUM_MATCHES: 100,
            self.ROUND_ROBIN: True,
            self.SCORECHART_FILE: 'config/scorechart_fortress.csv',
            self.MATCH_POOL_FILE: 'results_demo/fortress1000.txt',
            self.OUTPUT_SPREADSHEET: None,
            self.OUTPUT_INTERMEDIATE: 'intermediate',
            self.PLOT: False,
        }

        # stores type conversions for parameters
        self.parser = {
            self.E_GREEDY_EXPLORATION: float,
            self.E_NASH_EXPLOITATION: float,
            self.VERBOSE: str_to_bool,
            self.SHUFFLE_MATCH_LIST: str_to_bool,
            self.RANDOM_SEED: int,
            self.REPETITIONS: int,
            self.NUM_MATCHES: int,
            self.ROUND_ROBIN: str_to_bool,
            self.SCORECHART_FILE: str,
            self.MATCH_POOL_FILE: str,
            self.OUTPUT_SPREADSHEET: str,
            self.OUTPUT_INTERMEDIATE: str,
            self.PLOT: str_to_bool
        }

    def get_bots(self):
        return self.data[self.BOTS]

    def __getitem__(self, item):
        return self.get(item)

    def __getattr__(self, item):
        return self.get(item.replace('_', '-'))

    def get(self, item):
        """
        Retuns a configuration parameter
        :param item: str
        :return:
        """
        if item not in self.data:
            raise KeyError("Item '%s' not found in config object." % item)
        return self.data[item]

    # def _parse_path(self, value):
    #     return os.path.join(
    #         self.cfgdir, os.path.expanduser(value)
    #     )

    def get_is_config_updated(self):
        return self.get(self.BOTS) != self.default_bots  #is_config_updated

    def parse(self, cfgpath=None):
        print 'Parsing file:', cfgpath
        cfgtree = ET.parse(cfgpath)

        for element in cfgtree.getroot():
            if element.tag == self.CHOICES_FIELD:
                self.data[self.BOTS] = {x.get('name'): float(x.get('nashprob')) for x in element}

            elif element.tag == self.PLAYERS:
                self.data[self.ROUND_ROBIN] = True
                self.data[self.PLAYERS] = [x.get('name') for x in element]

            elif element.tag == self.PARAMETERS_FIELD:
                for param in element:
                    self.data[param.tag] = self.parser[param.tag](param.get('value'))

            # default is to assign 'value' attribute to data indexed by tag
            else:
                self.data[element.tag] = self.parser[element.tag](element.get('value'))

        #if self.bots != self.default_bots:
        #    self.is_config_updated = True

        #print 'Bot definition updated by config file:', self.bots

