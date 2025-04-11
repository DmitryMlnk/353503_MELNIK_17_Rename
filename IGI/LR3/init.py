import random
import math

def init_by_user():
    """Initialize x and eps based on user input."""
    while True:
        try:
            x = float(input("Enter x (in radians): "))
            break
        except ValueError:
            print("Please enter a valid number for x!")

    while True:
        try:
            eps = float(input("Enter eps (e.g., 0.0001): "))
            if eps <= 0:
                raise ValueError("eps must be positive!")
            break
        except ValueError as e:
            print(f"Error: {e}. Try again.")
    return x, eps

def init_by_rand():
    """Initialize x and eps with random values."""
    x = random.uniform(-2 * math.pi, 2 * math.pi)
    eps = random.choice([1e-3, 1e-4, 1e-5, 1e-6])
    print(f"Generated x: {x}, eps: {eps}")
    return x, eps

def input_integer_list():
    """Input integer list from user with validation."""
    numbers = []
    print("Enter integers (empty line to finish):")
    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                if not numbers:
                    print("List cannot be empty!")
                    continue
                break
            numbers.append(int(user_input))
        except ValueError:
            print("Please enter a valid integer!")
    return numbers

def init_integer_list_by_generator():
    """Init integer list using generator."""
    for number in range(1, 100):
        yield number * random.randint(1, 2)