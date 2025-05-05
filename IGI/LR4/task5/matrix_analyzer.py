# Matrix analysis using NumPy for Lab 3 - Task 5
# Developer: Dmitry Melnik
# Date: May 03, 2025

import numpy as np

class MatrixProcessor:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._matrix = None

    @property
    def matrix(self):
        """Get the matrix."""
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        """Set the matrix with validation."""
        if not isinstance(value, np.ndarray):
            raise TypeError("Matrix must be a NumPy array")
        self._matrix = value

    def __str__(self):
        """String representation of the matrix processor."""
        return f"MatrixProcessor({self._rows}x{self._cols})"

class MatrixAnalyzer(MatrixProcessor):
    _analysis_count = 0  # Static attribute

    def __init__(self, rows, cols):
        super().__init__(rows, cols)
        self._results = {}  # Dynamic attribute
        MatrixAnalyzer._analysis_count += 1
        self._generate_matrix()

    def _generate_matrix(self):
        """Generate a random integer matrix using NumPy."""
        # Using np.random.randint to create an array of random integers
        self._matrix = np.random.randint(low=1, high=100, size=(self._rows, self._cols))

    def demonstrate_numpy_features(self):
        """Demonstrate various NumPy functionalities."""
        # 1. Creating arrays with array() and arange()
        array1 = np.array([1, 2, 3, 4])
        array2 = np.arange(0, 10, 2)

        # 2. Functions for creating arrays of specific types
        zeros_array = np.zeros((2, 3))
        ones_array = np.ones((2, 3))
        identity_matrix = np.eye(3)

        # 3. Indexing and slicing
        sliced_matrix = self._matrix[0:2, 1:3]  # First two rows, columns 2-3

        # 4. Operations with arrays (universal functions)
        squared_matrix = np.square(self._matrix)
        sum_matrix = np.add(self._matrix, 10)

        return {
            "Array1 (array)": array1,
            "Array2 (arange)": array2,
            "Zeros Array": zeros_array,
            "Ones Array": ones_array,
            "Identity Matrix": identity_matrix,
            "Sliced Matrix": sliced_matrix,
            "Squared Matrix (first row)": squared_matrix[0],
            "Sum Matrix (first row)": sum_matrix[0]
        }

    def statistical_analysis(self):
        """Perform statistical analysis on the matrix."""
        # Mathematical and statistical operations
        mean_val = np.mean(self._matrix)
        median_val = np.median(self._matrix)
        corr_coef = np.corrcoef(self._matrix.flatten(), self._matrix.flatten())[0, 1]
        variance_val = np.var(self._matrix)
        std_dev = np.std(self._matrix)

        # Task-specific: Count elements greater than mean and their standard deviation
        elements_above_mean = self._matrix[self._matrix > mean_val]
        count_above_mean = len(elements_above_mean)

        # Standard deviation using NumPy
        std_dev_above_mean = np.std(elements_above_mean) if count_above_mean > 0 else 0

        # Standard deviation using manual formula: sqrt(sum((x - mean)^2) / N)
        if count_above_mean > 0:
            mean_above = np.mean(elements_above_mean)
            squared_diff_sum = np.sum((elements_above_mean - mean_above) ** 2)
            manual_std_dev = np.sqrt(squared_diff_sum / count_above_mean)
        else:
            manual_std_dev = 0

        return {
            "Matrix": self._matrix,
            "Mean": mean_val,
            "Median": median_val,
            "Correlation Coefficient": corr_coef,
            "Variance": variance_val,
            "Standard Deviation (all)": std_dev,
            "Elements Above Mean": elements_above_mean,
            "Count Above Mean": count_above_mean,
            "Std Dev (Above Mean, NumPy)": round(std_dev_above_mean, 2),
            "Std Dev (Above Mean, Manual)": round(manual_std_dev, 2)
        }

    def __lt__(self, other):
        """Polymorphism: Compare analyzers by mean value of matrices."""
        if not isinstance(other, MatrixAnalyzer):
            return NotImplemented
        return np.mean(self._matrix) < np.mean(other.matrix)

    def __repr__(self):
        """Detailed string representation."""
        return f"MatrixAnalyzer({self._rows}x{self._cols}, results={self._results})"

    @classmethod
    def get_analysis_count(cls):
        """Class method to get total analysis count."""
        return cls._analysis_count