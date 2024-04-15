import os
from datetime import datetime

from constants import MAIN_DIR, CIRCUITS_DIR, EMBRYO
#import constants
from generation_control.generator import generate, init_gen

def main():
    # create run dir
    # might need to create gitignore for new circuit directories
    #main_dir = os.path.dirname(os.path.abspath(__file__))
    #circuit_dir = os.path.join(main_dir, "circuits")
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    subdirectory = current_time_str
    subdirectory_path = os.path.join(CIRCUITS_DIR, subdirectory)
    os.makedirs(subdirectory_path)

    # create first generation
    gen_count = 0
    init_gen(subdirectory_path)

    # run selector

    # teriminate?

    # cross over

    # create new generation

    # mutate

    # loop back
    pass

if __name__ == "__main__":
    main()