import os
from datetime import datetime

def main():
    # create run dir
    # might need to create gitignore for new circuit directories
    main_dir = os.path.dirname(os.path.abspath(__file__))
    circuit_dir = os.path.join(main_dir, "circuits")
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    subdirectory = current_time_str
    subdirectory_path = os.path.join(circuit_dir, subdirectory)
    os.makedirs(subdirectory_path)

    # create first generation

    # run selector

    # teriminate?

    # cross over

    # create new generation

    # mutate

    # loop back
    pass

if __name__ == "__main__":
    main()