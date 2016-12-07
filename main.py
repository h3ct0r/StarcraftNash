import os
import csv
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
# TODO: set seed only for shuffling (because other random calls may disrupt repeatability)


class Main:
    def __init__(self):
        self.result_parser = None
        self.config = config.Config.get_instance()
        self.strategy_selector = StrategySelector()
        self.usr_input = self.get_arg()
        self.game_matches = []  # matches between strategy selectors (list of tuples)
        # self.config.round_robin = False          # defines matches between all strategy selectors
        # self.config.num_matches = 0                    # number of matches between strategy selectors
        self.fig_counter = 0  # number of figures for plotting

        # validates params and configures internal variables (including game_matches)
        self.validate_params()

        self.bot_match_list = self.result_parser.get_match_list()

        # sets possible players' selections from config object
        strategies.strategy_base.StrategyBase.bot_list = self.config.bots.keys()

        self.result_list = []

        for rep in xrange(self.config.repetitions):
            print 'Repetition', rep + 1, 'of', self.config.repetitions, '...'

            # recreate objects of the strategies to make the repetitions independent
            self.recreate_strategies()

            # shuffles match list if required
            if self.config.shuffle_match_list == True:
                print 'Shuffling match list...'
                random.shuffle(self.bot_match_list)

            single_result_dict = {}  # stores players' percent of victories
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

                if self.config.plot:
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

        print 'Getting the mean win percentages of %d repetitions...' % self.config.repetitions
        self.result_dict = Main.get_mean_percentages(self.result_list)

        if self.config.output_intermediate:
            output_folder = self.config.output_intermediate
            print 'Outputting CSV files to:', output_folder
            Main.output_csv_results(output_folder, self.result_list)

        if self.config.verbose:
            print 'Original results:', self.result_list, '\n'
            print 'Mean results:', self.result_dict

        if self.usr_input['plot']:
            plt.show()

        if self.config.output_spreadsheet is not None:
            self.generate_excel_results()

    def recreate_strategies(self):
        for i, match in enumerate(self.game_matches):
            aa, bb = match

            new_aa = StrategySelector.recreate_strategy(aa)
            new_bb = StrategySelector.recreate_strategy(bb)
            self.game_matches[i] = (new_aa, new_bb)

    @staticmethod
    def output_csv_results(output, win_list):
        """
        Outout results in CSV of a list of dicts with the percentage of wins
        :param output:
        :param win_list:
        :return:
        """
        if output is None or win_list is None or len(win_list) <= 0:
            return None

        if not os.path.exists(output):
            os.makedirs(output)

        s_keys = win_list[0].keys()

        overwrites_experiment = False
        overwrites_suffix = str(int(round(time.time() * 1000)))

        for i in xrange(len(win_list)):
            f = None
            rep_index = str(i + 1)
            try:
                filename = 'rep_' + rep_index + '.csv'
                if os.path.isfile(os.path.join(output, filename)):
                    overwrites_experiment = True

                if overwrites_experiment:
                    print >> sys.stderr, 'Previous file found with name:', filename, 'using suffix:', overwrites_suffix
                    filename = 'rep_' + rep_index + '_' + overwrites_suffix + '.csv'

                f = open(os.path.join(output, filename), 'wt')
                writer = csv.writer(f)
                writer.writerow(s_keys)

                elem = win_list[i]

                print elem
                print s_keys

                for k1 in s_keys:
                    column_data = []
                    for k2 in s_keys:
                        if k1 == k2:
                            column_data.append(-1)
                        else:
                            column_data.append(elem[k1][k2])
                        pass
                    writer.writerow(column_data)
            finally:
                if f is not None:
                    f.close()
        pass

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
        # overrides match pool if there is one via command line
        if self.usr_input['input'] is not None:
            self.config.match_pool_file = self.usr_input['input']

        if 'config_file' in self.usr_input and self.usr_input['config_file'] is not None:
            self.config.parse(self.usr_input['config_file'])
            self.strategy_selector.update_strategies(self.config.get_bots())

        # overrides number of matches if there is one via command line
        if self.usr_input['matches'] is not None:
            self.config.num_matches = self.usr_input['matches']

        # overrides file seed if there is one via command line
        if self.usr_input['random_seed'] is not None:
            random_seed = self.usr_input['random_seed']

        # overrides number of repetitions if user supplied it
        if self.usr_input['repetitions'] is not None:
            self.config.repetitions = self.usr_input['repetitions']

        # overrides output-spreadsheet
        if self.usr_input['excel'] is not None:
            self.config.output_spreadsheet = self.usr_input['excel']

        # overrides round-robin if there is one via command line
        if self.usr_input['tournament']:
            self.config.round_robin = self.usr_input['tournament']

        # overrides intermediates
        if self.usr_input['output_intermediate'] is not None:
            self.config.output_intermediate = self.usr_input['output_intermediate']

        # overrides results
        if self.usr_input['output_results'] is not None:
            self.config.SCORECHART_FILE = self.usr_input['output_results']

        # overrides enash-exploitation:
        if self.usr_input['enash_exploitation'] is not None:
            self.config.enash_exploitation = self.usr_input['enash_exploitation']

        # overrides egreedy-exploration
        if self.usr_input['egreedy_exploration'] is not None:
            self.config.egreedy_exploration = self.usr_input['egreedy_exploration']

        # overrides shuffle-match-list
        if self.usr_input['shuffle_match_list'] is not None:
            self.config.shuffle_match_list = self.usr_input['shuffle_match_list']

        # forces verbose if user requested via command line
        if self.usr_input['verbose'] is not None:
            self.config.verbose = self.usr_input['verbose']

        if self.usr_input['plot'] is not None:
            self.config.plot = self.usr_input['plot']

        # sets random seed
        random_seed = None
        if self.config.random_seed is not None:
            random_seed = self.config.random_seed

        # finally sets random seed
        if random_seed is not None:
            random.seed(random_seed)
            print 'Random seed set to %d' % random_seed

        self.result_parser = result_parser.ResultParser(self.config.match_pool_file)
        self.strategy_selector.set_unique_choices(self.result_parser.get_unique_opponents())

        # plays round-robin if configured for that and players were not explicitly passed via command line
        if self.config.round_robin and (self.usr_input['player_a'] is None and self.usr_input['player_b'] is None):
            players = StrategySelector.strategies.keys()  # players are the strategy (bot) selectors

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
        player_a.prepare()
        player_b.prepare()

        for i in xrange(self.config.num_matches):
            player_a.set_result_list(self.res_history)
            player_a.set_match_list(self.match_history)
            player_b.set_result_list(self.res_history)
            player_b.set_match_list(self.match_history)

            bot_a = player_a.get_next_bot()
            bot_b = player_b.get_next_bot()

            repeat_counter = 0
            while bot_a == bot_b:
                bot_a = player_a.get_next_bot()
                bot_b = player_b.get_next_bot()
                repeat_counter += 1
                if repeat_counter > 10:
                    if self.config.verbose:
                        print 'The bots are the same after several retries @ match', i
                    break
                    # raise StopIteration('The bots are the same after several retries...')

            if self.config.verbose:
                print i + 1, "Match", bot_a, 'vs', bot_b, '(match index:', self.match_index, ')'

            # if bots are equal, do not search for a match in the pool 'coz it does not exist
            if bot_a == bot_b:
                if self.config.verbose:
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

            # writes some nice information about progress
            sys.stdout.write(
                "\r%s -vs- %s -- Match #%d: %s - Winner: %s".ljust(60) %
                (player_a.get_name(), player_b.get_name(), i + 1, match, winner)
            )
            self.res_history.append(winner)
            self.match_history.append(match)
            pass
        print  # adds newline because of previous sys.stdout

    def get_match(self, bot_a, bot_b):
        """
        Given a list of matches, select a new match between the strategies of BotA and BotB using an index

        :param bot_a:
        :param bot_b:
        :return:
        """
        match = None
        if self.match_index >= len(self.bot_match_list) - 1:
            print >> sys.stderr, 'Match index (%d) >= number of matches (%d). Moving to pool beginning' % \
                                 (self.match_index, len(self.bot_match_list))
            self.match_index = 0
            # raise StopIteration('Match index have passed the match number, please select a small -m value')

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
            # raise StopIteration('Cannot find a match after the match index defined, please select a small -m value')

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
            '-i', '--input', help='Input file of the results file', required=False
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
            '-m', '--matches', help='The number of matches to run', type=int, required=False
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

        parser.add_argument(
            '-or', '--output_results',
            help='Output folder with the results in CSV format of every repetition of matches', required=False
        )

        parser.add_argument(
            '-oi', '--output_intermediate',
            help='Output folder with intermediate results in CSV format of every tournament repetition ', required=False
        )

        parser.add_argument(
            '-v', '--verbose', help='Prints informations about the games', required=False, action='store_true'
        )

        parser.add_argument(
            '-en', '--enash-exploitation', help='Parameter that defines the exploitation in an e-nash strategy',
            required=False, type=float
        )

        parser.add_argument(
            '-eg', '--egreedy-exploration', help='Defines the exploration in an e-greedy strategy',
            required=False, type=float
        )

        parser.add_argument(
            '-sh', '--shuffle-match-list', help='Shuffle the list of matches', required=False
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

        line_a, = plt.plot(d_range, data_a, color='red', label=player_a.strategy_name)
        line_b, = plt.plot(d_range, data_b, color='blue', label=player_b.strategy_name)
        # plt.legend(handles=[line_a, line_b], loc=2)
        plt.legend(loc=2)
        plt.grid(True)

        plt.xlabel('Match number')
        plt.ylabel('Accumulated wins')

        plt.show(block=False)
        self.fig_counter += 1
        pass

    def generate_excel_results(self):
        import xlsxwriter

        excel_filename = self.config.output_spreadsheet  # usr_input['excel']

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

                worksheet.write(0, 1 + i, id1)
                worksheet.write(1 + i, 0, id1)

                if id1 == id2:
                    worksheet.write(1 + i, 1 + j, '', format1)

                elif id2 in self.result_dict[id1]:
                    total = self.result_dict[id1][id2]  # str(self.result_dict[id1][id2]) + '%'

                    if self.config.verbose:
                        print id1, ":", id2, total

                    worksheet.write(1 + i, 1 + j, total)
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
