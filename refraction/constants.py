import numpy as np

c = 3*1e8 # м / с

m = 8*1e-28 # kg
alpha = 1.2*1e-28
k = 1.38*1e-23 # Дж/К


dt = 10**(-8) # c
dh = 10  # м
eps = 0.2
particle_numbers = 100
R = 6 * 1e6 # м
g = 9.8 * 0.84 # м/с^2

Po = 1e7 # Па
T = 773 # K
coef_reflection = 0.3
atmosphere_height = R  # м
y_lim = np.array([0.465, 0.57], dtype=float) * atmosphere_height + R # м
N = 10**8

# def atmosphere_height_find():
#     delta_n = 0.00001
#     return max(- k*T * np.log(delta_n * k * T/(4* np.pi * alpha * Po))/(m * g), R)