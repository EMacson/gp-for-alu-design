import os
import shutil

from constants import EMBRYO, GENERATION_SIZE

def init_gen(path):
    # create generation 0 directory
    gen0 = os.path.join(path, "gen0")
    os.makedirs(gen0)

    # copy embryo into generation 0
    with open(EMBRYO, "r") as file:
        content = file.read()
    for i in range(GENERATION_SIZE):
        i_str = str(i)
        new_circuit_name = "define(0/" + i_str + ")"
        modified_content = content.replace('Define("embryo")', new_circuit_name)
        new_circuit_file = os.path.join(gen0, i_str)
        with open(new_circuit_file, "w") as file:
            file.write(modified_content)
        #shutil.copy2(EMBRYO, new_circuit)

    pass

def generate(path, gen_count, parent):

    pass
