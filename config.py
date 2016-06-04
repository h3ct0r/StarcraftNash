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

    E_GREEDY_EXPLORATION_FIELD = 'egreedy-exploration'
    E_NASH_EXPLOITATION_FIELD = 'enash-exploitation'

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

        self.bots = self.default_bots
        self.verbose = False
        self.enash_exploitation = 0.1
        self.egreedy_exploration = 0.1

    def get_bots(self):
        return self.bots

    def _parse_path(self, value):
        return os.path.join(
            self.cfgdir, os.path.expanduser(value)
        )

    def get_is_config_updated(self):
        return self.bots != self.default_bots  #is_config_updated

    def parse(self, cfgpath=None):
        print 'Parsing file:', cfgpath
        cfgtree = ET.parse(cfgpath)

        for element in cfgtree.getroot():
            if element.tag == self.CHOICES_FIELD:
                self.bots = {x.get('name'): float(x.get('nashprob')) for x in element}

            elif element.tag == self.PARAMETERS_FIELD:
                for param in element:
                    if param.tag == self.E_GREEDY_EXPLORATION_FIELD:
                        self.egreedy_exploration = float(param.get('value'))

                    if param.tag == self.E_NASH_EXPLOITATION_FIELD:
                        self.enash_exploitation = float(param.get('value'))

        #if self.bots != self.default_bots:
        #    self.is_config_updated = True

        #print 'Bot definition updated by config file:', self.bots

