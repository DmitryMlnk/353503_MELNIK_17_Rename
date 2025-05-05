# Geometric shape classes for Lab 3 - Task 4
# Developer: Dmitry Melnik
# Date: May 02, 2025

from abc import ABC, abstractmethod
import math
import matplotlib.pyplot as plt
import numpy as np

class GeometricShape(ABC):
    @abstractmethod
    def area(self):
        """Calculate the area of the shape."""
        pass

    @abstractmethod
    def plot(self, label, filename):
        """Plot the shape and save to file."""
        pass

class Color:
    _valid_colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'black']

    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        """Get the color of the shape."""
        return self._color

    @color.setter
    def color(self, value):
        """Set the color of the shape."""
        if value.lower() not in self._valid_colors:
            raise ValueError(f"Color must be one of {self._valid_colors}")
        self._color = value.lower()

    def __str__(self):
        """String representation of the color."""
        return self._color

class Triangle(GeometricShape):
    _shape_name = "Triangle"  # Class-level field for shape name

    def __init__(self, radius, color):
        self.radius = radius
        self.color_obj = Color(color)
        self._sides = self.calculate_sides()
        self._area = None
        self._calculate_area()

    @property
    def radius(self):
        """Get the radius of the circumscribed circle."""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Set the radius with validation."""
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Radius must be a positive number")
        self._radius = value

    def calculate_sides(self):
        """Calculate the sides of an equilateral triangle inscribed in a circle."""
        # For an equilateral triangle inscribed in a circle, side length = R * sqrt(3)
        side = self.radius * math.sqrt(3)
        return [side, side, side]

    def _calculate_area(self):
        """Calculate the area of the triangle."""
        # Area of equilateral triangle = (side^2 * sqrt(3)) / 4
        side = self._sides[0]
        self._area = (side ** 2 * math.sqrt(3)) / 4

    def area(self):
        """Return the area of the triangle."""
        return self._area

    def get_shape_name(self):
        """Return the name of the shape."""
        return self._shape_name

    def get_details(self):
        """Return a string with the triangle's details."""
        return "Triangle: radius={:>5}, color={:>10}, area={:>10.2f}".format(
            self.radius, self.color_obj.color, self.area()
        )

    def plot(self, label, filename):
        """Plot the triangle inscribed in a circle, fill with color, and save to file."""
        # Coordinates of an equilateral triangle inscribed in a circle of radius R
        theta = np.linspace(0, 2 * np.pi, 3, endpoint=False)
        x = self.radius * np.cos(theta)
        y = self.radius * np.sin(theta)
        x = np.append(x, x[0])  # Close the triangle
        y = np.append(y, y[0])

        # Plot the circle
        circle = plt.Circle((0, 0), self.radius, fill=False, color='black')
        fig, ax = plt.subplots()
        ax.add_patch(circle)

        # Plot and fill the triangle
        ax.fill(x, y, color=self.color_obj.color, alpha=0.5)
        ax.plot(x, y, 'b-')

        # Add label
        ax.text(0, self.radius + 0.1, label, ha='center', va='bottom')

        ax.set_aspect('equal')
        ax.set_xlim(-self.radius - 1, self.radius + 1)
        ax.set_ylim(-self.radius - 1, self.radius + 1)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Triangle Inscribed in Circle')
        plt.grid(True)
        plt.savefig(filename)
        plt.show()
        plt.close()

    def __repr__(self):
        """Detailed string representation."""
        return f"Triangle(radius={self.radius}, color={self.color_obj.color})"

    def __lt__(self, other):
        """Polymorphism: Compare triangles by area."""
        if not isinstance(other, Triangle):
            return NotImplemented
        return self.area() < other.area()