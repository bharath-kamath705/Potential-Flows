"""
Rankine Oval
"""

import numpy
import math
from matplotlib import pyplot

def source(x_s, y_s, S_str, X, Y):
    """
    Returns the velocity and stream function field generated by the source
    
    Parameters
    ----------
    x_s: float
         x-coordinate of the source
    y_s: float
         y-coordinate of the source
    S_str: float
           strength of the source
    X, Y: 2D numpy arrays
          grid generated by numpy.meshgrid( )         
    
    Returns
    -------
    u: 2D Numpy array of floats
       x-component of the velocity field
    v: 2D Numpy array of floats
       y-component of the velocity field
    psi: 2D Numpy array of floats
       stream function field
    
    """
   # radial distance and angle from source
    r   = numpy.sqrt( (X - x_s)**2 + (Y - y_s)**2)
    theta = numpy.arctan2(Y - y_s, X - x_s)
    
    # velocity field
    u = 0.5 * S_str / (numpy.pi * r) * numpy.cos(theta) 
    v = 0.5 * S_str / (numpy.pi * r) * numpy.sin(theta)
    
    #stream function
    psi = 0.5 * S_str / numpy.pi * numpy.arctan2((Y - y_s), (X - x_s)) 
    
    return u, v, psi    

def freestream(U, aoa, X, Y):
    """
    Returns uniform flow velocity field and stream function
    
    Parameters
    ----------
    U: float
    uniform flow velocity
    aoa: float
    angle of attack
    X, Y: 2D Numpy array
    grid points
    
    Returns
    -------
    u, v: 2D Numpy arrays
    x and y direction velocity fields
    psi: 2D Numpy array of floats
       stream function field
    """
    
    u = U * numpy.cos(aoa) * numpy.ones(numpy.shape(X))
    v = U * numpy.sin(aoa) * numpy.ones(numpy.shape(X))
    psi = U * Y
    return u, v, psi

N = 200          # grid resolution in each direction

# grid dimensions
x_start, x_end = -4.0, 4.0
y_start, y_end = -2.0, 2.0  

# creating the grid
x = numpy.linspace(x_start, x_end, N)
y = numpy.linspace(y_start, y_end, N)
X, Y = numpy.meshgrid(x, y)

#----- Generating Rankine Oval Velocity Field -------

S_str = 5.0            # source strength
x_s, y_s = -1.0, 0.0   # source location

Sk_str = -5.0          # sink strength
x_sk, y_sk = 1.0, 0.0  # sink location

U = 1.0                # freestream velocity
aoa = 0.0             # angle of attack

# velocity field
u = source(x_s, y_s, S_str, X, Y)[0] + source(x_sk, y_sk, Sk_str, X, Y)[0] + freestream(U, aoa, X, Y)[0]
v = source(x_s, y_s, S_str, X, Y)[1] + source(x_sk, y_sk, Sk_str, X, Y)[1] + freestream(U, aoa, X, Y)[1]

# stream function
psi = source(x_s, y_s, S_str, X, Y)[2] + source(x_sk, y_sk, Sk_str, X, Y)[2] + freestream(U, aoa, X, Y)[2]


# plot the streamlines
width = 10
height = 10 / (x_end - x_start) * (y_end - y_start)
pyplot.figure(figsize=(width,height))
pyplot.streamplot(X, Y, u, v)
pyplot.contour(X, Y, psi, 0, colors='r')
pyplot.xlabel('x',fontsize=20), pyplot.ylabel('y',fontsize=20)

# plot pressure coefficient contours
cp = numpy.ones([N,N]) - (u**2 + v**2) / U**2
pyplot.figure()
contf = pyplot.contourf(X, Y, cp, levels=numpy.linspace(-2.0, 1.0, 100), extend='both')
cbar = pyplot.colorbar(contf)
pyplot.contour(X, Y, psi, 0, colors='r')
cbar.set_label('cp', fontsize=16)

