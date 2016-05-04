README:

To run this program, you will need to have the latest version of python 2.7 (and any external libraries here).  Run `nf_main.py` from the console to start the program.  It will produce both source and output files in the format specified in the original project.  Graph topology is randomly generated at runtime, giving realtime updates on the status of the network.  Once a solution has been found, I invite you to use the files generated as input for your own algorithms to compare with my outputs.

USAGE:

Running nf_main.py without any parameters will use the values specified in `STATICS.txt`.  You can use `--default` appended to the console command to force the use of default values over `STATICS.txt`.  The static variables and their default values are given below:

[LIST VARIABLES HERE]

To use specific input files, use `--id=###` in the console command.  For example: to use custom `nodes_abc.csv` and  `edges_abc.csv` as input files, run `nf_main.py --id=abc`

!WARNING!: These algorithms are intended to be run on an *ACYCLIC* network.  Passing in a custom graph with cycles will likely produce incorrect solutions.