import matplotlib.pyplot as plt
import math
import numpy as np

# Constants
rho = 1.225
S = 0.2
Cl = 1.25
CD = 0.125
m = 1
g = 9.80665
k_p = 0.1
k_d = 1
dt = 0.01

# Variables
t = 0
ax = 0
az = 0
vx = 8.002718
vz = 0
x = 0
z = 50
z_new = 70
e = 0
de = 0
e_list = [20]
x_list = []
z_list = []
vx_list = []
vz_list = []
t_list = []
gamma = 0
theta = 0
AOA = 0
T_eq = 0.980665
T = 0

# While the time is below 100 seconds and the wing is above ground level
while t < 100 and z > 0:
    t += dt
    # Calculate the error and new thrust
    e = z_new - z
    e_list.append(e)
    de = (e_list[-1] - e_list[-2]) / dt
    T = T_eq + k_p * e + k_d * de
    v = math.sqrt(vx**2 + vz**2)

    # Calculate forces and angles
    L = 0.5 * Cl * rho * v ** 2 * S
    D = 0.5 * CD * rho * v ** 2 * S
    gamma = np.arctan2(vz,vx)
    theta = gamma + AOA
    Fz = -m*g + L*math.cos(gamma) - D*math.sin(gamma) + T*math.sin(theta)
    Fx = T * math.cos(theta) - D * math.cos(gamma) - L * math.sin(gamma)

    # Integrate acceleration to velocity and position
    az = Fz / m
    vz += az * dt
    z += vz * dt
    ax = Fx / m
    vx += ax * dt
    x += vx * dt
    x_list.append(x)
    z_list.append(z)
    vx_list.append(vx)
    vz_list.append(vz)
    t_list.append(t)

# Plotting
plt.subplot(321)
plt.plot(t_list, x_list)
plt.title('x')
plt.subplot(322)
plt.plot(t_list, z_list)
plt.title('z')
plt.axis([0, 100, z, z_new])
plt.yticks(np.arange(50, 75, 5.0))
plt.subplot(323)
plt.plot(t_list, vx_list)
plt.title('x velocity')
plt.subplot(324)
plt.plot(t_list, vz_list)
plt.title('z velocity')
plt.tight_layout()
plt.subplot(325)
plt.plot(t_list, e_list[:-1])
plt.title('error')
plt.show()