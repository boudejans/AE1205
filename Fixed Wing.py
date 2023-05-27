import matplotlib.pyplot as plt
import math

m = 1
g = 9.80665
dt = 0.1
t = [0]
x = [0]
z = [50]
vx = 2
vz = 0
vxa = [0]
vza = [0]
Cl = 1.25
CD = 0.125
rho = 1.225
S = 0.2
FPAngle = 0
PAngle = 0
AOA = 0
T = 1
i = 0

while True:
    v = math.sqrt(vx**2 + vz**2)
    L = 0.5*Cl*rho*v**2*S
    D = 0.5*CD*rho*v**2*S
    print("L: " + str(L) + " -  D: " + str(D))
    # FPAngle = math.atan(vz/vx)
    Fz = -m*g + L*math.cos(FPAngle) - D*math.sin(FPAngle) + T*math.sin(PAngle)
    vz += Fz/m*dt
    Fx = T*math.cos(PAngle) - D*math.cos(FPAngle) - L*math.sin(FPAngle)
    vx += Fx/m*dt
    t.append(t[-1] + dt)
    x.append(x[-1] + vx)
    z.append(z[-1] + vz)
    vxa.append(vx)
    vza.append(vz)
    i += 1
    if i == 100:
        break

plt.subplot(321)
plt.plot(t, x)
plt.title('x')
plt.subplot(322)
plt.plot(t, z)
plt.title('z')
plt.subplot(323)
plt.plot(t, vxa)
plt.title('z')
plt.subplot(324)
plt.plot(t, vza)
plt.title('z')

plt.show()