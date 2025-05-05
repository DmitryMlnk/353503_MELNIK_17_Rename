# Handling file operations for Lab 3 - Task 1
# Developer: Melnik Dmitry
# Date: May 01, 2025

import csv
import pickle
from task1.student import Student

class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def save_to_csv(self, students):
        """Save student list to CSV file."""
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Full Name', 'Day', 'Month', 'Year'])
            for student in students:
                writer.writerow([student.full_name, student._day, student._month, student._year])

    def load_from_csv(self):
        """Load students from CSV file."""
        students = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                students.append(Student(row[0], int(row[1]), int(row[2]), int(row[3])))
        return students

class PickleHandler(FileHandler):
    def save_to_pickle(self, students):
        """Save student list to Pickle file."""
        with open(self.filename, 'wb') as file:
            pickle.dump(students, file)

    def load_from_pickle(self):
        """Load students from Pickle file."""
        with open(self.filename, 'rb') as file:
            return pickle.load(file)