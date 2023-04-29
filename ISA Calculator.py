import math

# Standard Values
g0 = 9.80665
R = 287
T0 = 288.15
p0 = 101325

ft = 0.3048 # [m]
FL = 100 * ft # [m]

# Teperature Gradients
a0 = -0.0065
a2 = 0.0011
a3 = 0.0028
a5 = -0.0028
a6 = -0.002

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

h1 = min(h, 11000)
T1 = T0 + a0*(h1)
p1 = p0*(T1/T0)**(-g0/(a0*R))
rho = p1/(R*T1)
p = p1
T = T1

if h > 11000:
    h2 = min(h, 20000)
    T2 = T1
    p2 = p1 * math.e**(-g0 / (T2 * R) * (h2-h1))
    rho = p2 / (R * T2)
    p = p2
    T = T2

if h > 20000:
    h3 = min(h, 32000)
    T3 = T2 + a2 * (h3 - h2)
    p3 = p2 * (T3 / T2) ** (-g0 / (a2 * R))
    rho = p3 / (R * T3)
    p = p3
    T = T3

if h > 32000:
    h4 = min(h, 47000)
    T4 = T3 + a3 * (h4 - h3)
    p4 = p3 * (T4 / T3) ** (-g0 / (a3 * R))
    rho = p4 / (R * T4)
    p = p4
    T = T4

if h > 47000:
    h5 = min(h, 51000)
    T5 = T4
    p5 = p4 * math.e**(-g0 / (T5 * R) * (h5-h4))
    rho = p5 / (R * T5)
    p = p5
    T = T5

if h > 51000:
    h6 = min(h, 71000)
    T6 = T5 + a5 * (h6 - h5)
    p6 = p5 * (T6 / T5) ** (-g0 / (a5 * R))
    rho = p6 / (R * T6)
    p = p6
    T = T6

if h > 71000:
    h7 = min(h, 86000)
    T7 = T6 + a6 * (h7 - h6)
    p7 = p6 * (T7 / T6) ** (-g0 / (a6 * R))
    rho = p7 / (R * T7)
    p = p7
    T = T7

print("Temperature: " + str(T) + " [K]")
print("Pressure: " + str(p) + " [Pa]")
print("Density: " + str(rho) + " [kg/m^3]")
