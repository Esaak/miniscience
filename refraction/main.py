from Solver import *


dt = 1e-8
dh = 10
eps = 0.2
particle_numbers = 10
R  = 6*1e6
g = 9.8*0.84
#Po = 1e6
Po = 1e7
T = 773
coef_reflection = 0.3
atmosphere_height = 100*1e3
#x_start = -2*6*1e6
x_start = -10*atmosphere_height
y_start = 6*1e6
N = 100000
#dy = (R + atmosphere_height)/particle_numbers
earth, atmosphere, particles = initialization(particle_numbers=  particle_numbers,
                                              R= R,
                                              g = g,
                                              Po= Po,
                                              T = T,
                                              coef_reflection= coef_reflection,
                                              atmosphere_height= atmosphere_height,
                                              x_start = x_start,
                                              y_start = y_start,
                                              dh = dh
                                              )
movement(earth, atmosphere, particles, N, dt, particle_numbers)