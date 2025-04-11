def log_execution(func):
    """Decorator to log function execution."""
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"{func.__name__} completed.")
        return result
    return wrapper

def get_valid_choice(prompt, min_val, max_val):
    """Get a valid integer choice within a range."""
    while True:
        try:
            choice = int(input(prompt))
            if not min_val <= choice <= max_val:
                raise ValueError(f"Choice must be between {min_val} and {max_val}!")
            return choice
        except ValueError as e:
            print(f"Error: {e}. Try again.")

def rerun_program():
    """Ask if the user wants to rerun the program."""
    while True:
        choice = input("Run again? (yes/no): ").lower().strip()
        if choice in ['yes', 'no']:
            return choice == 'yes'
        print("Please enter 'yes' or 'no'.")

def print_table(x, n, computed_cos, math_cos, eps):
    """Print cosine computation results in plain table-like format (no borders)."""
    print("\nCosine computation results:")
    print(f"{'x':^10} {'n':^10} {'F(x)':^10} {'Math F(x)':^15} {'eps':^12}")
    print(f"{x:^10.4f} {n:^10d} {computed_cos:^10.4f} {math_cos:^15.4f} {eps:^12f}")

def print_analysis_results(text, letters, digits):
    """Print text analysis results in plain format."""
    print("\nText analysis results:")
    print(f"Text (first 20 characters): {text[:20]}")
    if len(text) > 20:
        print("(text truncated)")
    print(f"Number of letters: {letters}")
    print(f"Number of digits: {digits}")

def print_string_analysis(vowel_count, double_letters, sorted_words):
    """Print string analysis results in plain format."""
    print("\nString analysis results:")
    print(f"a) Words starting with a vowel: {vowel_count}")

    print("\nb) Words with double letters:")
    if double_letters:
        for pos, word in double_letters:
            print(f"  Position: {pos}, Word: {word}")
    else:
        print("  No words with double letters found.")

    print("\nc) Words in alphabetical order:")
    print(", ".join(sorted_words))

def print_list_results(numbers, product, sum_between):
    """Print integer list processing results in plain format."""
    print("\nList processing results:")
    print(f"Input list: {numbers}")
    print(f"Product of even elements at even indices: {product}")
    print(f"Sum between first and last non-zero elements: {sum_between}")
