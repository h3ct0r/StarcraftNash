# StarcraftNash

Repository with code for strategy selection in StarCraft. 

StarCraft is a complex game and players often resort to strategies (policies that map game states to actions). Here, we abstract game details and deal with strategy selection. 

StarcraftNash project runs a round-robin tournament between **strategy selection methods for StarCraft**. In the tournament, methods play each other for a number of matches, selecting strategies that play a game of StarCraft. As strategy may interact in interesting forms (like rock-paper-scissors), it is useful to develop smart strategy selection methods.

Please [read the wiki](https://github.com/h3ct0r/StarcraftNash/wiki/) for a detailed discussion on how the software works and how you can implement and test your own strategy selection methods.

###Example
(assuming you have cloned the project and are located at project's root directory)

Run a tournament with 500 matches between Nash and Random Uniform methods, useing a default [pool of matches](https://github.com/h3ct0r/StarcraftNash/wiki/Pool-of-matches) and parameters.

    python main.py -a nash -b random_uniform -i results_demo/fortress1000.txt -m 500

Accepted parameters are:

    -i: File with the pool of matches (more information [here](wiki/Pool-of-matches))
    -a: Strategy selection method for player a [optional if -t is supplied]
    -b: Strategy selection method for player b [optional if -t is supplied]
    -m: Number of matches between strategy selection methods
    -t: Round-robin tournament with all the strategies
    -s: Random seed for experiments
    -r: Number of tournament repetitions
    -e: Outputs tournament score chart to a .xls file given by this parameter
    -or: Output folder with intermediate results in CSV format of every tournament repetition 
    -v: Verbose - prints informations about the games
    -en: Parameter that defines the exploitation in an e-nash strategy
    -eg: Defines the exploration in an e-greedy strategy
    -sh: Shuffle the list of matches before each repetition
    -p: Plot the results
    
Run tournament with experiment parameters given by a default `.xml` configuration file:

    python main.py -c config/config_fortress.xml
    
Where `-c` specifies the path to the configuration file. Check this [wiki page](https://github.com/h3ct0r/StarcraftNash/wiki/Configuration-files) for instructions on how to specify parameters via the experiments configuration file.
