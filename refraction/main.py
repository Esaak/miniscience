from Solver import *

dt = 1e-7
dh = 100
eps = 0.2
particle_numbers = 5000
R = 6 * 1e6
g = 9.8 * 0.84

Po = 1e7
T = 773
coef_reflection = 0.3
atmosphere_height = 100 * 1e3

x_start = -10 * atmosphere_height
y_lim = np.array([0.8, 0.9]) * atmosphere_height + R
dy = (- y_lim[0] + y_lim[1]) / particle_numbers

N = 100000000

earth, atmosphere, particles = initialization(particle_numbers=particle_numbers,
                                              R=R,
                                              g=g,
                                              Po=Po,
                                              T=T,
                                              coef_reflection=coef_reflection,
                                              atmosphere_height=atmosphere_height,
                                              x_start=x_start,
                                              y_lim=y_lim,
                                              dy=dy,
                                              dh=dh
                                              )
movement(earth, atmosphere, particles, N, dt)
