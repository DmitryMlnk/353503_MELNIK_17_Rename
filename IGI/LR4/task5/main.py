# Main testing module for Lab 3 - Task 5
# Developer: Dmitry Melnik
# Date: May 03, 2025

from task5.matrix_analyzer import MatrixAnalyzer
from task5.utils import get_valid_input, handle_exception

def main():
    while True:
        print("\nTask 5: Matrix Analysis with NumPy")
        print("1. Analyze a random matrix")
        print("2. Back to Task Selection")
        choice = get_valid_input("Enter your choice (1-2): ", 1, 2)

        try:
            if choice == 1:
                rows = get_valid_input("Enter number of rows (1-10): ", 1, 10)
                cols = get_valid_input("Enter number of columns (1-10): ", 1, 10)

                analyzer = MatrixAnalyzer(rows, cols)

                # Demonstrate NumPy features
                numpy_features = analyzer.demonstrate_numpy_features()
                print("\nDemonstrating NumPy Features:")
                for key, value in numpy_features.items():
                    print(f"{key}: {value}")

                # Perform statistical analysis
                stats = analyzer.statistical_analysis()
                print("\nStatistical Analysis:")
                for key, value in stats.items():
                    print(f"{key}: {value}")
            elif choice == 2:
                break
        except Exception as e:
            handle_exception(e)

if __name__ == "__main__":
    main()