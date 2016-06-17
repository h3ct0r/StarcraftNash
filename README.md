# StarcraftNash
Repository of the Starcraft experiments regards the Nash equilibrium on RTS games

Example:
    python main.py -i results_demo/results.txt -a nash -b random_uniform -m 100

    -i 'File with the results'
    -a 'Strategy for the opponent a'
    -b 'Strategy for the opponent b'
	-c 'File with experiment configurations'
    -m 'Quantity of matches between a and b'
    -p 'Plot the results'
	-s 'Random seed for experiments'
	-r 'Number of repetitions for the tournament/matches'
	-e 'Outputs results to a .xls file given by this parameter'
    -t 'Create a tournament with all the strategies'
	-or 'Output folder with the results in CSV format of every repetition of matches'
	-v 'Prints lots of information'
	-en 'Parameter that defines the exploitation in an e-nash strategy'
	-eg 'Defines the exploration in an e-greedy strategy'
	-sh 'Shuffle the list of matches'
