# Managing student data for Lab 3 - Task 1
# Developer: Melnik Dmitry
# Date: May 01, 2025

from datetime import datetime

class LogMixin:
    """Mixin for logging operations using print."""
    def log_action(self, action):
        """Log action using print."""
        print(f"Action: {action} performed on {self.__class__.__name__}")

class Person:
    def __init__(self, full_name):
        self._full_name = full_name

    @property
    def full_name(self):
        """Get the full name of the person."""
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        """Set the full name of the person."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Full name must be a non-empty string")
        self._full_name = value

    def __str__(self):
        """String representation of the person."""
        return self._full_name

class Student(Person):
    _total_students = 0  # Static attribute

    def __init__(self, full_name, day, month, year):
        super().__init__(full_name)
        self._day = day
        self._month = month
        self._year = year
        self._birth_date = None  # Dynamic attribute
        Student._total_students += 1
        self._set_birth_date()

    @property
    def birth_date(self):
        """Get the birth date as a datetime object."""
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        """Set the birth date (not directly used, handled by _set_birth_date)."""
        raise AttributeError("Use day, month, year to set birth date")

    def _set_birth_date(self):
        """Set the birth date based on day, month, year."""
        try:
            self._birth_date = datetime(self._year, self._month, self._day)
        except ValueError as e:
            raise ValueError("Invalid date values") from e

    def __lt__(self, other):
        """Polymorphism: Compare students by birth date for sorting."""
        if not isinstance(other, Student):
            return NotImplemented
        return self._birth_date < other._birth_date

    def __repr__(self):
        """Special method for detailed string representation."""
        return f"Student(full_name='{self._full_name}', birth_date={self._birth_date.strftime('%Y-%m-%d')})"

class StudentManager(LogMixin):
    def __init__(self):
        self.students = []

    def add_student(self, student):
        """Add a student to the manager."""
        if not isinstance(student, Student):
            raise TypeError("Only Student objects can be added")
        self.students.append(student)
        self.log_action(f"Added student {student.full_name}")

    def get_students_by_month(self, month):
        """Filter students by birth month."""
        students = [s for s in self.students if s._month == month]
        self.log_action(f"Filtered students by month {month}")
        return students

    def sort_students(self):
        """Sort students by birth date."""
        sorted_students = sorted(self.students)
        self.log_action("Sorted students by birth date")
        return sorted_students

    @property
    def total_students(self):
        """Get the total number of students (using property)."""
        return Student._total_students