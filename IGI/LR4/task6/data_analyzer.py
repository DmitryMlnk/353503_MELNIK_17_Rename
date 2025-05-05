# Data analysis using Pandas for Lab 3 - Task 6
# Developer: Melnik Dmitry
# Date: May 03, 2025


import pandas as pd
from io import StringIO

class DataProcessor:
    def __init__(self, data_content):
        self._data_content = data_content
        self._df = None

    @property
    def dataframe(self):
        """Get the DataFrame."""
        return self._df

    @dataframe.setter
    def dataframe(self, value):
        """Set the DataFrame with validation."""
        if not isinstance(value, pd.DataFrame):
            raise TypeError("Data must be a Pandas DataFrame")
        self._df = value

    def __str__(self):
        """String representation of the data processor."""
        return f"DataProcessor(data_rows={len(self._data_content.splitlines()) - 1})"

class DataAnalyzer(DataProcessor):
    _analysis_count = 0  # Static attribute

    def __init__(self, data_content):
        super().__init__(data_content)
        self._results = {}  # Dynamic attribute
        DataAnalyzer._analysis_count += 1
        self._load_data()

    def _load_data(self):
        """Load the dataset from string content into a DataFrame."""
        self._df = pd.read_csv(StringIO(self._data_content))

    def demonstrate_pandas_features(self):
        """Demonstrate Pandas Series and DataFrame functionalities."""
        # 2 & 3. Create a Series
        shot_power_series = pd.Series(self._df['Treatment_Cost_USD'].values, name='Treatment_Cost_USD')

        # 4. Display the Series
        print("\nDisplaying Treatment_Cost_USD Series:")
        print(shot_power_series)

        # 5. Access elements using .loc and .iloc
        first_five_loc = shot_power_series.loc[0:4]  # First five elements by label
        first_five_iloc = shot_power_series.iloc[0:4]  # First five elements by position
        print("\nFirst five elements using .loc:")
        print(first_five_loc)
        print("First five elements using .iloc:")
        print(first_five_iloc)

        # 6. Create a DataFrame (already created as self._df)
        subset_df = self._df[['Patient_ID', 'Cancer_Type', 'Cancer_Stage', 'Treatment_Cost_USD']].head()
        print("\nDisplaying subset DataFrame:")
        print(subset_df)

        return shot_power_series, subset_df

    def get_dataframe_info(self):
        """Get detailed information about the DataFrame."""
        info_dict = {
            "Shape": self._df.shape,
            "Columns": list(self._df.columns),
            "Data Types": self._df.dtypes.to_dict(),
            "Memory Usage": self._df.memory_usage(deep=True).sum(),
            "Missing Values": self._df.isnull().sum().to_dict(),
            "Summary Statistics": self._df.describe().to_dict()
        }
        return info_dict

    def statistical_analysis(self):
        """Perform statistical analysis as per the task."""
        max_aggression = self._df['Genetic_Risk'].max()  # Using Genetic_Risk as a proxy for aggression
        min_aggression = self._df['Genetic_Risk'].min()
        max_agg_players = self._df[self._df['Genetic_Risk'] == max_aggression]
        min_agg_players = self._df[self._df['Genetic_Risk'] == min_aggression]
        mean_cost_max_agg = max_agg_players['Treatment_Cost_USD'].mean()
        mean_cost_min_agg = min_agg_players['Treatment_Cost_USD'].mean()
        cost_ratio = mean_cost_max_agg / mean_cost_min_agg if mean_cost_min_agg != 0 else float('inf')
        cost_ratio = round(cost_ratio, 2)

        mean_wage = self._df['Treatment_Cost_USD'].mean()  # Using cost as proxy for wage
        below_avg_cost_players = self._df[self._df['Treatment_Cost_USD'] < mean_wage]
        mean_surv_speed = round(below_avg_cost_players['Survival_Years'].mean(), 2)

        return {
            "Mean Cost (Max Genetic_Risk)": mean_cost_max_agg,
            "Mean Cost (Min Genetic_Risk)": mean_cost_min_agg,
            "Cost Ratio (Max/Min Genetic_Risk)": cost_ratio,
            "Mean Treatment Cost": mean_wage,
            "Mean Survival Years (Below Avg Cost)": mean_surv_speed
        }

    def calculate_metrics(self):
        """Calculate 5 different metrics based on the dataset."""
        metrics = {}

        # Metric 1: Average Treatment Cost by Cancer Type
        avg_cost_by_cancer = self._df.groupby('Cancer_Type')['Treatment_Cost_USD'].mean().round(2)
        metrics['Average_Treatment_Cost_by_Cancer_Type'] = avg_cost_by_cancer.to_dict()

        # Metric 2: Survival Rate by Cancer Stage
        survival_by_stage = self._df.groupby('Cancer_Stage')['Survival_Years'].mean().round(2)
        metrics['Average_Survival_Years_by_Stage'] = survival_by_stage.to_dict()

        # Metric 3: Risk Factor Index (sum of risk factors)
        self._df['Risk_Factor_Index'] = self._df[['Genetic_Risk', 'Air_Pollution', 'Alcohol_Use',
                                               'Smoking', 'Obesity_Level']].sum(axis=1)
        avg_risk_index = self._df['Risk_Factor_Index'].mean().round(2)
        metrics['Average_Risk_Factor_Index'] = avg_risk_index

        # Metric 4: Severity-Adjusted Cost Efficiency
        self._df['Cost_Efficiency'] = self._df['Treatment_Cost_USD'] / self._df['Target_Severity_Score']
        avg_cost_efficiency = self._df['Cost_Efficiency'].mean().round(2)
        metrics['Average_Severity_Adjusted_Cost_Efficiency'] = avg_cost_efficiency

        # Metric 5: Age-Stratified Severity Score
        bins = [0, 30, 50, 70, 100]
        labels = ['0-30', '31-50', '51-70', '71+']
        self._df['Age_Group'] = pd.cut(self._df['Age'], bins=bins, labels=labels, right=False)
        severity_by_age = self._df.groupby('Age_Group', observed=True)['Target_Severity_Score'].mean().round(2)
        metrics['Average_Severity_Score_by_Age_Group'] = severity_by_age.to_dict()

        return metrics

    def __lt__(self, other):
        """Polymorphism: Compare analyzers by DataFrame size."""
        if not isinstance(other, DataAnalyzer):
            return NotImplemented
        return self._df.size < other.dataframe.size

    def __repr__(self):
        """Detailed string representation."""
        return f"DataAnalyzer(data_rows={self._df.shape[0]})"

    @classmethod
    def get_analysis_count(cls):
        """Class method to get total analysis count."""
        return cls._analysis_count