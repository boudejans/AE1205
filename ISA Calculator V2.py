import math

# Standard Values
g0 = 9.80665
R = 287
T0 = 288.15
p0 = 101325

ft = 0.3048  # [m]
FL = 100 * ft  # [m]

# Teperature Gradients
a = [-0.0065, 0, 0.001, 0.0028, 0, -0.0028, -0.002]
b = [0, 11000, 20000, 32000, 47000, 51000, 71000]

print("--- ISA Calculator ---")
print("Please choose one of the following options:")
print("[1] Calculate ISA for altitude in meters")
print("[2] Calculate ISA for altitude in feet")
print("[3] Calculate ISA for altitude in FL")
choice = input("\nEnter your choice: ")

match choice:
    case "1":
        h = int(input("\nEnter your altitude in meters: "))
    case "2":
        h = int(input("\nEnter your altitude in feet: ")) * ft
    case "3":
        h = int(input("\nEnter your altitude in FL: ")) * FL
    case default:
        print(str(choice) + " is not an option.")
        exit()

if h < 0:
    print("A negative altitude is not possible.")
    exit()

i = 0
h0 = 0
while h >= b[i]:
    a0 = a[i]
    h0 = b[i]
    if i > 5:
        h1 = h
    else:
        h1 = b[i + 1]
    if h < h1: h1 = h
    T1 = T0 + a0 * (h1 - h0)
    if a0 == 0:
        p1 = p0 * math.e ** (-g0 / (T0 * R) * (h1 - h0))
    else:
        p1 = p0 * (T1 / T0) ** (-g0 / (a0 * R))
    rho = p1 / (R * T1)
    T0 = T1
    p0 = p1
    i += 1
    if i > 6: break

print("Temperature: " + str(T0) + " [K]")
print("Pressure: " + str(p0) + " [Pa]")
print("Density: " + str(rho) + " [kg/m^3]")
