# Main script for Lab 3 task selection
# Version 1.0
# Developer: Dmitry Melnik
# Date: May 01, 2025

import importlib
from task1.utils import get_valid_input, handle_exception

def run_task(task_num):
    """Run the selected task's main function."""
    try:
        module = importlib.import_module(f"task{task_num}.main")
        module.main()
    except ImportError:
        print(f"Task {task_num} is not implemented yet.")
    except Exception as e:
        handle_exception(e)

def main():
    while True:
        print("\nLab 3 Task Selection")
        print("1. Task 1: Student Management")
        print("2. Task 2: Text Analysis")
        print("3. Task 3: Sequence Analysis and Plotting")
        print("4. Task 4: Geometric Shape (Triangle)")
        print("5. Task 5: Matrix Analysis with NumPy")
        print("6. Task 6: Data Analysis with Pandas")
        print("7. Exit")
        choice = get_valid_input("Enter task number (1-7): ", 1, 7)

        if choice == 7:
            print("Exiting...")
            break
        else:
            run_task(choice)

if __name__ == "__main__":
    main()