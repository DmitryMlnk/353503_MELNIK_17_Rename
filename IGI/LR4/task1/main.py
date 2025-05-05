# Main testing module for Lab 3 - Task 1
# Developer: Melnik Dmitry
# Date: May 01, 2025

from task1.student import Student, StudentManager
from task1.file_handler import FileHandler, PickleHandler
from task1.utils import get_valid_input, handle_exception

def main():
    manager = StudentManager()
    csv_handler = FileHandler("./task1/students.csv")
    pickle_handler = PickleHandler("./task1/students.pkl")

    # Sample data
    try:
        manager.add_student(Student("Ivan I.I.", 15, 5, 2005))
        manager.add_student(Student("Maria M.M.", 20, 6, 2006))
        manager.add_student(Student("Alex A.A.", 10, 5, 2004))
    except Exception as e:
        handle_exception(e)
        return

    while True:
        print("\nTask 1: Student Management System")
        print("1. Save to CSV")
        print("2. Save to Pickle")
        print("3. Load from Pickle")
        print("4. Filter by month")
        print("5. Sort students")
        print("6. Back to Task Selection")
        choice = get_valid_input("Enter your choice (1-6): ", 1, 6)

        try:
            if choice == 1:
                csv_handler.save_to_csv(manager.students)
                print("Students saved to students.csv")
            elif choice == 2:
                pickle_handler.save_to_pickle(manager.students)
                print("Students saved to students.pkl")
            elif choice == 3:
                manager.students = pickle_handler.load_from_pickle()
                print("Students loaded from students.pkl")
            elif choice == 4:
                month = get_valid_input("Enter month (1-12): ", 1, 12)
                students = manager.get_students_by_month(month)
                print(f"Students born in month {month}:")
                for student in students:
                    print(student)
            elif choice == 5:
                sorted_students = manager.sort_students()
                print("Students sorted by birth date:")
                for student in sorted_students:
                    print(student)
            elif choice == 6:
                break
        except Exception as e:
            handle_exception(e)

if __name__ == "__main__":
    main()