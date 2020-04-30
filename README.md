# COproj

The simulator phase 1
-

Run the file Phase1/GUI.py

The simulator phase 2
-

Run the file Phase2/pipelined_simulator.py
In the above file specify path for Phase1/bubble_sort.asm file in Simulate function line no. 715

The Phase 2 required to form a pipelined simulation of MIPS assembler and use data forwarding.
Final output of the program will be number of stalls and Instructions per cycle(IPC).

Simulation Procedure:-
-

1)We have implemented the simulation using threading in python.

2)In this we have a function pipeline which calls fetch, decode, execute, memory and writeback.

3)Pipeline function is threaded such that after every one cycle of previous pipeline function the next pipeline is triggered.

4)In some cases there are stalls where we just stall the length of one cycle which is 0.1 sec.

5)Simulation function carries out this process after which we have the output.

6)The program keeps printing the line number of instruction(PC), which are available in file Phase2/Prog_count.txt, until the end.

Drawbacks:-
-

1)The threading requires precise synchronization which is missing in our program hence sometimes the output is incorrect or program crashes.

2)Whenever the error "Sleep length must be positive......" is encountered program needs to be --stopped-- and re-run in preferably new terminal.

3)If the output is unsorted then again we need to re-run the program(Synchronization is the soul cause of such error where we could not do any good to resolve error.)

By -----

Deep - CS18B008

Tapish - CS18B038
