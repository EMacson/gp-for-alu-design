import os
import threading
from datetime import datetime

from constants import MAIN_DIR, CIRCUITS_DIR, EMBRYO, MAX_SCORE
from utils import redirect_print, restore_print

#import constants
from generation_control.generator import init_gen, generate_gen
from generation_control.evaluator import circuit_evaluation, generation_evaluation
from generation_control.crossover import crossover
from mutation.topology import topology
from mutation.rewire import rewire
from display import display

def main():
    # create run dir    
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    subdirectory = current_time_str
    subdirectory_path = os.path.join(CIRCUITS_DIR, subdirectory)
    os.makedirs(subdirectory_path)

    # create first generation
    gen_count = 0
    init_gen(subdirectory_path)
    print(subdirectory_path)
    circuit_gen = os.path.join(CIRCUITS_DIR, subdirectory_path)

    parents = []

    for i in range(500):
    #while True:
        # run selector
        parents = generation_evaluation(circuit_gen, gen_count)
        msg = f"\n\nparent 1 circuit number: {parents["circ1"][0]} parent 2 circuit number: {parents["circ2"][0]}"
        print(msg)
        
        # teriminate?
        if parents["circ1"][1] == MAX_SCORE:
            break

        # crossover
        # creates parent.py circuit in current generation
        # parent.py used to generate the next generation
        p1 = str(parents["circ1"][0])
        p2 = str(parents["circ2"][0])
        crossover(circuit_gen, gen_count, p1, p2)

        # create new generation
        gen_count = gen_count + 1
        generate_gen(circuit_gen, gen_count)

        # mutate
        topology(circuit_gen, gen_count)
        rewire(circuit_gen, gen_count)


    # create final circuit diagram
    display(str(parents["circ1"][0]), circuit_gen, str(gen_count))


if __name__ == "__main__":
    main()