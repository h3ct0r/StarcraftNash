import csv
import collections

__author__ = 'Anderson Tavares'


def from_file(chart_file, scale=1):
    """
    Reads a scorechart from a .csv file with choice names in first line and scorechart in the following.
    Example: for the following scorechart with probabilities of victories:

    Bot	        Xeln	Cruz	NUSB	Aiur	Skyn
    Xelnaga	    50%	    26%	    86%    	73% 	73%
    CruzBot	    74%	    50%	    80%    	67% 	16%
    NUSBot	    14%	    20%	    50%    	74% 	97%
    Aiur	    27%	    33%	    26%    	50% 	79%
    Skynet	    27%	    84%	    3%	    21% 	50%

    The file could be:
    Xelnaga,CruzBot,NUSBot,Aiur,Skynet
    50,26,86,73,73
    74,50,80,67,16
    14,20,50,74,97
    27,33,26,50,79
    27,84,3,21,50

    (if decimals are desired instead of percents, one can apply a scaling transform)

    :param chart_file:path to scorechart.csv file
    :param scale: factor to scale file values
    :return:
    """

    chart = {}
    with open(chart_file, 'rb') as csv_file:
        reader = csv.reader(csv_file)

        rows = list(reader)

        # first line has the names
        names = rows[0]

        # remaining rows have the scores in order
        for row_num, row in enumerate(rows[1:]):
            chart[names[row_num]] = {names[col_num]: scale*float(col) for col_num, col in enumerate(row)}

    return chart
