import argparse
import result_parser
from strategies.nash import Nash

__author__ = 'Hector Azpurua'

strategies_dict = {
    'nash': Nash(),
    'max_win_prev': None,
    'win_prev': None,
    'skynet': None,
    'xelnaga': None,
    'nusbot': None
}


class Main:
    def __init__(self):
        usr_input = self.get_arg()

        self.strategy_a = strategies_dict[usr_input['strategy_a']]
        self.strategy_b = strategies_dict[usr_input['strategy_b']]
        self.input_results = usr_input['input']

        rp = result_parser.ResultParser(self.input_results)
        print rp.get_match_list()
        pass

    def get_arg(self):
        parser = argparse.ArgumentParser(description='Analisys of Starcraft Broodwar results file using several '
                                                     'techniques')
        parser.add_argument('-i', '--input', help='Input file of the results file', required=True)
        parser.add_argument('-a', '--strategy_a', help='The strategy used on the opponent A', required=True,
                            choices=strategies_dict.keys())
        parser.add_argument('-b', '--strategy_b', help='The strategy used on the opponent B', required=True,
                            choices=strategies_dict.keys())
        args = vars(parser.parse_args())
        return args

if __name__ == '__main__':
    Main()