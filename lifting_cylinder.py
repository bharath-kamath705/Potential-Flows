
"""
Lifting Cylinder
"""
import numpy as np
import potflow as pflo
import math
from matplotlib import pyplot as plt


    
# creating the grid
N = 200      # number of grid points in each direction
x_start, x_end = -2.0, 2.0
y_start, y_end = -1.0, 1.0
x = np.linspace(x_start, x_end, N)
y = np.linspace(y_start, y_end, N)
X, Y = np.meshgrid(x , y)

#--------- flow parameters----------------
xd, yd = [0.0], [0.0]      # doublet location
d_str = [1.0]            # double strength

U = 1.0                # free stream velocity
aoa = 0.0              # angle of attack

Vstr = [5.0]             # vortex strength
xv, yv = [0.0], [0.0]      # vortex location

R = math.sqrt(d_str[0]/(2 * math.pi * U))

# velocity field
u = pflo.vortex(xv, yv, Vstr, X, Y)[0] + pflo.doublet(X, Y, xd, yd, d_str)[0] + pflo.freestream(U, aoa, X, Y)[0]
v = pflo.vortex(xv, yv, Vstr, X, Y)[1] + pflo.doublet(X, Y, xd, yd, d_str)[1] + pflo.freestream(U, aoa, X, Y)[1]

# stream function 
psi = pflo.vortex(xv, yv, Vstr, X, Y)[2] + pflo.doublet(X, Y, xd, yd, d_str)[2] + pflo.freestream(U, aoa, X, Y)[2]

# pressure coefficient
cp = pflo.cp_get(u, v, U)

# plot cylinder and streamlines
width = 10.0
height = 10.0 / (x_end - x_start) * (y_end - y_start)
plt.figure(figsize=[width, height])
plt.xlabel('x', fontsize=16), plt.ylabel('y', fontsize=16)
plt.xlim(x_start, x_end), plt.ylim(y_start, y_end)
plt.streamplot(X, Y, u, v, density = 3)
circle=plt.Circle((0,0), R, color='r', alpha=1, zorder=3)
plt.gcf().gca().add_artist(circle)

# analytic pressure coefficient
theta = np.linspace(0, 2*np.pi, 100)
u_theta = -2 * U * np.sin(theta) - Vstr / (2 * np.pi * R)
cp = 1 - (u_theta/ U)**2

# non lifting case for comparison
u_nolift = -2 * U * np.sin(theta)
cp_nolift = 1 - (u_nolift / U)**2

# plot pressure coefficients
plt.figure(), plt.grid(True)
plt.xlim(theta[0], theta[-1])
plt.xlabel('$ \\theta $', fontsize=18), plt.ylabel('$C_p $', fontsize=18)
plt.plot(theta, cp, linewidth=2)
plt.plot(theta, cp_nolift, linewidth=2)

