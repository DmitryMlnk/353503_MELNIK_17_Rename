# Sequence analysis and plotting module for Lab 3 - Task 3
# Developer: Dmitry Melnik
# Date: May 02, 2025

import numpy as np
import matplotlib.pyplot as plt
import math


class DataProcessor:
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        """Get the data array."""
        return self._data

    @data.setter
    def data(self, value):
        """Set the data array."""
        if not isinstance(value, (list, np.ndarray)):
            raise TypeError("Data must be a list or numpy array")
        self._data = np.array(value)

    def __str__(self):
        """String representation of the data processor."""
        return f"DataProcessor with {len(self._data)} elements"


class SequenceAnalyzer(DataProcessor):
    _analysis_count = 0  # Static attribute

    def __init__(self, data):
        super().__init__(data)
        self._stats = {}  # Dynamic attribute
        SequenceAnalyzer._analysis_count += 1

    @property
    def stats(self):
        """Get the statistical results."""
        return self._stats

    def mean(self):
        """Calculate the mean of the sequence."""
        return np.mean(self.data)

    def median(self):
        """Calculate the median of the sequence."""
        return np.median(self.data)

    def mode(self):
        """Calculate the mode of the sequence."""
        values, counts = np.unique(self.data, return_counts=True)
        return values[np.argmax(counts)]

    def variance(self):
        """Calculate the variance of the sequence."""
        return np.var(self.data)

    def std_dev(self):
        """Calculate the standard deviation of the sequence."""
        return np.std(self.data)

    def __lt__(self, other):
        """Polymorphism: Compare analyzers by mean value."""
        if not isinstance(other, SequenceAnalyzer):
            return NotImplemented
        return self.mean() < other.mean()

    def __repr__(self):
        """Detailed string representation."""
        return f"SequenceAnalyzer(data_length={len(self.data)}, stats={self._stats})"

    @classmethod
    def get_analysis_count(cls):
        """Class method to get total analysis count."""
        return cls._analysis_count

    def plot_series(self, x, fx, math_fx, eps):
        """Plot series and math function with annotations."""
        plt.figure(figsize=(10, 6))
        plt.plot(x, fx, 'b-', label='Series F(x) (Taylor)')
        plt.plot(x, math_fx, 'r--', label='Math F(x) (cos(x))')
        plt.xlabel('x')
        plt.ylabel('F(x)')
        plt.title('Taylor Series Approximation of cos(x) vs Actual cos(x)')
        plt.legend()
        plt.grid(True)

        # Annotate the maximum error point
        max_eps_idx = np.argmax(eps)
        plt.annotate(f'Max Error: {eps[max_eps_idx]:.4f}',
                     xy=(x[max_eps_idx], fx[max_eps_idx]),
                     xytext=(x[max_eps_idx] + 0.5, fx[max_eps_idx] + 0.5),
                     arrowprops=dict(facecolor='black', shrink=0.05))

        plt.savefig('task3/series_plot.png')
        plt.close()


def calculate_series(x, n_max):
    """Calculate the Taylor series approximation of cos(x) for given x and n_max."""
    fx = np.zeros_like(x, dtype=float)
    for n in range(n_max + 1):
        term = (-1) ** n * x ** (2 * n) / math.factorial(2 * n)
        fx += term
    return fx


def analyze_sequence(x, n, fx, math_fx, eps):
    """Analyze sequence and generate plot."""
    analyzer = SequenceAnalyzer(fx)
    analyzer._stats = {
        'Mean': round(analyzer.mean(), 4),
        'Median': round(analyzer.median(), 4),
        'Mode': round(analyzer.mode(), 4),
        'Variance': round(analyzer.variance(), 4),
        'Std Dev': round(analyzer.std_dev(), 4),
        'Max Absolute Error': round(np.max(eps), 4)
    }
    analyzer.plot_series(x, fx, math_fx, eps)
    return analyzer._stats