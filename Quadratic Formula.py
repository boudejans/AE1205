import math

print("Solve for ax^2 + bx + c = 0")
a = int(input("Enter a: "))
b = int(input("Enter b: "))
c = int(input("Enter c: "))

# Linear
if a == 0:
    x = -c/b
    print("Only one solution: " + str(x))
else: # Quadratic
    if (b**2 - 4*a*c) < 0:
        print("Solutions are imaginary")
    else:
        x1 = (-b+math.sqrt(b**2 - 4*a*c))/(2*a)
        x2 = (-b-math.sqrt(b**2 - 4*a*c))/(2*a)
        print("The two solutions: " + str(x1) + ", " + str(x2))