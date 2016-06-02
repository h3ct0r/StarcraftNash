import os
import xml.etree.ElementTree as ET
import math

__author__ = 'Anderson Tavares'


def str_to_bool(value):
    return value.lower() == 'true'


class Config(object):

    instance = None
    is_config_updated = False
    default_bots = {"Skynet": .33, "Xelnaga": .33, "NUSBot": .33}

    @staticmethod
    def get_instance():
        """
        Returns the (singleton) instance of Config object
        """
        if Config.instance is None:
            Config.instance = Config()
        return Config.instance

    """
    Class that handles configurations of an experiment
    """
    def __init__(self, ):
        # dir of config file needed coz' path to server is relative
        # self.cfgdir = os.path.dirname(os.path.realpath(cfgpath))

        self.bots = self.default_bots

    def get_bots(self):
        return self.bots

    def _parse_path(self, value):
        return os.path.join(
            self.cfgdir, os.path.expanduser(value)
        )

    def get_is_config_updated(self):
        return self.is_config_updated

    def parse(self, cfgpath=None):
        print 'Parsing file:', cfgpath
        cfgtree = ET.parse(cfgpath)

        for element in cfgtree.getroot():
            if element.tag == 'bots':
                self.bots = {x.get('name'): float(x.get('nashprob')) for x in element}

        if self.bots != self.default_bots:
            self.is_config_updated = True

        print 'Bot definition updated by config file:', self.bots

