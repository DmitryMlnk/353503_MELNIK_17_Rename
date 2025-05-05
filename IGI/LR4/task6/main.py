# Main testing module for Lab 3 - Dop task
# Developer: Melnik Dmitry
# Date: May 03, 2025

from task6.data_analyzer import DataAnalyzer
from task1.utils import get_valid_input, handle_exception

def main():
    # Use the provided dataset content
    with open('./task6/global_cancer_patients_2015_2024.csv', 'r', encoding='utf-8') as file:
        data_content = file.read()

    while True:
        print("\nTask 6: Data Analysis with Pandas")
        print("1. Analyze cancer patient dataset")
        print("2. Back to Task Selection")
        choice = get_valid_input("Enter your choice (1-2): ", 1, 2)

        try:
            if choice == 1:
                analyzer = DataAnalyzer(data_content)

                # Demonstrate Pandas features
                series, subset_df = analyzer.demonstrate_pandas_features()

                # Get DataFrame information
                df_info = analyzer.get_dataframe_info()
                print("\nDataFrame Information:")
                for key, value in df_info.items():
                    print(f"{key}: {value}")

                # Perform statistical analysis
                stats = analyzer.statistical_analysis()
                print("\nStatistical Analysis:")
                for key, value in stats.items():
                    print(f"{key}: {value}")

                # Calculate and display 5 metrics
                metrics = analyzer.calculate_metrics()
                print("\nCustom Metrics:")
                for metric_name, metric_value in metrics.items():
                    print(f"{metric_name}: {metric_value}")

            elif choice == 2:
                break
        except Exception as e:
            handle_exception(e)

if __name__ == "__main__":
    main()