# gp-for-alu-design

## Installiation Requirements
- Python 3.12.2
- PyCircHDL Library https://github.com/samyzaf/pycirchdl 
- Graphviz Library https://graphviz.org 

## To Run
To run simply run main.py. This will run the main execution loop for the system. Print statements will show the score for each circuit during the evaluation step. Print statements will also appear indicating when mutating topology, mutating sizing, or crossover is happening and what the system is doing (ie "insert not gate").

At times the system may stall. This happens when trying to open a circuit that is sequential (a circuit with a feedback loop), or when a circuit has some dangling ports. I tried to catch these with try blocks, however stalls still happen occasionally. To fix this press 'crtl+c', this will get the system back to the main execution loop.