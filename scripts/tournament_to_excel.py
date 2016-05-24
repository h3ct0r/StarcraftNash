import json
import xlsxwriter

data = None

data = {
    'E-greedy': {
        'WinPrev': 18.5,
        'Xelnaga': 78.0,
        'Skynet': 49.0,
        'NUSBot': 67.5,
        'Nash': 42.5,
        'MaxWinPrev': 29.5,
        'Random uniform': 47.0,
        'E-greedy': 0.0
    },
    'WinPrev': {
        'E-greedy': 81.5,
        'Xelnaga': 80.0,
        'Skynet': 51.5,
        'NUSBot': 93.0,
        'Nash': 47.5,
        'MaxWinPrev': 79.5,
        'Random uniform': 58.0,
        'WinPrev': 0.0
    },
    'Xelnaga': {
        'E-greedy': 22.0,
        'WinPrev': 20.0,
        'Skynet': 20.0,
        'NUSBot': 93.5,
        'Nash': 39.0,
        'MaxWinPrev': 20.0,
        'Random uniform': 57.5,
        'Xelnaga': 0.0
    },
    'Skynet': {
        'E-greedy': 51.0,
        'Xelnaga': 80.0,
        'WinPrev': 48.5,
        'NUSBot': 48.5,
        'Nash': 65.5,
        'MaxWinPrev': 49.0,
        'Random uniform': 65.5,
        'Skynet': 0.0
    },
    'NUSBot': {
        'E-greedy': 32.5,
        'WinPrev': 7.0,
        'Xelnaga': 6.5,
        'Skynet': 51.5,
        'Nash': 39.0,
        'MaxWinPrev': 8.0,
        'Random uniform': 32.5,
        'NUSBot': 0.0
    },
    'Nash': {
        'E-greedy': 57.5,
        'WinPrev': 52.5,
        'Xelnaga': 61.0,
        'Skynet': 34.5,
        'NUSBot': 61.0,
        'MaxWinPrev': 34.5,
        'Random uniform': 61.0,
        'Nash': 0.0
    },
    'MaxWinPrev': {
        'E-greedy': 70.5,
        'WinPrev': 20.5,
        'Xelnaga': 80.0,
        'Skynet': 51.0,
        'NUSBot': 92.0,
        'Nash': 65.5,
        'Random uniform': 31.5,
        'MaxWinPrev': 0.0
    },
    'Random uniform': {
        'E-greedy': 53.0,
        'WinPrev': 42.0,
        'Xelnaga': 42.5,
        'Skynet': 34.5,
        'NUSBot': 67.5,
        'Nash': 39.0,
        'MaxWinPrev': 68.5,
        'Random uniform': 0.0
    }
}

strategy_list_srt = sorted(data.keys())

workbook = xlsxwriter.Workbook('tournament_results_1.xlsx')

worksheet = workbook.add_worksheet()

element_count = len(strategy_list_srt)

format1 = workbook.add_format()
format1.set_pattern(1) 
format1.set_bg_color('green')

i = 0
for id1 in strategy_list_srt:
	j = 0
	for id2 in strategy_list_srt:

		worksheet.write(0, 1+i, id1)
		worksheet.write(1+i, 0, id1)

		if id1 == id2:
			worksheet.write(1 + i, 1+j, '', format1)
			
		elif id2 in data[id1]:
			total = str(data[id1][id2]) + '%'

			print id1, ":", id2, total

			worksheet.write(1 + i, 1+j, total)
		j += 1
		pass

	i += 1
	print i, "/", element_count
	pass

workbook.close()