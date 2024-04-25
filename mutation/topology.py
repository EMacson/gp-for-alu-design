import os
import random
from pycirchdl import *
import time

from constants import GENERATION_SIZE, MUTATION_RATE
from utils import select_gate, redirect_print, restore_print

def insert_not(circ, circ_file):
    gate = "not"

    msg = "\n\n insert not \n\n\n"
    print(msg)

    # create new gate definition
    # get the last gate definition to inform the new gate's name
    num_wires = len(circ.wires)
    random_wire = random.randint(0, num_wires-1)
    original_wire = circ.wires[random_wire]
    new_wire = original_wire
    
    last_gate_num = -1
    last_gate = ""
    for g in circ.gates:
        if g.type == "inp" or g.type == "out":
            continue
        curr_num = int(g.name[1:])
        if curr_num > last_gate_num:
            last_gate_num = curr_num
            last_gate = g
    last_gate_num = last_gate_num + 1
    new_gate_name = "g"+str(last_gate_num)
    
    print(new_gate_name)
    print(original_wire.source)
    print(original_wire.target)

    # write to circ file
    circ_file = os.path.join(circ_file, circ.name+".py")
    original_last_gate_txt = F"GATE(\"{last_gate.name}\", type=\"{last_gate.type}\")"
    new_gate_txt = f"GATE(\"{new_gate_name}\", type=\"not\")\n"
    original_wire_txt = f"WIRE(\"{original_wire.source}\", \"{original_wire.target}\")"
    original_wire_txt_new = f"WIRE(\"{original_wire.source}\", \"{new_gate_name}/x\")\n"
    new_wire_txt = f"WIRE(\"{new_gate_name}/y\", \"{original_wire.target}\")\n"
    print(original_last_gate_txt)
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
        elif line.strip() == original_last_gate_txt:
            modified_lines.append(line)
            modified_lines.append(new_gate_txt)
        else:
            modified_lines.append(line)
        
    with open(circ_file, "w") as file:
        file.writelines(modified_lines)

def insert_or(circ, circ_file):
    msg = "\n\n insert or \n\n\n"
    print(msg)

    # create new gate definition
    # get the last gate
    last_gate_num = -1
    last_gate = ""
    for g in circ.gates:
        if g.type == "inp" or g.type == "out":
            continue
        curr_num = int(g.name[1:])
        if curr_num > last_gate_num:
            last_gate_num = curr_num
            last_gate = g
    last_gate_num = last_gate_num + 1
    new_gate_name = "g"+str(last_gate_num)

    # choose input wires
    randomized_wires = circ.wires
    random.shuffle(randomized_wires)
    
    wire1 = randomized_wires[0]
    wire2 = randomized_wires[1]
    temp = wire1
    temp.target = new_gate_name+"/x1"
    randomized_wires.append(temp)
    temp = wire2
    temp.target = new_gate_name+"/x2"
    randomized_wires.append(temp)
    print(wire1)
    print(wire2)
    
    # choose ouput wire
    random.shuffle(randomized_wires)
    wire3 = ""
    wire_found = False
    for w in randomized_wires:
        if w.target == "b":
            continue
        elif w.target == "cout":
            continue
        elif w.source == "a1":
            continue
        elif w.source == "a2":
            continue
        elif w.source == "f1":
            continue
        elif w.source == "f2":
            continue
        elif w.source == "cin":
            continue

        # check if wire target leds back to the new gate
        # if it does this creates a sequential circuit
        # and we should reject this wire
        temp = w
        print("\n======================\ncheck new wire\n==========================")
        print(temp)
        temp_gate = ""
        while not wire_found:
            # check if temp's target is an output gate
            if temp.target == "b0":
                wire_found = True
                break
            elif temp.target == "cout":
                wire_found = True
                break
            # check if temp's target is the new gate
            elif temp.target == new_gate_name+"/x1":
                break 
            elif temp.target == new_gate_name+"/x2":
                break

            #print(temp.target)
            temp_gate = temp.target[:2]
            #print(temp_gate)
            new_source = temp_gate+"/y"
            for v in circ.wires:
                if v.source == new_source:
                    temp = v
                    break

            print(temp)

        if wire_found:
            wire3 = w
            break

    # create txt fields
    try:
        new_gate_txt = f"GATE(\"{new_gate_name}\", type=\"or2\")\n"
        original_last_gate_txt = F"GATE(\"{last_gate.name}\", type=\"{last_gate.type}\")"
        wire1_txt=f"WIRE(\"{wire1.source}\", \"{new_gate_name}/x1\")\n"
        wire2_txt=f"WIRE(\"{wire2.source}\", \"{new_gate_name}/x2\")\n"
        old_wire_txt=f"WIRE(\"{wire3.source}\", \"{wire3.target}\")"
        wire3_txt=f"WIRE(\"{new_gate_name}/y\", \"{wire3.target}\")\n"
        print("old_wire_txt\t"+old_wire_txt)
        print("original_last_gate_txt\t"+original_last_gate_txt)
        print("new_gate_txt\t"+new_gate_txt)
        print("wire1_txt\t"+wire1_txt)
        print("wire2_txt\t"+wire2_txt)
        print("wire3_txt\t"+wire3_txt)
    except:
        print("couldn't insert or gate")
        return

    # write to circ file
    circ_file = os.path.join(circ_file, circ.name+".py")
    with open(circ_file, "r") as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if line.strip() == old_wire_txt:
            modified_lines.append(wire1_txt)
            modified_lines.append(wire2_txt)
            modified_lines.append(wire3_txt)
        elif line.strip() == original_last_gate_txt:
            modified_lines.append(line)
            modified_lines.append(new_gate_txt)
        else:
            modified_lines.append(line)
        
    with open(circ_file, "w") as file:
        file.writelines(modified_lines)

def insert_and(circ, circ_file):
    msg = "\n\n insert and \n\n\n"
    print(msg)

    # create new gate definition
    # get the last gate
    last_gate_num = -1
    last_gate = ""
    for g in circ.gates:
        if g.type == "inp" or g.type == "out":
            continue
        curr_num = int(g.name[1:])
        if curr_num > last_gate_num:
            last_gate_num = curr_num
            last_gate = g
    last_gate_num = last_gate_num + 1
    new_gate_name = "g"+str(last_gate_num)

    # choose input wires
    randomized_wires = circ.wires
    random.shuffle(randomized_wires)
    
    wire1 = randomized_wires[0]
    wire2 = randomized_wires[1]
    temp = wire1
    wire1.target = new_gate_name+"/x1"
    randomized_wires.append(temp)
    temp = wire2
    wire2.target = new_gate_name+"/x2"
    randomized_wires.append(temp)
    print(wire1)
    print(wire2)
    
    # choose ouput wire
    random.shuffle(randomized_wires)
    wire3 = ""
    wire_found = False
    for w in randomized_wires:
        if w.target == "b":
            continue
        elif w.target == "cout":
            continue
        elif w.source == "a1":
            continue
        elif w.source == "a2":
            continue
        elif w.source == "f1":
            continue
        elif w.source == "f2":
            continue
        elif w.source == "cin":
            continue
        
        temp = w
        print("\n==================\ncheck new wire\n==========================")
        print(temp)
        temp_gate = ""
        while not wire_found:
            # check if temp's target is an output gate
            if temp.target == "b0":
                wire_found = True
                break
            elif temp.target == "cout":
                wire_found = True
                break
            # check if temp's target is the new gate
            elif temp.target == new_gate_name+"/x1":
                break 
            elif temp.target == new_gate_name+"/x2":
                break

            temp_gate = temp.target[:2]
            
            new_source = temp_gate+"/y"
            for v in circ.wires:
                if v.source == new_source:
                    temp = v
                    break

            print(temp)

        if wire_found:
            wire3 = w
            break

    # create txt fields
    try:
        new_gate_txt = f"GATE(\"{new_gate_name}\", type=\"and2\")\n"
        original_last_gate_txt = F"GATE(\"{last_gate.name}\", type=\"{last_gate.type}\")"
        wire1_txt=f"WIRE(\"{wire1.source}\", \"{new_gate_name}/x1\")\n"
        wire2_txt=f"WIRE(\"{wire2.source}\", \"{new_gate_name}/x2\")\n"
        old_wire_txt=f"WIRE(\"{wire3.source}\", \"{wire3.target}\")"
        wire3_txt=f"WIRE(\"{new_gate_name}/y\", \"{wire3.target}\")\n"
        print("old_wire_txt\t"+old_wire_txt)
        print("original_last_gate_txt\t"+original_last_gate_txt)
        print("new_gate_txt\t"+new_gate_txt)
        print("wire1_txt\t"+wire1_txt)
        print("wire2_txt\t"+wire2_txt)
        print("wire3_txt\t"+wire3_txt)
    except:
        print("couldn't insert and gate")
        return

    # write to circ file
    circ_file = os.path.join(circ_file, circ.name+".py")
    with open(circ_file, "r") as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if line.strip() == old_wire_txt:
            modified_lines.append(wire1_txt)
            modified_lines.append(wire2_txt)
            modified_lines.append(wire3_txt)
        elif line.strip() == original_last_gate_txt:
            modified_lines.append(line)
            modified_lines.append(new_gate_txt)
        else:
            modified_lines.append(line)
        
    with open(circ_file, "w") as file:
        file.writelines(modified_lines)

# insert new gate
def insert(circ, path):
    # randomly select gate tpe to insert
    random_number = random.randint(0, 3)
    if random_number == 0:
        msg = f"\tinsert not gate"
        print(msg)
        insert_not(circ, path)
    elif random_number == 1:
        msg = f"\tinsert or gate"
        print(msg)
        insert_or(circ, path)
    elif random_number == 2:
        msg = f"\tinsert and gate"
        print(msg, path)
        insert_and(circ, path)

def delete_size1(circ, gate, circ_file):
    wire1=""
    wire3=""
    # get input wires
    for w in circ.wires:
        if w.target == gate.name+"/x":
            wire1 = w
        elif w.source == gate.name+"/y":
            wire3 = w
    out_wires = []
    # get ouput wires
    for w in circ.wires:
        if w.source == gate.name+"/y":
            out_wires.append(w)

    # txt variables for file
    try:
        gate_txt=f"GATE(\"{gate.name}\", type=\"{gate.type}\")"
        wire_txt=f""
        wire1_txt=f"WIRE(\"{wire1.source}\", \"{wire1.target}\")"
        wire3_txt=f"WIRE(\"{wire3.source}\", \"{wire3.target}\")"
        out_wires_txt = []
        for t in out_wires:
            wire_txt=f"WIRE(\"{wire1.source}\", \"{t.target}\")\n"
            out_wires_txt.append(wire_txt)
        wire_txt=f"WIRE(\"{wire1.source}\", \"{wire3.target}\")\n"
    except:
        print(f"couldn't delete {gate.type}")
        return

    print("\n"+gate_txt)
    print(wire1_txt)
    print(wire3_txt)
    print("\n"+wire_txt)

    # write to circ file
    circ_file = os.path.join(circ_file, circ.name+".py")
    with open(circ_file, "r") as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if line.strip() == gate_txt:
            continue
        elif line.strip() == wire1_txt:
            continue
        elif line.strip() == wire3_txt:
            modified_lines+=(out_wires_txt)
        else:
            modified_lines.append(line)

    with open(circ_file, "w") as file:
        file.writelines(modified_lines)

def delete_size2(circ, gate, circ_file):
    wire1=""
    wrie2=""
    wire3=""
    # get input wires
    for w in circ.wires:
        if w.target == gate.name+"/x1":
            wire1 = w
        elif w.target == gate.name+"/x2":
            wire2 = w
        elif w.source == gate.name+"/y":
            wire3 = w
    out_wires = []
    # get ouput wires
    for w in circ.wires:
        if w.source == gate.name+"/y":
            out_wires.append(w)

    # write text components
    try:
        gate_txt=f"GATE(\"{gate.name}\", type=\"{gate.type}\")"
        wire_txt=f""
        wire1_txt=f"WIRE(\"{wire1.source}\", \"{wire1.target}\")"
        wire2_txt=f"WIRE(\"{wire2.source}\", \"{wire2.target}\")"
        wire3_txt=f"WIRE(\"{wire3.source}\", \"{wire3.target}\")"
        out_wires_txt = []
        choose_in = random.randint(1, 2)
        if choose_in == 1:
            for t in out_wires:
                wire_txt=f"WIRE(\"{wire1.source}\", \"{t.target}\")\n"
                out_wires_txt.append(wire_txt)
            wire_txt=f"WIRE(\"{wire1.source}\", \"{wire3.target}\")\n"
        elif choose_in == 2:
            for t in out_wires:
                wire_txt=f"WIRE(\"{wire2.source}\", \"{t.target}\")\n"
                out_wires_txt.append(wire_txt)
            wire_txt=f"WIRE(\"{wire2.source}\", \"{wire3.target}\")\n"
    except:
        print(f"couldn't delete {gate.type}")
        return

    print("\n"+gate_txt)
    print(wire1_txt)
    print(wire2_txt)
    print(wire3_txt)
    print("\n"+wire_txt)

    # write to circ file
    circ_file = os.path.join(circ_file, circ.name+".py")
    with open(circ_file, "r") as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if line.strip() == gate_txt:
            continue
        elif line.strip() == wire1_txt:
            continue
        elif line.strip() == wire2_txt:
            continue
        elif line.strip() == wire3_txt:
            modified_lines+=(out_wires_txt)
        else:
            modified_lines.append(line)

    with open(circ_file, "w") as file:
        file.writelines(modified_lines)
    

# delete gate
def delete(circ, path):
    # only delete a gate if the circuit has 12 or more gates
    if len(circ.gates) < 12:
        return
    
    # randomly select gate to delete
    randomized_gates = circ.gates
    random.shuffle(randomized_gates)

    gate_to_delete = randomized_gates[0]
    
    # delete gate based on its input port size
    if gate_to_delete.type == "or2":
        delete_size2(circ, gate_to_delete, path)
    elif gate_to_delete.type == "and2":
        delete_size2(circ, gate_to_delete, path)
    elif gate_to_delete.type == "not":
        delete_size1(circ, gate_to_delete, path)

    
def invert_size2(circ, gate, new_type, circ_file):
    # create txt fields
    original_txt=f"GATE(\"{gate.name}\", type=\"{gate.type}\")"
    new_gate_txt=f"GATE(\"{gate.name}\", type=\"{new_type}\")"

    # write to circ file
    circ_file = os.path.join(circ_file, circ.name+".py")
    with open(circ_file, "r") as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if line.strip() == original_txt:
            modified_lines.append(new_gate_txt)
        else:
            modified_lines.append(line)

    with open(circ_file, "w") as file:
        file.writelines(modified_lines)

# invert/change gate type
def invert(circ, path):
    # randomly select gate to invert
    randomized_gates = circ.gates
    random.shuffle(randomized_gates)

    gate_to_delete = randomized_gates[0]

    # only invert or2 to and 2, or and2 to or2
    if gate_to_delete.type == "or2":
        invert_size2(circ, gate_to_delete, "and2", path)
    elif gate_to_delete.type == "and2":
        invert_size2(circ, gate_to_delete, "or2", path)

def topology(path, gen_count):
    path = os.path.join(path, str(gen_count))
    set_path([path])

    for i in range(GENERATION_SIZE):
        random_number = random.randint(0, 100)

        if random_number > MUTATION_RATE:
            continue

        print("mutate topology")
        
        redirect_print()
        need(str(i))
        circ = PyCirc[str(i)]
        restore_print()
        # select insert or delete
        random_number = random.randint(0, 3)
        if random_number == 0:
            print(i)
            insert(circ, path)
            print(i)
            break
        elif random_number == 1:
            delete(circ, path)
            print(i)
        elif random_number == 2:
            invert(circ, path)
