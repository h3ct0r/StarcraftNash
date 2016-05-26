import result_parser
import argparse
import sys

__author__ = 'Anderson Tavares'


def calculate(results_file, bot1, bot2, first=0, last=None, num_parts=4, output=None):

    rparser = result_parser.ResultParser(results_file)
    x_values, y_values = rparser.analyse(bot1, bot2, first, last)

    out_stream = sys.stdout if output is None else open(output, 'w')

    print >> out_stream, 'Total matches in %s: %d\n#matches %s vs %s: %d\n' % \
        (results_file, len(rparser.get_match_list()), bot1, bot2, len(y_values))

    for part in range(0, num_parts):
        # considers no draws and counts the number of victories for each bot
        total_len = len(y_values)

        start = total_len * part / num_parts
        end = start + (total_len / num_parts)

        data_part = y_values[start:end]

        # number of bot2 victories is the number of ones in array
        victories_bot2 = sum(data_part) / float(len(data_part))
        victories_bot1 = 1 - victories_bot2

        print >> out_stream, 'Match %d to %d:' % (start, end)
        print >> out_stream, '%s: %.5f\n%s: %.5f\n' % (bot1, victories_bot1, bot2, victories_bot2)

    out_stream.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Calculates win distribution of bots along matches'
    )

    parser.add_argument(
        'result', help='Input file of with detailed tournament results',
    )

    parser.add_argument(
        'bots', nargs=2, help='Names of two bots whose matches will be analysed',
    )

    parser.add_argument(
        '-f', '--first', type=int, help='First match of sequence to show. Starts with zero.',
        default=0, required=False
    )

    parser.add_argument(
        '-l', '--last', type=int, help='Last match of sequence to show.',
        default=None, required=False
    )

    parser.add_argument(
        '-d', '--divide', type=int, help='Number of parts to split analysis',
        default=4, required=False
    )

    parser.add_argument(
        '-o', '--output', type=str, help='Filename to save analysis',
        default=None, required=False
    )

    args = parser.parse_args()

    calculate(
        args.result, args.bots[0], args.bots[1], args.first, args.last,
        args.divide, args.output
    )

