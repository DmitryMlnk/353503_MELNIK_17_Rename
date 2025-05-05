# Main testing module for Lab 3 - Task 3
# Developer: Dmitry Melnik
# Date: May 02, 2025

from task3.sequence_analyzer import calculate_series, analyze_sequence
from task3.utils import get_valid_input, handle_exception
import numpy as np


def main():
    while True:
        print("\nTask 3: Sequence Analysis and Plotting")
        print("1. Analyze and plot cosine series")
        print("2. Back to Task Selection")
        choice = get_valid_input("Enter your choice (1-2): ", 1, 2)

        try:
            if choice == 1:
                # Let user define the range and number of points
                num_points = get_valid_input("Enter the number of points (e.g., 10): ", 1, 1000)
                x_start = float(input("Enter the start value of x (e.g., 0): "))
                x_end = float(input("Enter the end value of x (e.g., 1): "))
                x = np.linspace(x_start, x_end, num_points)

                # Get the number of terms for the series
                n_max = get_valid_input("Enter the number of terms (n_max, e.g., 5): ", 1, 20)

                # Calculate series and exact function
                fx = calculate_series(x, n_max)
                math_fx = np.cos(x)
                eps = np.abs(fx - math_fx)

                # Analyze and plot
                stats = analyze_sequence(x, range(n_max + 1), fx, math_fx, eps)
                print("\nStatistical Analysis:")
                for key, value in stats.items():
                    print(f"{key}: {value}")
                print("Plot saved as 'task3/series_plot.png'")
            elif choice == 2:
                break
        except Exception as e:
            handle_exception(e)


if __name__ == "__main__":
    main()