# StarcraftNash

Repository with code for strategy selection in Real-Time Strategy games. 

StarCraft is a complex game and players often resort to strategies (policies that map game states to actions). Here, we abstract game details and deal with strategy selection. 

So far, we implement the following strategy selection methods:

1. Frequentist: attempts to exploit opponent by selecting the best-response of its most frequent strategy;
2. Reply-last: attempts to exploit opponent by selecting the best-response of its last strategy;
3. alpha-greedy: selects a random strategy (exploration) with probability alpha, and the most victorious strategy with probability 1 - alpha (exploitation);
4. Single choice: selects a single strategy, regardless of what the opponent does. This is the most exploitable technique;
5. Nash: selects a strategy according to Nash Equilibria, given determined probabilities;
6. epsilon-Nash: attempts to exploit opponent with probability epsilon (by playing frequentist) and plays a safe strategy (Nash Equilibria) with probability 1 - epsilon.

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
