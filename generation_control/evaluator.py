from pycirchdl import *

from constants import GENERATION_SIZE, B_OUT, CARRY_OUT
from utils import redirect_print, restore_print

def circuit_evaluation(circ):
    Input = [x.name for x in circ.input]
    Output = [y.name for y in circ.output]
    names = Input + Output
    head = " ".join(names)

    score = 0
    count = 0

    # check for any dangling pins
    for g in circ.gates:
        if g.name == "a1":
            continue
        elif g.name == "a2":
            continue
        elif g.name == "f1":
            continue
        elif g.name == "f2":
            continue
        elif g.name == "cin":
            continue
        elif g.name == "b0":
            continue
        elif g.name == "cout":
            continue

        no_out = True
        for w in circ.wires:
            if w.source == g.name+"/y":
                no_out = False
                break
        if no_out:
            msg = f"circuit {circ.name} has a dangling port: gate {g.name} have no out wire"
            print(msg)
            return score

    # check how many correct B and COUT values the circuit produces
    for a in Assign.iter(Input):
        o = circ(a)
        if o()[0] == B_OUT[count]:
            score = score + 1
        if o()[1] == CARRY_OUT[count]:
            score = score + 1

        count = count + 1

    return score

def generation_evaluation(circuit_gen, gen_count):
    circuit_gen = os.path.join(circuit_gen, str(gen_count))
    set_path([circuit_gen])

    # dictionary for storing the top 2 circuits
    # format, "circ1": (circuit_num, score)
    parents = {
        "circ1": (0, -1),
        "circ2": (0, -1),
    }

    for i in range(GENERATION_SIZE):
        i_str = str(i)
        # redirect stdout while loading a circuit
        # pycirchdl creates  few print statement each time you open a circuit
        # also used for catching any errors while opening
        try:
            redirect_print()
            load(i_str)
            circuit = PyCirc[i_str]
            restore_print()
        except:
            continue

        score = circuit_evaluation(circuit)
        msg = f"circuit {i}: score {score}/64"
        print(msg)

        # check if the current score is greater then the stored top two scores so far
        if score > parents["circ1"][1]:
            temp = parents["circ1"]
            parents["circ1"] = (i, score)
            parents["circ2"] = temp
        elif score > parents["circ2"][1]:
            parents["circ2"] = (i, score)
   
    return parents