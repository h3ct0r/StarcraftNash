import sys
import time
import config
import random
import argparse
import itertools
import result_parser
import strategies.strategy_base
import matplotlib.pyplot as plt
from strategies.strategy_selector import StrategySelector


__author__ = 'Hector Azpurua'

DEBUG = True

# TODO: verbose via command line
# TODO: read cross table


class Main:
    def __init__(self):
        self.result_parser = None
        self.config = config.Config.get_instance()
        self.strategy_selector = StrategySelector()
        self.usr_input = self.get_arg()
        self.game_matches = []              # matches between strategy selectors (list of tuples)
        self.is_tournament = False          # defines matches between all strategy selectors
        self.input_results = None           # file with pool of matches between strategies (not strategy selectors!)
        self.matches = 0                    # number of matches between strategy selectors
        self.fig_counter = 0                # number of figures for plotting
        self.repetitions = 1                # number of repetitions of matches

        # validates params and configures internal variables (including game_matches)
        self.validate_params()

        self.bot_match_list = self.result_parser.get_match_list()

        # sets possible players' selections from config object
        strategies.strategy_base.StrategyBase.bot_list = self.config.bots.keys()

        self.result_list = []

        for rep in xrange(self.repetitions):
            print 'Repetition', rep+1, 'of', self.repetitions, '...'
            # shuffles match list if required
            if self.config.shuffle_match_list:
                print 'Shuffling match list...'
                random.shuffle(self.bot_match_list)

            single_result_dict = {}   # stores players' percent of victories
            for i in xrange(len(self.game_matches)):
                player_a, player_b = self.game_matches[i]

                self.match_index = 0
                self.match_history = []
                self.res_history = []
                self.run(player_a, player_b)

                a_win_percentage = (self.res_history.count('A') * 100) / float(len(self.res_history))
                b_win_percentage = (self.res_history.count('B') * 100) / float(len(self.res_history))

                if self.config.verbose:
                    print 'A) ', player_a.get_name().ljust(13), ':\t', a_win_percentage, '%'
                    print 'B) ', player_b.get_name().ljust(13), ':\t', b_win_percentage, '%'

                if self.usr_input['plot']:
                    self.plot_results(self.res_history, player_a, player_b)

                if player_a.get_name() not in single_result_dict:
                    single_result_dict[player_a.get_name()] = {}
                if player_b.get_name() not in single_result_dict:
                    single_result_dict[player_b.get_name()] = {}

                single_result_dict[player_a.get_name()][player_b.get_name()] = a_win_percentage
                single_result_dict[player_b.get_name()][player_a.get_name()] = b_win_percentage
            print  # adds newline
            self.result_list.append(single_result_dict)
        pass

        print 'Getting the mean win percentages of %d repetitions...' % self.repetitions
        self.result_dict = Main.get_mean_percentages(self.result_list)
        if self.config.verbose:
            print 'Original results:', self.result_list, '\n'
            print 'Mean results:', self.result_dict

        if self.usr_input['plot']:
            plt.show()

        if 'excel' in self.usr_input and self.usr_input['excel'] is not None:
            self.generate_excel_results()

    @staticmethod
    def get_mean_percentages(win_list):
        """
        Get the mean values of a list of dicts with the percentage of wins
        :param win_list:
        :return:
        """
        if win_list is None or len(win_list) <= 0:
            return None

        repetitions = len(win_list)
        mean_values = {}

        for win_dict in win_list:
            for key, value in win_dict.items():
                if key not in mean_values:
                    mean_values[key] = {}

                for key2, value2 in value.items():
                    if key2 not in mean_values[key]:
                        mean_values[key][key2] = 0
                    mean_values[key][key2] += value2

        for key, value in mean_values.items():
            for key2, value2 in value.items():
                mean_values[key][key2] /= repetitions

        return mean_values

    def validate_params(self):
        """
        Validates user input of parameters and
        configures several internal variables, such as the match list!

        :return:
        """

        if 'config_file' in self.usr_input and self.usr_input['config_file'] is not None:
            self.config.parse(self.usr_input['config_file'])
            self.strategy_selector.update_strategies(self.config.get_bots())

        # sets random seed
        random_seed = None
        if self.config.random_seed is not None:
            random_seed = self.config.random_seed

        # overrides file seed if there is one via command line
        if self.usr_input['random_seed'] is not None:
            random_seed = self.usr_input['random_seed']

        # finally sets random seed
        if random_seed is not None:
            random.seed(random_seed)
            print 'Random seed set to %d' % random_seed

        if self.usr_input['repetitions'] is not None:
            self.repetitions = self.usr_input['repetitions']

        self.is_tournament = self.usr_input['tournament']

        self.input_results = self.usr_input['input']
        self.matches = self.usr_input['matches']

        self.result_parser = result_parser.ResultParser(self.input_results)
        self.strategy_selector.set_unique_choices(self.result_parser.get_unique_opponents())

        if self.is_tournament:
            players = StrategySelector.strategies.keys()    # players are the strategy (bot) selectors

            if self.config.get_is_config_updated():
                players += self.config.get_bots()
            else:
                players += self.strategy_selector.get_unique_choices()

            # override players' list with config if existent
            if len(self.config[self.config.PLAYERS]) > 0:
                players = self.config[self.config.PLAYERS]

            players = list(set(players))

            print 'Tournament participants: %s' % ', '.join(players)

            matches = list(itertools.combinations(players, 2))  # generates match list given the list of players
            for match in matches:
                aa = self.strategy_selector.get_strategy(match[0])
                aa.set_id('A')
                bb = self.strategy_selector.get_strategy(match[1])
                bb.set_id('B')
                self.game_matches.append((aa, bb))
        else:
            if self.usr_input['player_a'] is None or self.usr_input['player_b'] is None:
                print >> sys.stderr, 'Strategy for opponent A or B is missing, use -h to use Help to see the list' \
                                     'of possible parameters and combinations'
                sys.exit(1)

            all_players = StrategySelector.strategies.keys() + self.result_parser.get_unique_opponents()
            if self.usr_input['player_a'] not in all_players or self.usr_input['player_b'] not in all_players:
                print >> sys.stderr, \
                    'Strategy for opponent A or B are invalid, the valid strategies are', all_players
                sys.exit(1)

            player_a = self.strategy_selector.get_strategy(self.usr_input['player_a'])
            player_a.set_id('A')

            player_b = self.strategy_selector.get_strategy(self.usr_input['player_b'])
            player_b.set_id('B')

            self.game_matches.append((player_a, player_b))

    def run(self, player_a, player_b):
        """
        Run the tournament between 2 strategies for a number of matches

        :param player_a:
        :param player_b:
        :return:
        """
        repeat_counter = 0

        #if self.config.verbose:
        print player_a.get_name(), '-vs-', player_b.get_name()

        for i in xrange(self.matches):
            player_a.set_result_list(self.res_history)
            player_a.set_match_list(self.match_history)
            player_b.set_result_list(self.res_history)
            player_b.set_match_list(self.match_history)

            bot_a = player_a.get_next_bot()
            bot_b = player_b.get_next_bot()

            while bot_a == bot_b:
                bot_a = player_a.get_next_bot()
                bot_b = player_b.get_next_bot()
                repeat_counter += 1
                if repeat_counter > 100:
                    if self.config.verbose:
                        print 'The bots are the same after several retries @ match', i
                     #raise StopIteration('The bots are the same after several retries...')
            repeat_counter = 0

            if self.config.verbose:
                print i+1, "Match", bot_a, 'vs', bot_b, '(match index:', self.match_index, ')'

            # if bots are equal, do not search for a match in the pool 'coz it does not exist
            if bot_a == bot_b:
                print "Same bots competing, winner will be chosen randomly"
                match = (bot_a, bot_b)
            else:
                match = self.get_match(bot_a.lower(), bot_b.lower())

            if self.config.verbose:
                print 'Match:', match

            winner = 'A' if match[0] == bot_a else 'B'
            if bot_a == bot_b:  # necessary check if bots are the same
                winner = 'A' if random.random() < .5 else 'B'

            if self.config.verbose:
                print "Winner:", winner, match, '\n'

            self.res_history.append(winner)
            self.match_history.append(match)
            pass

    def get_match(self, bot_a, bot_b):
        """
        Given a list of matches, select a new match between the strategies of BotA and BotB using an index

        :param bot_a:
        :param bot_b:
        :return:
        """
        match = None
        if self.match_index >= len(self.bot_match_list)-1:
            print >> sys.stderr, 'The match index (' + str(self.match_index) + \
                                 ') is equal or superior to the number of matches (' + str(len(self.bot_match_list)) + ')'
            raise StopIteration('Match index have passed the match number, please select a small -m value')

        for i in xrange(self.match_index, len(self.bot_match_list)):
            res = self.bot_match_list[i]
            if (res[0].lower() == bot_a or res[0].lower() == bot_b) and \
                    (res[1].lower() == bot_a or res[1].lower() == bot_b):
                self.match_index = i + 1
                match = res
                break
            pass
        pass

        if match is None:
            self.match_index = 0
            if self.config.verbose:
                print >> sys.stderr, 'Cannot find a match between "' + bot_a + '" and "' + bot_b + '" after the index (' + \
                                     str(self.match_index) + ').\nWill resume from beginning'

            return self.get_match(bot_a, bot_b)
            #raise StopIteration('Cannot find a match after the match index defined, please select a small -m value')

        return match

    @staticmethod
    def get_arg():
        """
        Get the arguments of this program

        :return:
        """
        parser = argparse.ArgumentParser(
            description='Strategy selection in StarCraft'
        )

        parser.add_argument(
            '-i', '--input', help='Input file of the results file', required=True
        )

        parser.add_argument(
            '-a', '--player_a', help='The strategy used on the opponent A, ignored if -t is set', required=False
        )

        parser.add_argument(
            '-b', '--player_b', help='The strategy used on the opponent B, ignored if -t is set', required=False
        )

        parser.add_argument(
            '-c', '--config_file', help='File with experiment configurations',
            required=False, type=str,
        )

        parser.add_argument(
            '-m', '--matches', help='The number of matches to run', type=int, required=True
        )

        parser.add_argument(
            '-p', '--plot', help='If this param is set, the results are plotted',
            required=False, action='store_true'
        )

        parser.add_argument(
            '-s', '--random-seed', help='Random seed for experiments',
            required=False, type=int
        )

        parser.add_argument(
            '-r', '--repetitions', help='Number of repetitions for the tournament/matches',
            required=False, type=int
        )

        parser.add_argument(
            '-e', '--excel', help='Outputs results to a .xls file given by this parameter',
            required=False
        )

        parser.add_argument(
            '-t', '--tournament', help='If this param is set, all the techniques are tested against each other. '
                                       'The params -a -b are ignored', required=False, action='store_true'
        )

        args = vars(parser.parse_args())
        return args

    def plot_results(self, res_history, player_a, player_b):
        """
        Plot the results of the matches given a list of wins and losses

        :param res_history:
        :param player_a:
        :param player_b:
        :return:
        """
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

        line_a,  = plt.plot(d_range, data_a, color='red', label=player_a.strategy_name)
        line_b, = plt.plot(d_range, data_b, color='blue', label=player_b.strategy_name)
        #plt.legend(handles=[line_a, line_b], loc=2)
        plt.legend(loc=2)
        plt.grid(True)

        plt.xlabel('Match number')
        plt.ylabel('Accumulated wins')

        plt.show(block=False)
        self.fig_counter += 1
        pass

    def generate_excel_results(self):
        import xlsxwriter

        excel_filename = self.usr_input['excel']

        print 'Generating excel results to file:', excel_filename

        strategy_list_srt = sorted(self.result_dict.keys())
        workbook = xlsxwriter.Workbook(excel_filename)

        worksheet = workbook.add_worksheet()

        element_count = len(strategy_list_srt)

        format1 = workbook.add_format()
        format1.set_pattern(1)
        format1.set_bg_color('yellow')

        i = 0
        for id1 in strategy_list_srt:
            j = 0
            for id2 in strategy_list_srt:

                worksheet.write(0, 1+i, id1)
                worksheet.write(1+i, 0, id1)

                if id1 == id2:
                    worksheet.write(1 + i, 1+j, '', format1)

                elif id2 in self.result_dict[id1]:
                    total = self.result_dict[id1][id2]  # str(self.result_dict[id1][id2]) + '%'

                    if self.config.verbose:
                        print id1, ":", id2, total

                    worksheet.write(1 + i, 1+j, total)
                j += 1
                pass

            i += 1
            if self.config.verbose:
                print i, "/", element_count

            pass

        workbook.close()
        print 'DONE.'

if __name__ == '__main__':
    Main()
