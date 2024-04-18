import os
import random
from pycirchdl import *

from constants import GENERATION_SIZE, MUTATION_RATE
#from utils import gate_select, get_gate
from utils import select_gate

def insert_not(circ, circ_file):
    gate = "not"

    num_wires = len(circ.wires)
    random_wire = random.randint(0, num_wires-1)
    original_wire = circ.wires[random_wire]
    new_wire = original_wire
    #print(circ.gates)
    num_gates = len(circ.gates)
    last_gate_name = circ.gates[num_gates-1].name
    gate_suffix = last_gate_name[1:]
    gate_num = int(gate_suffix)
    new_gate_name = "g"+str(gate_num+1)
    print(new_gate_name)
    print(original_wire.source)
    print(original_wire.target)

    # write to circ file
    circ_file = os.path.join(circ_file, circ.name+".py")
    new_gate_txt = f"GATE(\"{new_gate_name}\", type=\"not\")\n"
    original_wire_txt = f"WIRE(\"{original_wire.source}\", \"{original_wire.target}\")"
    original_wire_txt_new = f"WIRE(\"{original_wire.source}\", \"{new_gate_name}/x\")\n"
    new_wire_txt = f"WIRE(\"{new_gate_name}/y\", \"{original_wire.target}\")\n"
    print(new_gate_txt)
    print(original_wire_txt)
    print(original_wire_txt_new)
    print(new_wire_txt)
    with open(circ_file, "r") as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if line.strip() == original_wire_txt:
            modified_lines.append(original_wire_txt_new)
            modified_lines.append(new_wire_txt)
            modified_lines.append(new_gate_txt)
        else:
            modified_lines.append(line)
        
    with open(circ_file, "w") as file:
        file.writelines(modified_lines)

    #not_gate = Gate(name=new_gate_name, type="not")
    #circ.add_node(not_gate)


    #print(circ.gates)

    #for w in circ.gates:
    #    print(w)
    pass

def insert_or():
    pass

def insert_and():
    pass

# insert new gate
def insert(circ):
    # get gate to insert
    #gate = select_gate()
    #msg = f"\tinsert {gate} gate"
    #print(msg)

    random_number = random.randint(0, 2)
    if random_number == 0:
        msg = f"\tinsert not gate"
        print(msg)
        insert_not(circ)
    elif random_number == 1:
        msg = f"\tinsert or gate"
        print(msg)
        insert_or()
    elif random_number == 2:
        msg = f"\tinsert and gate"
        print(msg)
        insert_and()

# delete gate
def delete(circ):
    pass

# invert/change gate type
def invert(circ):
    pass

def topology(path, gen_count):
    path = os.path.join(path, str(gen_count))
    set_path([path])

    for i in range(GENERATION_SIZE):
        random_number = random.randint(0, 100)

        if random_number > MUTATION_RATE:
            continue

        print("mutate topology")
        #circ = os.path.join(path, str(i))
        need(str(i))
        circ = PyCirc[str(i)]
        
        # select insert or delete
        random_number = random.randint(0, 2)
        if random_number == 0:
            insert_not(circ, path)
            print(i)
            break
        elif random_number == 1:
            delete(circ)
        elif random_number == 2:
            invert(circ)
        pass

    pass