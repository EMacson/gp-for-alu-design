from pycirchdl import *

from constants import GENERATION_SIZE, B_OUT, CARRY_OUT

def evaluate():
    pass

def circuit_evaluation(circuit00):
    #set_path([circuit_gen])
    #load(circuit_num)
    #circuit00 = PyCirc[circuit_num]
    Input = [x.name for x in circuit00.input]
    Output = [y.name for y in circuit00.output]
    names = Input + Output
    head = " ".join(names)
    #print(head)

    score = 0
    count = 0

    for a in Assign.iter(Input):
        o = circuit00(a)
        #msg = f"circuit [{o()[0]}, {o()[1]}], actual [{B_OUT[count]}, {CARRY_OUT[count]}]"
        #print(msg)

        if o()[0] == B_OUT[count]:
            #print("B")
            #print(o()[0])
            #print(B_OUT[count])
            score = score + 1
        if o()[1] == CARRY_OUT[count]:
            #print("carry out")
            #print(o()[1])
            #print(CARRY_OUT[count])
            score = score + 1

        count = count + 1

        #bits = tuple(a() + o())
        #line = len(bits) * "%d  "  % bits
        #print(line)
    return score

def generation_evaluation(circuit_gen):
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
    #load("0")
    #circuit00 = PyCirc["0"]
    #score = circuit_evaluation(circuit00)
    #msg = f"score {score}/64"
    #print(msg)
    pass