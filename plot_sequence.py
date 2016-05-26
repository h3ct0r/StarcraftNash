import matplotlib.pyplot as plt
import result_parser
import argparse

__author__ = 'Anderson Tavares'


def plot_sequence(results_file, bot1, bot2, first=0, last=None, num_parts=1):
    rparser = result_parser.ResultParser(results_file)
    rparser.parse_file()

    if last is None:
        last = len(rparser.get_match_list())

    valid_matches = -1
    x_values = []
    y_values = []
    for winner, loser in rparser.get_match_list():

        if winner in [bot1, bot2] and loser in [bot1, bot2]:

            valid_matches += 1

            if valid_matches < first:
                continue

            if valid_matches > last:
                break

            x_values.append(valid_matches)

            # y=0 is bot1 and y=1 is bot2
            if winner == bot1:
                y_values.append(0)
            else:
                y_values.append(1)

    # makes subplots with parts of data
    plt.figure(1)

    for part in range(0, num_parts):
        datalen = len(y_values)

        start = datalen * part / num_parts
        end = start + (datalen / num_parts)

        plt.subplot(int('%d1%d' % (num_parts, part + 1)))
        plt.plot(x_values[start:end], y_values[start:end], 'ro')
        plt.ylabel('0=%s / 1=%s' % (bot1, bot2))
        plt.xlabel('Match number')
        plt.axis([start, end + 1, -.5, 1.5])

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Plots the sequence of matches between two bots'
    )

    parser.add_argument(
        'result', help='Input file of with detailed tournament results',
    )

    parser.add_argument(
        'bots', nargs=2, help='Names of two bots whose matches will be plotted',
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
        '-d', '--divide', type=int, help='Divide plot in a number of parts',
        default=1, required=False
    )

    args = parser.parse_args()

    plot_sequence(
        args.result, args.bots[0], args.bots[1], args.first, args.last, args.divide
    )


