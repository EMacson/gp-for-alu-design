import os
from datetime import datetime

from constants import MAIN_DIR, CIRCUITS_DIR, EMBRYO, MAX_SCORE
#import constants
from generation_control.generator import init_gen, generate_gen
from generation_control.evaluator import circuit_evaluation, generation_evaluation
from generation_control.crossover import crossover
from mutation.topology import topology


def main():
    # create run dir
    # might need to create gitignore for new circuit directories
    #main_dir = os.path.dirname(os.path.abspath(__file__))
    #circuit_dir = os.path.join(main_dir, "circuits")
    dev = False
    if dev == False:
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

    #for i in range(1):
    while True:
        # run selector
        #circuit_gen = os.path.join(circuit_gen, str(gen_count))
        parents = generation_evaluation(circuit_gen, gen_count)
        msg = f"\n\nparent 1: {parents["circ1"][0]} parent 2: {parents["circ2"][0]}"
        #score = circuit_evaluation(circuit0, "0")
        #msg = f"score {score}/64"
        print(msg)
        
        # teriminate?
        if parents["circ1"][1] == MAX_SCORE:
            # TODO: print final circuit
            break

        # cross over
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
        #parents = generation_evaluation(circuit_gen, gen_count)

        # loop back

    pass

if __name__ == "__main__":
    main()