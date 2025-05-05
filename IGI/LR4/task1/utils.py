# Utility functions for Lab 3 - Task 1
# Developer: Dmitry Melnik
# Date: May 01, 2025

def get_valid_input(prompt, min_val=None, max_val=None):
    """Get valid integer input with range validation."""
    while True:
        try:
            value = input(prompt)
            value = int(value)
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