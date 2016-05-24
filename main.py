import argparse
import result_parser
import sys
import matplotlib.pyplot as plt
from strategies.strategy_selector import StrategySelector
import itertools

__author__ = 'Hector Azpurua'

DEBUG = True


class Main:
    def __init__(self):
        self.ss = StrategySelector()
        self.usr_input = self.get_arg()
        self.strategies_matches = []
        self.is_tournament = False
        self.input_results = []
        self.matches = []
        self.fig_counter = 0

        self.validate_params()

        if self.is_tournament:
            matches = list(itertools.combinations(StrategySelector.strategies.keys(), 2))
            for match in matches:
                aa = self.ss.get_strategy(match[0])
                aa.set_id('A')
                bb = self.ss.get_strategy(match[1])
                bb.set_id('B')
                self.strategies_matches.append((aa, bb))

        rp = result_parser.ResultParser(self.input_results)
        self.match_list = rp.get_match_list()

        self.result_dict = {}

        for i in xrange(len(self.strategies_matches)):
            strategy_a, strategy_b = self.strategies_matches[i]

            self.match_index = 0
            self.match_history = []
            self.res_history = []
            self.run(strategy_a, strategy_b)

            a_win_percentage = (self.res_history.count('A') * 100) / float(len(self.res_history))
            b_win_percentage = (self.res_history.count('B') * 100) / float(len(self.res_history))

            #print 'Result history of matches:', self.res_history
            print 'A) ', strategy_a.get_name().ljust(10), ':\t', a_win_percentage, '%'
            print 'B) ', strategy_b.get_name().ljust(10), ':\t', b_win_percentage, '%'

            if self.usr_input['plot']:
                self.plot_results(self.res_history, strategy_a, strategy_b)

            if strategy_a.get_name() not in self.result_dict:
                self.result_dict[strategy_a.get_name()] = {}
            if strategy_b.get_name() not in self.result_dict:
                self.result_dict[strategy_b.get_name()] = {}

            self.result_dict[strategy_a.get_name()][strategy_b.get_name()] = a_win_percentage
            self.result_dict[strategy_b.get_name()][strategy_a.get_name()] = b_win_percentage
        pass

        print self.result_dict
        if self.usr_input['plot']:
            plt.show()

    def validate_params(self):
        self.is_tournament = self.usr_input['tournament']
        if self.is_tournament is False:
            if self.usr_input['strategy_a'] is None or self.usr_input['strategy_b'] is None:
                print >> sys.stderr, 'Strategy for opponent A or B is missing, use -h to use Help to see the list' \
                                     'of possible parameters and combinations'
                sys.exit(1)

            strategy_a = self.ss.get_strategy(self.usr_input['strategy_a'])
            strategy_a.set_id('A')

            strategy_b = self.ss.get_strategy(self.usr_input['strategy_b'])
            strategy_b.set_id('B')

            self.strategies_matches.append((strategy_a, strategy_b))

        self.input_results = self.usr_input['input']
        self.matches = self.usr_input['matches']

    def run(self, strategy_a, strategy_b):
        repeat_counter = 0

        print '\n', strategy_a.get_name(), 'vs', strategy_b.get_name()

        for i in xrange(self.matches):
            strategy_a.set_result_list(self.res_history)
            strategy_a.set_match_list(self.match_history)
            strategy_b.set_result_list(self.res_history)
            strategy_b.set_match_list(self.match_history)

            bot_a = ''
            bot_b = ''

            while bot_a == bot_b:
                bot_a = strategy_a.get_next_bot()
                bot_b = strategy_b.get_next_bot()
                repeat_counter += 1
                if repeat_counter > 100:
                    print >> sys.stderr, 'The bots are the same after several retries...'
                    raise StopIteration('The bots are the same after several retries...')
            repeat_counter = 0

            if DEBUG:
                print i+1, "Match", bot_a, 'vs', bot_b, '(match index:', self.match_index, ')'

            match = self.get_match(bot_a.lower(), bot_b.lower())

            winner = 'B'
            if match[0] == bot_a:
                winner = 'A'

            if DEBUG:
                print "Winner:", winner, match, '\n'

            self.res_history.append(winner)
            self.match_history.append(match)
            pass

    def get_match(self, bot_a, bot_b):
        for i in xrange(self.match_index, len(self.match_list)):
            res = self.match_list[i]
            if (res[0].lower() == bot_a or res[0].lower() == bot_b) and \
                    (res[1].lower() == bot_a or res[1].lower() == bot_b):
                self.match_index = i + 1
                return res
            pass
        pass

    @staticmethod
    def get_arg():
        parser = argparse.ArgumentParser(
            description='Analisys of Starcraft Broodwar results file using several techniques')
        parser.add_argument(
            '-i', '--input', help='Input file of the results file', required=True)
        parser.add_argument(
            '-a', '--strategy_a', help='The strategy used on the opponent A, ignored if -t is set', required=False,
            choices=StrategySelector.strategies.keys())
        parser.add_argument(
            '-b', '--strategy_b', help='The strategy used on the opponent B, ignored if -t is set', required=False,
            choices=StrategySelector.strategies.keys())
        parser.add_argument(
            '-m', '--matches', help='The number of matches to run', type=int, required=True)
        parser.add_argument(
            '-p', '--plot', help='If this param is set, the results are plotted', required=False, action='store_true')
        parser.add_argument(
            '-t', '--tournament', help='If this param is set, all the techniques are tested against each other. '
                                       'The params -a -b are ignored', required=False, action='store_true')
        args = vars(parser.parse_args())
        return args

    def plot_results(self, res_history, strategy_a, strategy_b):
        plt.figure(self.fig_counter)
        counter = {
            'A': 0,
            'B': 0
        }
        data_a = []
        data_b = []
        d_range = []
        for i in xrange(len(res_history)):
            elem = res_history[i]
            counter[elem] += 1
            data_a.append(counter['A'])
            data_b.append(counter['B'])
            d_range.append(i)

        line_a,  = plt.plot(d_range, data_a, color='red', label=strategy_a.strategy_name)
        line_b, = plt.plot(d_range, data_b, color='blue', label=strategy_b.strategy_name)
        plt.legend(handles=[line_a, line_b], loc=2)
        plt.grid(True)

        plt.xlabel('Match number')
        plt.ylabel('Accumulated wins')

        plt.show(block=False)
        self.fig_counter += 1
        pass

if __name__ == '__main__':
    Main()
