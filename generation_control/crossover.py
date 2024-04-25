import os
import shutil
from pycirchdl import *

# gate definitions for input and output pins
circuit_init = [
    "GATE(\"a1\", type=\"inp\")\n",
    "GATE(\"a2\", type=\"inp\")\n",
    "GATE(\"f1\", type=\"inp\")\n",
    "GATE(\"f2\", type=\"inp\")\n",
    "GATE(\"cin\", type=\"inp\")\n",
    "GATE(\"b0\", type=\"out\")\n",
    "GATE(\"cout\", type=\"out\")\n\n",
]

def perform_crossover(gen, p1, p2):
    # get p1 gates
    p1_gates = []
    for g in p1.gates:
        if g.type == "inp":
            continue
        elif g.type == "out":
            continue

        p1_gates.append(g)

    # get p2 gates
    p2_gates = []
    for g in p2.gates:
        if g.type == "inp":
            continue
        elif g.type == "out":
            continue

        p2_gates.append(g)

    # set p1 gates to be the type of p2 gates
    for i in range(len(p1_gates)):
        # check for matching gate name/location
        # try catches out of bound errors for p2_gates
        try:
            if p1_gates[i].name == p2_gates[i].name:
                # check for matching gate sizing
                if (p1_gates[i].type == "or2") or (p1_gates[i].type == "and2"):
                    if (p2_gates[i].type == "or2") or (p2_gates[i].type == "and2"):
                        p1_gates[i].type = p2_gates[i].type
        except:
            break
    
    # create txt fields
    modified_lines = []
    modified_lines.extend(circuit_init)

    for g in p1_gates:
        gate_txt=f"GATE(\"{g.name}\", type=\"{g.type}\")\n"
        modified_lines.append(gate_txt)

    modified_lines.append("\n")

    # write to file
    circ_file = os.path.join(gen, p1.name+".py")
    with open(circ_file, "r") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("WIRE"):
            modified_lines.append(line)
            modified_lines.append("\n")
    
    circ_file = os.path.join(gen, "parent.py")
    with open(circ_file, "w") as file:
        file.writelines(modified_lines)


def crossover(gen, gen_count, p1, p2):
    gen = os.path.join(gen, str(gen_count))
    set_path([gen])
    need(p1)
    need(p2)
    circ1 = PyCirc[p1]
    circ2 = PyCirc[p2]

    perform_crossover(gen, circ1, circ2)