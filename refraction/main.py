from Solver import *


dt = 1e-1
dh = 10
eps = 0.2
particle_numbers = 10
R  = 500
g = 9.8*0.84
Po = 1e7
T = 773
coef_reflection = 0.3
atmosphere_height = 1000
x_start = -1000
N = 10000
#dy = (R + atmosphere_height)/particle_numbers
earth, atmosphere, particles = initialization(particle_numbers=  particle_numbers,
                                              R= R,
                                              g = g,
                                              Po= Po,
                                              T = T,
                                              coef_reflection= coef_reflection,
                                              atmosphere_height= atmosphere_height,
                                              x_start = x_start,
                                              dh = dh
                                              )
movement(earth, atmosphere, particles, N, dt)