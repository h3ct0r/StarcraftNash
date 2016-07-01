# StarcraftNash

Repository with code for strategy selection in Real-Time Strategy games. 

StarCraft is a complex game and players often resort to strategies (policies that map game states to actions). Here, we abstract game details and deal with strategy selection. 

To check the list of strategy selection methods and how to implement one yourself, check out the [wiki page](https://github.com/h3ct0r/StarcraftNash/wiki/Strategy-selection-techniques).

###Example
Run with experiment parameters given by command line:

    python main.py -i results_demo/results.txt -a nash -b random_uniform -m 100

Where parameters are:

    -i: File with the pool of matches (more information [here](wiki/Pool-of-matches))
    -a: Strategy selection method for player a [optional if -t is supplied]
    -b: Strategy selection method for player b [optional if -t is supplied]
    -m: Number of matches between strategy selection methods
    -t: Create a tournament with all the strategies
    -s: Random seed for experiments
    -r: Number of tournament repetitions
    -e: Outputs tournament score chart to a .xls file given by this parameter
    -or: Output folder with the results in CSV format of every repetition of matches (intermediate results)
    -v: Verbose - prints informations about the games
    -en: Parameter that defines the exploitation in an e-nash strategy
    -eg: Defines the exploration in an e-greedy strategy
    -sh: Shuffle the list of matches before each repetition
    -p: Plot the results
    
Run with experiment parameters given by a `.xml` configuration file:

    python main.py -c config/config_fortress.xml
    
Where `-c` specifies the path to the configuration file. Check this [wiki page](https://github.com/h3ct0r/StarcraftNash/wiki/Configuration-files) for instructions on how to specify parameters via the experiments configuration file.
