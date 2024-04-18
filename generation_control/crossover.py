import os
import shutil
from pycirchdl import *

def crossover(gen, gen_count, p1, p2):
    gen = os.path.join(gen, str(gen_count))
    set_path([gen])
    need(p1)
    need(p2)
    circ1 = PyCirc[p1]
    circ2 = PyCirc[p2]

    msg = f"\n\np1 gates: {len(circ1.gates)}    p2 gates: {len(circ2.gates)}\n\n"
    print(msg)

    parent_file = os.path.join(gen, "parent.py")
    circ1_file = os.path.join(gen, p1+".py")
    #with open(circ1_file, "r") as file:
    #    content = file.read()

    shutil.copy2(circ1_file, parent_file)

    pass