from pycirchdl import *

from constants import GENERATION_SIZE, B_OUT, CARRY_OUT

def evaluate():
    pass

def circuit_evaluation(circuit00):
    Input = [x.name for x in circuit00.input]
    Output = [y.name for y in circuit00.output]
    names = Input + Output
    head = " ".join(names)
    #print(head)

    score = 0
    count = 0

    # check for any dangling pins
    for g in circuit00.gates:
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
        for w in circuit00.wires:
            if w.source == g.name+"/y":
                no_out = False
                break
        if no_out:
            msg = f"gate {g.name} have no out wire"
            print(msg)
            return score

    for a in Assign.iter(Input):
        o = circuit00(a)
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
        "circ1": (-1, -1),
        "circ2": (-1, -1),
    }

    for i in range(GENERATION_SIZE):
        i_str = str(i)
        load(i_str)
        circuit = PyCirc[i_str]
        score = circuit_evaluation(circuit)
        msg = f"circuit {i}: score {score}/64"
        print(msg)

        if score > parents["circ1"][1]:
            temp = parents["circ1"]
            parents["circ1"] = (i, score)
            parents["circ2"] = temp
        elif score > parents["circ2"][1]:
            parents["circ2"] = (i, score)
   
    return parents