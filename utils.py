import random
import sys

def redirect_print():
    sys.stdout = open('NUL', "w")

def restore_print():
    sys.stdout.close()
    sys.stdout = sys.__stdout__

def select_gate():
    gate_types = ["and2", "or2", "not"]
    random_number = random.randint(0, 2)

    return gate_types[random_number]

def gate_select():
    pass

def get_gate():
    pass