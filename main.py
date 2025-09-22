"""
main.py - Entry point for IS601 Proj1
"""

from calculator import add, subtract, multiply, divide

def main():
    print("Simple Calculator")
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    print(f"{a} + {b} = {add(a, b)}")
    print(f"{a} - {b} = {subtract(a, b)}")
    print(f"{a} * {b} = {multiply(a, b)}")
    try:
        print(f"{a} / {b} = {divide(a, b)}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
