import os

from geometric_lib.circle import area, perimeter
def calc(x):
    a = area(float(x))
    b = perimeter(float(x))
    print("area: ", a)
    print("perimeter: ", b)

if __name__ == '__main__':
    y = os.getenv('SCRIPT_INPUT')
    calc(y)
