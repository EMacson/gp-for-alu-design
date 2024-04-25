import os
import shutil

from constants import EMBRYO, GENERATION_SIZE

def init_gen(path):
    # create generation 0 directory
    gen0 = os.path.join(path, "0")
    os.makedirs(gen0)

    # copy embryo into generation 0
    with open(EMBRYO, "r") as file:
        content = file.read()
    for i in range(GENERATION_SIZE):
        i_str = str(i)
        new_circuit_file = os.path.join(gen0, i_str+".py")
        shutil.copy2(EMBRYO, new_circuit_file)

def generate_gen(path, gen_count):
    # create new generation directory
    new_gen = os.path.join(path, str(gen_count))
    os.makedirs(new_gen)

    # get parent file path
    parent_file = os.path.join(path, str(gen_count-1))
    parent_file = os.path.join(parent_file, "parent.py")

    for i in range(GENERATION_SIZE):
        new_circuit_file = os.path.join(new_gen, str(i)+".py")
        shutil.copy2(parent_file, new_circuit_file)

