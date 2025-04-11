import math


def compute_cos_series(x, eps, max_iterations=500):
    """Compute cos(x) using Taylor series expansion."""
    computed_cos, term, n = 0.0, 1.0, 0
    while abs(term) >= eps and n < max_iterations:
        computed_cos += term
        n += 1
        term = (-1) ** n * (x ** (2 * n)) / math.factorial(2 * n)

    if n == max_iterations:
        print("Warning: Maximum iterations reached. Result may not be precise.")
    return computed_cos, n, math.cos(x)


def count_odd_numbers():
    """Count and sum odd natural numbers until 0 is entered."""
    count, odd_sum = 0, 0
    while True:
        try:
            num = int(input("Enter a number (0 to stop): "))
            if num == 0:
                break
            if num < 0:
                print("Please enter natural numbers only!")
                continue
            if num % 2 == 1:
                count += 1
                odd_sum += num
        except ValueError:
            print("Please enter a valid integer!")
    return count, odd_sum


def analyze_text(text):
    """Count Latin alphabet letters and digits in text."""
    letter_count, digit_count = 0, 0
    for char in text:
        if char.isalpha() and char.isascii():
            letter_count += 1
        elif char.isdigit():
            digit_count += 1
    return letter_count, digit_count


def analyze_string(text):
    """Analyze text for vowel-starting words, double letters, and alphabetical order."""
    words = text.replace(",", " ").split()

    vowels = {'a','e','i','o','u'}
    vowel_start_count = sum(1 for word in words if word[0].lower() in vowels)
    double_letter_words = [(i + 1, word) for i, word in enumerate(words)
                           for j in range(len(word) - 1) if word[j] == word[j + 1]]
    sorted_words = sorted(words)

    return vowel_start_count, double_letter_words, sorted_words


def process_integer_list(numbers):
    """Process list for even elements product and sum between non-zero elements."""
    product = 1
    found_even = False
    first_non_zero_index = -1
    last_non_zero_index = -1

    for i, num in enumerate(numbers):
        if i % 2 == 0 and num % 2 == 0:
            product *= abs(num)
            found_even = True

        if num != 0:
            if first_non_zero_index == -1:
                first_non_zero_index = i
            last_non_zero_index = i

    final_product = product if found_even else 0

    if first_non_zero_index == -1 or last_non_zero_index <= first_non_zero_index + 1:
        sum_between = 0
    else:
        sum_between = sum(numbers[first_non_zero_index + 1:last_non_zero_index])

    return final_product, sum_between