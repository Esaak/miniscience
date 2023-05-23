from Solver import *

# dt = 10**(-9)
# dh = 1  # м
# eps = 0.2
# particle_numbers = 30
# R = 6 * 1e6
# g = 9.8 * 0.84
#
# Po = 1e7
# T = 773
# coef_reflection = 0.3
# atmosphere_height = R  # м
#
# N = 10**5

dt = constants.dt
dh = constants.dh  # м
eps = constants.eps
particle_numbers = constants.particle_numbers
R = constants.R
g = constants.g

Po = constants.Po
T = constants.T
coef_reflection = constants.coef_reflection
atmosphere_height = constants.atmosphere_height  # м


N = constants.N

x_start = - (atmosphere_height + R) - 1

y_lim = constants.y_lim
dy = (- y_lim[0] + y_lim[1]) / max(1, particle_numbers - 1)

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
