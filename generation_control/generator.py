import os
import shutil

from constants import EMBRYO, GENERATION_SIZE

def init_gen(path):
    # create generation 0 directory
    gen0 = os.path.join(path, "gen0")
    os.makedirs(gen0)

    # copy embryo into generation 0
    for i in range(GENERATION_SIZE):
        i_str = str(i)
        new_circuit = os.path.join(gen0, i_str)
        shutil.copy2(EMBRYO, new_circuit)

    pass

def generate(path, gen_count, parent):

    pass
