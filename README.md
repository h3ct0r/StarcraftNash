# StarcraftNash
Repository of the Starcraft experiments regarding the Nash equilibrium on RTS games. 

By noticing that some strategies interact in a cyclical way, we draw insights from strategy selection in classical rock-paper-scissors game: we compute the Nash Equilibrium from results of several matches and build a strategy selection method that tries to behave accordingly.
We call this strategy-selection metagame for playing the real-time strategy (RTS) game StarCraft. We proceed by estimating a Nash Equilibrium in the metagame which specifies the probabilities with which bots should be chosen to achieve a theoretically-guaranteed expected payoff.

The experiments are performed with participant bots of AIIDE 2015 StarCraft AI tournament. Bots usually act differently from each other so that different bots can be considered distinct strategies within this given concept. Thus, in our strategy-selection metagame, to choose a strategy means to play a StarCraft match following the policy dictated by the chosen bot.

In order to test insights from computer rock-paper-scissors tournaments, we evaluate the following strategy selection techniques in StarCraft:
1. Frequentist: attempts to exploit opponent by selecting the best-response of its most frequent strategy;
2. Reply-last: attempts to exploit opponent by selecting the best-response of its last strategy;
3. a-greedy: selects a random strategy (exploration) with probability a, and the most victorious strategy with probability 1 - a (exploitation);
4. Single choice: selects a single strategy, regardless of what the opponent does. This is the most exploitable technique;
5. Nash: selects a strategy according to Nash Equilibria, given determined probabilities;
6. e-Nash: attempts to exploit opponent with probability e (by playing frequentist) and plays a safe strategy (Nash Equilibria) with probability 1 - e.

###Example
The next lines shows an example of the command to execute our experiments:
    python main.py -i results_demo/results.txt -a nash -b random_uniform -m 100
	python main.py -c config/config_fortress.xml

The following parameters can be used to choose the options for the execution:
    -i: File with the results
    -a: Strategy for the opponent a
    -b: Strategy for the opponent b
	-c: File with experiment configurations
    -m: Quantity of matches between a and b
    -p: Plot the results
	-s: Random seed for experiments
	-r: Number of repetitions for the tournament/matches
	-e: Outputs results to a .xls file given by this parameter
    -t: Create a tournament with all the strategies
	-or: Output folder with the results in CSV format of every repetition of matches
	-v: Prints informations about the games
	-en: Parameter that defines the exploitation in an e-nash strategy
	-eg: Defines the exploration in an e-greedy strategy
	-sh: Shuffle the list of matches