# gp-for-alu-design

## Quickstart
The following are system requirements for running this project
- Python 3.12.2
- PyCircHDL Library https://github.com/samyzaf/pycirchdl 
- Graphviz Library https://graphviz.org 

## To Run
To run simply run main.py. This will run the main execution loop for the system. Print statements will show the score for each circuit during the evaluation step. Print statements will also appear indicating when mutating topology, mutating sizing, or crossover is happening and what the system is doing (ie "insert not gate").

At times the system may stall. This happens when trying to open a circuit that is sequential (a circuit with a feedback loop), or when a circuit has some dangling ports. I tried to catch these with try blocks, however stalls still happen occasionally. To fix this press 'crtl+c', this will get the system back to the main execution loop.

## Output
The system's output will show under circuits, in a subdirectory that is the time-stamp when main.py started executing. Each generation will contain 100 circuit defintions and a parent circuit that was the result of crossover between the top two performing circuits a of that generation, this parent circuits is used to generate the next generation. After main.py finishes executing the final diagram will by created in the time-stamped directory under final.png. If the system is stoppped early final.png will not be produced. You can change the maximum number of generations by changing the for loop in main.py to have a different range value.