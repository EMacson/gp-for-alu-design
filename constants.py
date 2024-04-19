import os

# GP definitions
GENERATION_SIZE = 100
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
CIRCUITS_DIR = os.path.join(MAIN_DIR, "circuits")
EMBRYO = os.path.join(MAIN_DIR, "embryo.py")
MUTATION_RATE = 50

# circuit definitions
OPERAND_SIZE = 2
OPCODE_SIZE = 2
CARRY_IN_SIZE = 1
INPUT_SIZE = OPERAND_SIZE + OPERAND_SIZE + CARRY_IN_SIZE
B_OUT = [1,1,0,0,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,1,1,0,1,0,0,1]
CARRY_OUT = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1]
OUTPUT_SIZE = 2
MAX_SCORE = 64
