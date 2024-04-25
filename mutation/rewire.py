import os
import random
from pycirchdl import *
import time

from constants import GENERATION_SIZE, MUTATION_RATE
from utils import redirect_print, restore_print

def rewire_circ(circ, circ_file) :
    # randomly choose two wires
    randomized_wires = circ.wires
    random.shuffle(randomized_wires)

    wire1 = randomized_wires[0]
    wire2 = randomized_wires[1]

    # create txt fields
    original_wire1_txt=f"WIRE(\"{wire1.source}\", \"{wire1.target}\")"
    new_wire1_txt=f"WIRE(\"{wire1.source}\", \"{wire2.target}\")"
    original_wire2_txt=f"WIRE(\"{wire2.source}\", \"{wire2.target}\")"
    new_wire2_txt=f"WIRE(\"{wire2.source}\", \"{wire1.target}\")"

    # write to circ file
    circ_file = os.path.join(circ_file, circ.name+".py")
    with open(circ_file, "r") as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if line == original_wire1_txt:
            modified_lines.append(new_wire1_txt)
        elif line == original_wire2_txt:
            modified_lines.append(new_wire2_txt)
        else:
            modified_lines.append(line)

    with open(circ_file, "w") as file:
        file.writelines(modified_lines)

def rewire(path, gen_count):
    path = os.path.join(path, str(gen_count))
    set_path([path])

    for i in range(GENERATION_SIZE):
        random_number = random.randint(0, 100)

        if random_number > MUTATION_RATE:
            continue

        print("rewire")
        redirect_print()
        need(str(i))
        circ = PyCirc[str(i)]
        restore_print()
        rewire_circ(circ, path)
