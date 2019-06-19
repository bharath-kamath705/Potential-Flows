"""
Row of Vortices
"""

import numpy as np
import pflow
from matplotlib import pyplot as plt




N = 50          # grid resolution in each direction

# grid dimensions
x_start, x_end = -2.0, 2.0
y_start, y_end = -0.45, 0.45  

# creating the grid
x = np.linspace(x_start, x_end, N)
y = np.linspace(y_start, y_end, N)
X, Y = np.meshgrid(x, y)

#----- Generating the Velocity Field -------

# number of vortices and spacing
n, a = 100, 0.5
# vortex strengths
Vstr = 1.0 * np.ones(n+1)           
# vortex locations
xv = np.linspace(-n//2*a, n//2*a, n+1)
yv = np.zeros(n+1)   

# velocity field
u = pflow.vortex(xv, yv, Vstr, X, Y)[0] 
v = pflow.vortex(xv, yv, Vstr, X, Y)[1] 
# stream function
psi = pflow.vortex(xv, yv, Vstr, X, Y)[2]

# plot the streamlines
width = 10
height = 10 / (x_end - x_start) * (y_end - y_start)
plt.figure(figsize=(width,height))
plt.streamplot(X, Y, u, v, density = 3)
plt.scatter(xv, yv, color='r')
plt.xlim(x_start, x_end), plt.ylim(y_start, y_end)
plt.xlabel('x',fontsize=20), plt.ylabel('y', fontsize=20)

# ------ Analytic solution: infinite row vortices ----------

# some definitions to simplify expressions
b = 2 * np.pi / a
dr = np.cosh(b * Y) - np.cos(b * X)

# analytic velocity field
ua = 0.5 * Vstr[0] / a * np.sinh(b * Y) / dr
va = -0.5 * Vstr[0] /a * np.sin(b * X) / dr

# plot the streamlines
width = 10
height = 10 / (x_end - x_start) * (y_end - y_start)
plt.figure(num = 'analytic solution', figsize=(width,height))
plt.streamplot(X, Y, ua, va, density = 3)
plt.scatter(xv, yv, color='b')
plt.xlim(x_start, x_end), plt.ylim(y_start, y_end)
plt.xlabel('x',fontsize=20), plt.ylabel('y', fontsize=20)

