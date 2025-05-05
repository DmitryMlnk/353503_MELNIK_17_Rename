# Utility functions for Lab 3 - Task 4
# Developer: Dmitry Melnik
# Date: May 02, 2025

def get_valid_float(prompt):
    """Get a valid positive float input."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a positive number.")

def get_valid_color(prompt):
    """Get a valid color input."""
    valid_colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'black']
    while True:
        value = input(prompt).lower()
        if value in valid_colors:
            return value
        print(f"Color must be one of {valid_colors}.")

def get_valid_input(prompt, min_val=None, max_val=None):
    """Get valid integer input with range validation."""
    while True:
        try:
            value = int(input(prompt))
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                raise ValueError
            return value
        except ValueError:
            print(f"Please enter a valid number{' between ' + str(min_val) + ' and ' + str(max_val) if min_val or max_val else ''}.")

def handle_exception(exc):
    """Handle specific exceptions with user-friendly messages."""
    if isinstance(exc, ValueError):
        print("Error: Invalid input or data format.")
    elif isinstance(exc, TypeError):
        print("Error: Incorrect type provided.")
    else:
        print("An unexpected error occurred.")