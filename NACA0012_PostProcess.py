"""
Flowfield given source distribution 
NACA 0012 Airfoil
"""

import numpy as np
import pflow
from matplotlib import pyplot as plt



# generate grid
N = 501                             # number of grid points in each direction
x_start, x_end = -1.0, 2.0
y_start, y_end = -0.5, 0.5
x = np.linspace(x_start, x_end, N)
y = np.linspace(y_start, y_end, N)
X, Y = np.meshgrid(x, y)

# read Source strengths and locations from file
s_st = np.loadtxt("NACA0012_sigma.txt", dtype="float", delimiter="\n")
xs = np.loadtxt("NACA0012_x.txt", dtype="float", delimiter="\n")
ys = np.loadtxt("NACA0012_y.txt", dtype="float", delimiter="\n")

# flow parameters
U = 1.0                # freestream velocity
aoa = 0.0             # angle of attack

# velocity field
u = pflow.source(xs, ys, s_st, X, Y)[0] + pflow.freestream(U, aoa, X, Y)[0]
v = pflow.source(xs, ys, s_st, X, Y)[1] + pflow.freestream(U, aoa, X, Y)[1]

# stream function
psi = pflow.source(xs, ys, s_st, X, Y)[2] + pflow.freestream(U, aoa, X, Y)[2]

# pressure coefficient
cp = pflow.cp_get(u, v, U)

# plot the streamlines
width = 10
height = 10 / (x_end - x_start) * (y_end - y_start)
plt.figure(figsize=(width,height))
plt.streamplot(X, Y, u, v, density=2)
plt.xlabel('x',fontsize=20), plt.ylabel('y',fontsize=20)
plt.xlim(x_start, x_end), plt.ylim(y_start, y_end)
plt.fill(xs, ys, color='k',zorder=3)    # black out interior of body

# plot pressure contours
plt.figure()
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
plt.plot(xs,ys, color='r')
contf = plt.contourf(X, Y, cp, levels=np.linspace(-2.0, 1.0, 100), extend='both')
cbar = plt.colorbar(contf)
cbar.set_label('$C_p$', fontsize=16)
plt.fill(xs, ys, color='k', zorder=3)   # black out interior of body