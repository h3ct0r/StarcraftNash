import argparse
import result_parser
import sys
import matplotlib.pyplot as plt
from strategies.strategy_selector import StrategySelector

__author__ = 'Hector Azpurua'

DEBUG = False


class Main:
    def __init__(self):
        ss = StrategySelector()

        if DEBUG:
            print "DEBUG ON"
            self.strategy_a = ss.get_strategy('nash')
            self.strategy_a.set_id('A')
            self.strategy_b = ss.get_strategy('win_prev')
            self.strategy_b.set_id('B')
            self.input_results = 'results_demo/results.txt'
            self.matches = 100
        else:
            usr_input = self.get_arg()
            self.strategy_a = ss.get_strategy(usr_input['strategy_a'])
            self.strategy_a.set_id('A')
            self.strategy_b = ss.get_strategy(usr_input['strategy_b'])
            self.strategy_b.set_id('B')
            self.input_results = usr_input['input']
            self.matches = usr_input['matches']

        rp = result_parser.ResultParser(self.input_results)
        self.match_list = rp.get_match_list()

        self.match_index = 0
        self.match_history = []
        self.res_history = []
        self.run()

        print 'Result history of matches:', self.res_history
        print 'A) ', self.strategy_a.get_name().ljust(10), ':\t', \
            (self.res_history.count('A') * 100) / float(len(self.res_history)), '%'
        print 'B) ', self.strategy_b.get_name().ljust(10), ':\t', \
            (self.res_history.count('B') * 100) / float(len(self.res_history)), '%'

        if usr_input['plot']:
            self.plot_results()

        pass

    def get_arg(self):
        parser = argparse.ArgumentParser(description='Analisys of Starcraft Broodwar results file using several '
                                                     'techniques')
        parser.add_argument('-i', '--input', help='Input file of the results file', required=True)
        parser.add_argument('-a', '--strategy_a', help='The strategy used on the opponent A', required=True,
                            choices=StrategySelector.strategies.keys())
        parser.add_argument('-b', '--strategy_b', help='The strategy used on the opponent B', required=True,
                            choices=StrategySelector.strategies.keys())
        parser.add_argument('-m', '--matches', help='The number of matches to run', type=int, required=True)
        parser.add_argument('-p', '--plot', help='If this param is set, the results are plotted', required=False,
                            action='store_true')
        args = vars(parser.parse_args())
        return args

    def run(self):
        repeat_counter = 0

        for i in xrange(self.matches):
            self.strategy_a.set_result_list(self.res_history)
            self.strategy_a.set_match_list(self.match_history)
            self.strategy_b.set_result_list(self.res_history)
            self.strategy_b.set_match_list(self.match_history)

            bot_a = bot_b = ''

            while bot_a == bot_b:
                bot_a = self.strategy_a.get_next_bot()
                bot_b = self.strategy_b.get_next_bot()
                repeat_counter += 1
                if repeat_counter > 100:
                    print >> sys.stderr, 'The bots are the same after several retries...'
                    raise StopIteration('The bots are the same after several retries...')
            repeat_counter = 0

            print i+1, "Match", bot_a, 'vs', bot_b
            match = self.get_match(bot_a.lower(), bot_b.lower())

            winner = 'B'
            if match[0] == bot_a:
                winner = 'A'

            print "Winner:", winner, match, '\n'

            self.res_history.append(winner)
            self.match_history.append(match)
            pass

    def get_match(self, bot_a, bot_b):
        for i in xrange(self.match_index, len(self.match_list)):
            res = self.match_list[i]
            if (res[0].lower() == bot_a or res[0].lower() == bot_b) and \
                    (res[1].lower() == bot_a or res[1].lower() == bot_b):
                self.match_index = i
                return res
            pass
        pass

    def plot_results(self):
        counter = {
            'A': 0,
            'B': 0
        }
        data_a = []
        data_b = []
        d_range = []
        for i in xrange(len(self.res_history)):
            elem = self.res_history[i]
            counter[elem] += 1
            data_a.append(counter['A'])
            data_b.append(counter['B'])
            d_range.append(i)

        line_a,  = plt.plot(d_range, data_a, color='red', label=self.strategy_a.strategy_name)
        line_b, = plt.plot(d_range, data_b, color='blue', label=self.strategy_b.strategy_name)
        plt.legend(handles=[line_a, line_b])
        plt.grid(True)

        plt.xlabel('Match number')
        plt.ylabel('Accumulated wins')

        plt.show()
        pass

if __name__ == '__main__':
    Main()
