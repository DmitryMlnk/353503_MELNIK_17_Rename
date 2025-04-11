# Lab Work #3
# Developer: Dmitry Melnik
# Date: April 8, 2025
# Purpose: Implement various computational tasks including cosine series, text analysis, and list processing

from logic import *
from init import *
from utils import *


def run_cos_computation():
    """Execute cosine computation with user or random input."""
    choice = get_valid_choice("Enter 1 for User Input, 2 for Random: ", 1, 2)
    x, eps = init_by_user() if choice == 1 else init_by_rand()
    computed_cos, terms_used, math_cos = compute_cos_series(x, eps)
    print_table(x, terms_used, computed_cos, math_cos, eps)


@log_execution
def run_odd_counter():
    """Execute odd number counting functionality."""
    count, odd_sum = count_odd_numbers()
    print(f"\nOdd Number Counter Results:")
    print(f"Count of odd numbers: {count}")
    print(f"Sum of odd numbers: {odd_sum}")


def run_text_analyzer():
    """Execute text analysis functionality."""
    print("\nEnter text to analyze (empty line to finish):")
    while True:
        text = input("> ").strip()
        if not text:
            print("No text entered!")
            continue
        break
    letters, digits = analyze_text(text)
    print_analysis_results(text, letters, digits)


def run_string_analyzer():
    """Execute string analysis functionality with predefined text."""
    text = ("So she was considering in her own mind, as well as she could, "
            "for the hot day made her feel very sleepy and stupid, whether "
            "the pleasure of making a daisy-chain would be worth the trouble "
            "of getting up and picking the daisies, when suddenly a White "
            "Rabbit with pink eyes ran close by her.")
    print("\nAnalyzing text:")
    print(text)
    vowel_count, double_letters, sorted_words = analyze_string(text)
    print_string_analysis(vowel_count, double_letters, sorted_words)


def run_list_processor():
    """Execute integer list processing functionality."""
    choice = get_valid_choice("Enter 1 for User Input, 2 for Random: ", 1, 2)
    numbers = []
    if choice == 1:
        numbers = input_integer_list()
    else:
        for number in init_integer_list_by_generator():
            numbers.append(number)

    product, sum_between = process_integer_list(numbers)
    print_list_results(numbers, product, sum_between)


def main():
    """Main program loop with menu selection."""
    options = {
        1: ("Cosine Computation", run_cos_computation),
        2: ("Odd Number Counter", run_odd_counter),
        3: ("Text Analyzer", run_text_analyzer),
        4: ("String Analyzer", run_string_analyzer),
        5: ("Integer List Processor", run_list_processor)
    }

    while True:
        print("\nWelcome to the Multi-Function Program!")
        for key, (desc, _) in options.items():
            print(f"{key} - {desc}")

        try:
            choice = get_valid_choice(f"Enter 1-{len(options)}: ", 1, len(options))
            _, func = options[choice]
            func()
        except ValueError as e:
            print(f"Input Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

        if not rerun_program():
            print("Thank you for using the program!")
            break


if __name__ == "__main__":
    main()