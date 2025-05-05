# Main testing module for Lab 3 - Task 4
# Developer: Dmitry Melnik
# Date: May 02, 2025

from task4.shapes import Triangle
from task4.utils import get_valid_float, get_valid_color, get_valid_input, handle_exception

def main():
    while True:
        print("\nTask 4: Geometric Shape (Triangle Inscribed in Circle)")
        print("1. Create and plot a triangle")
        print("2. Back to Task Selection")
        choice = get_valid_input("Enter your choice (1-2): ", 1, 2)

        try:
            if choice == 1:
                radius = get_valid_float("Enter the radius of the circumscribed circle: ")
                color = get_valid_color("Enter the color (red, blue, green, yellow, purple, orange, black): ")
                label = input("Enter a label for the triangle: ")

                triangle = Triangle(radius, color)
                print("\nTriangle Details:")
                print(triangle.get_details())

                triangle.plot(label, "triangle_plot.png")
                print("Plot saved as 'triangle_plot.png'")
            elif choice == 2:
                break
        except Exception as e:
            handle_exception(e)

if __name__ == "__main__":
    main()