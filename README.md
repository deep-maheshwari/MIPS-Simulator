# COproj

The Simulator Phase 1
-

Run the file Phase1/GUI.py

The Simulator Phase 2
-

Run the file Phase2/Pipelined_simulator.py
In the above file specify path for Phase1/bubble_sort.asm file in Simulate function line no. 716

The Phase 2 required to form a pipelined simulation of MIPS assembler and use data forwarding.
Final output of the program will be number of stalls, sorted data (bubble_sort.asm as input) and Instructions per cycle(IPC).

Simulation Procedure:-
-

1) This program will simulate these discrete events in a longitudinal way in which the order of stages is WB, MEM, EX, ID, IF.

2) The program finally calculates the cycles by taking into account stalls and data forwarding through latches according to MIPS format.

3) The cycle data is generated in an Excel Sheet which is modified and attached in Phase2/cycles.xlsx which gives the timeline of cycles being executed along with the stalls. Its screenshot is attached below:




Threaded Simulation (Optional):-
-

Run the file Phase2/Threaded_Simulator.py
In the above file specify path for Phase1/bubble_sort.asm file in Simulate function line no. 729

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

The Simulator Phase 3
-

Run the file Phase3/Cached_Simulator.py

Simulation Procedure:-
-

1) The user will be asked to enter the details of cache L1 nd L2 (here, we used two levels of Cache named L1 and L2) which includes block size, set associativity and number of blocks for both the caches.

2) The number of cycles, sorted array (for bubble_sort.asm as an input), number of stalls, number of memory stalls, raw form of cache are printed.

3) Miss count and Hit count for caches L1 and L2 are also printed.

4) We assumed that the write through doesn't bring any stall in the program, but when data is to be added in the memory, there is a write stall which costs about 200 cycles.

Overall Simulation
-

Run the file named GUI.py which will show a desktop app. This is made using a library of Python, 'Tkinter'. The desktop app contains a few options such as Load File, Run File(only), Run File Step-by-Step, Run file and Show Memory and Cache, etc. which shows everything from all the phases on the display.

![Alt text](/COproj/Images/Screenshot (6).png?raw=true "Caches")


By -----

Deep - CS18B008

Tapish - CS18B038
