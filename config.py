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
    def __init__(self, ):
        # dir of config file needed coz' path to server is relative
        # self.cfgdir = os.path.dirname(os.path.realpath(cfgpath))

        self.bots = {"Skynet": .33, "Xelnaga": .33, "NUSBot": .33}



    def _parse_path(self, value):
        return os.path.join(
            self.cfgdir, os.path.expanduser(value)
        )

    def parse(self, cfgpath=None):

        cfgtree = ET.parse(cfgpath)

        for element in cfgtree.getroot():
            if element.tag == 'bots':
                self.bots = {x['name']: float(x['nashprob']) for x in element}

