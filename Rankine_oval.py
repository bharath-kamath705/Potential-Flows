"""
Rankine Oval
"""

import numpy
import potflow as pflo
from matplotlib import pyplot



N = 200          # grid resolution in each direction

# grid dimensions
x_start, x_end = -4.0, 4.0
y_start, y_end = -2.0, 2.0  

# creating the grid
x = numpy.linspace(x_start, x_end, N)
y = numpy.linspace(y_start, y_end, N)
X, Y = numpy.meshgrid(x, y)

#----- Generating Rankine Oval Velocity Field -------

S_str = [5.0]          # source strength
x_s, y_s = [-1.0],[ 0.0]   # source location

Sk_str = [-5.0]          # sink strength
x_sk, y_sk = [1.0], [0.0]  # sink location

U = 1.0                # freestream velocity
aoa = 0.0             # angle of attack

# velocity field
u = pflo.source(x_s, y_s, S_str, X, Y)[0] + pflo.source(x_sk, y_sk, Sk_str, X, Y)[0] + pflo.freestream(U, aoa, X, Y)[0]
v = pflo.source(x_s, y_s, S_str, X, Y)[1] + pflo.source(x_sk, y_sk, Sk_str, X, Y)[1] + pflo.freestream(U, aoa, X, Y)[1]

# stream function
psi = pflo.source(x_s, y_s, S_str, X, Y)[2] + pflo.source(x_sk, y_sk, Sk_str, X, Y)[2] + pflo.freestream(U, aoa, X, Y)[2]


# plot the streamlines
width = 10
height = 10 / (x_end - x_start) * (y_end - y_start)
pyplot.figure(figsize=(width,height))
pyplot.streamplot(X, Y, u, v)
pyplot.contour(X, Y, psi, 0, colors='r')
pyplot.xlabel('x',fontsize=20), pyplot.ylabel('y',fontsize=20)

# plot pressure coefficient contours
cp = pflo.cp_get(u, v, U)
pyplot.figure()
contf = pyplot.contourf(X, Y, cp, levels=numpy.linspace(-2.0, 1.0, 100), extend='both')
cbar = pyplot.colorbar(contf)
pyplot.contour(X, Y, psi, 0, colors='r')
cbar.set_label('cp', fontsize=16)


