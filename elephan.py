# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 23:51:41 2021

@author: the_p
"""

import matplotlib, time

from matplotlib import pyplot, animation
from matplotlib.animation import FuncAnimation

from numpy import append, cos,  linspace, pi, sin, zeros

# elephant parameters
p = [ 50 - 30j,
      18 +  8j,
      12 - 10j,
     -14 - 60j, 
      40 + 20j ] # Set p[4].real=0 to stop trunk wiggling

def fourier(t, C):
    f = zeros(t.shape) # initialize fourier values to zero
    for k in range(len(C)):
        f += C.real[k]*cos(k*t) + C.imag[k]*sin(k*t)
    return f

def elephant(t, p):
    npar = 6
    Cx = zeros((npar,), dtype='complex')
    Cy = zeros((npar,), dtype='complex')

    Cx[1] = p[0].real*1j
    Cy[1] = p[3].imag + p[0].imag*1j

    Cx[2] = p[1].real*1j
    Cy[2] = p[1].imag*1j

    Cx[3] = p[2].real
    Cy[3] = p[2].imag*1j

    Cx[5] = p[3].real


    x =  append(fourier(t,Cy), [p[4].imag])
    y = -append(fourier(t,Cx), [-p[4].imag])

    return x,y

fig, ax = pyplot.subplots()
elephan, = pyplot.plot([], [], 'o-', lw=2)
line, = pyplot.plot([], [], 'o-', lw=2)
x, y = elephant(linspace(0.4+1.3*pi,2*pi+0.9*pi,1000), p)
print(len(y))
def init():
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    return line, elephan
def LivePlot(i):
       # draw the body of the elephant
    x1, y2 = elephant(linspace(0.4+1.3*pi,2*pi+0.9*pi,1000), p)
    # wiggle trunk
    # create trunk
    elephan.set_data(x1, y2) 
    x, y = elephant(linspace(2*pi+0.9*pi,0.4+3.3*pi,1000), p)
    print(x)
    # move trunk to new position (but don't move eye stored at end or array)
    for ii in range(len(y)-1):
        y[ii] -= sin(((x[ii]-x[0])*pi/len(y)))*sin(float(i))*p[4].real
    line.set_data(x, y)
    return line,elephan      

ani = animation.FuncAnimation(
    fig, LivePlot, len(y), interval=0.03*1000, init_func=init,blit=True)
pyplot.show()
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
ani.save('elephan.mp4', writer=writer)


