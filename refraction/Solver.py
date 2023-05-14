import Planet
import Particle
import constants
import Visualization
import numpy as np
import threading
from time import time


def breaking_atmosphere(planet, dh, atmosphere_height):
    n = []
    coef0 = 4 * np.pi * constants.alpha * planet.Po / (constants.k * planet.T)
    coef1 = constants.m * planet.g / (constants.k * planet.T)

    for i in range(int(atmosphere_height / dh) + 1):
        n.append(np.sqrt(1 + coef0 * (np.exp(-coef1 * (dh * i)))))

    return Planet.Atmosphere(atmosphere_height, n, dh)


def initialization(particle_numbers, R, g, Po, T, coef_reflection, atmosphere_height, x_start, y_lim, dy, dh):
    earth = Planet.Planet(R, g, Po, T, coef_reflection)
    particles = []
    atmosphere = breaking_atmosphere(earth, dh, atmosphere_height)
    for i in range(particle_numbers):
        n0 = 0
        r = np.sqrt(x_start ** 2 + (i * dy + y_lim[0]) ** 2)
        if r > (atmosphere_height + R):
            n0 = 1.
        else:
            n0 = atmosphere.n[int((np.abs(r - R)) / atmosphere.dh)]
        particles.append(Particle.Particle(x_start, y_lim[0] + i * dy, 1, 0, constants.c / n0))

    return earth, atmosphere, particles


def rotation_matrix(cos_gamma, sign):
    matrix = np.array([[0, 0], [0, 0]], dtype=np.float)
    sin_gamma = np.sqrt(1 - cos_gamma * cos_gamma)
    matrix[0][0] = cos_gamma
    matrix[0][1] = - sign * sin_gamma
    matrix[1][0] = + sign * sin_gamma
    matrix[1][1] = cos_gamma
    return matrix


def snellius(sinb, sign_v_csi, sign_v_eta):
    if sign_v_csi >= 0 >= sign_v_eta:
        return sinb, -np.sqrt(1 - sinb * sinb)
    if sign_v_csi > 0 and sign_v_eta > 0:
        return sinb, np.sqrt(1 - sinb * sinb)
    if sign_v_csi < 0 < sign_v_eta:
        return -sinb, np.sqrt(1 - sinb * sinb)
    if sign_v_eta < 0 and sign_v_csi < 0:
        return -sinb, -np.sqrt(1 - sinb * sinb)


def one_step(particle, planet, atmosphere, dt):
    next_x = particle.coord[0] + particle.velocity[0] * particle.velocity[2] * dt
    next_y = particle.coord[1] + particle.velocity[1] * particle.velocity[2] * dt
    r = np.sqrt(next_x ** 2 + next_y ** 2)
    if r <= planet.R:
        if np.random.rand() > planet.coef_reflection:
            particle.coord[0] = 0
            particle.coord[1] = 0
            return
        else:
            particle.velocity[0] *= np.sign(particle.coord[0])
            particle.velocity[1] *= np.sign(particle.coord[1])
            particle.coord[0] += particle.velocity[0] * particle.velocity[2] * dt
            particle.coord[1] += particle.velocity[1] * particle.velocity[2] * dt
            return
    if r > (planet.R + atmosphere.height) and particle.velocity[0] != 1:
        particle.coord[0] = 0
        particle.coord[1] = 0
        return
    elif r > planet.R + atmosphere.height:
        particle.coord[0] += particle.velocity[0] * particle.velocity[2] * dt
        particle.coord[1] += particle.velocity[1] * particle.velocity[2] * dt
        return
    next_n = atmosphere.n[int((r - planet.R) / atmosphere.dh)]
    n = constants.c / particle.velocity[2]
    next_v_x = 2
    next_v_y = 2
    next_v_csi = 2
    next_v_eta = 2
    next_v_csi_eta = [2, 2]
    if next_n != n:

        cos_gamma = particle.coord[1] / np.sqrt(particle.coord[0] ** 2 + particle.coord[1] ** 2)

        A = rotation_matrix(cos_gamma, np.sign(particle.coord[0]))
        v_csi_eta = np.dot(A, np.array(particle.velocity[:-1]))
        sina = np.abs(v_csi_eta[0])
        sinb = n * sina / next_n
        if sinb >= 1:
            next_v_csi_eta[1] = -v_csi_eta[1]
            next_v_csi_eta[0] = v_csi_eta[0]
        else:
            next_v_csi_eta = snellius(sinb, np.sign(v_csi_eta[0]), np.sign(v_csi_eta[1]))

        next_v_x, next_v_y = np.dot(np.linalg.inv(A),
                                    np.array((np.float(next_v_csi_eta[0]), np.float(next_v_csi_eta[1]))))
        particle.velocity[0] = next_v_x
        particle.velocity[1] = next_v_y
        particle.velocity[2] = constants.c / next_n

    particle.coord[0] = next_x
    particle.coord[1] = next_y


def one_particle_way(particle, planet, atmosphere, dt, line_x, line_y, N):
    event = threading.Event()
    line_x.append(particle.coord[0])
    line_y.append(particle.coord[1])
    for i in range(N):
        one_step(particle, planet, atmosphere, dt)
        if particle.coord[0] == particle.coord[1] == 0:
            return
        if i % 100 == 0:
            line_x.append(particle.coord[0])
            line_y.append(particle.coord[1])
    print("Thread end working")


def movement(planet, atmosphere, particles, N, dt):
    t1 = time()
    lines_x = []
    lines_y = []
    for i in range(len(particles)):
        lines_x.append([])
        lines_y.append([])

    threads = [
        threading.Thread(target=one_particle_way,
                         args=(particles[j], planet, atmosphere, dt, lines_x[j], lines_y[j], N,))
        for j in range(0, len(particles))
    ]
    for thread in threads:
        thread.start()  # каждый поток должен быть запущен
    for thread in threads:
        thread.join()  # дожидаемся исполнения всех потоков

    x = []
    y = []
    t2 = time()
    print(t2 - t1)
    for i in range(len(particles)):
        x += lines_x[i]
        y += lines_y[i]

    Visualization.one_frame(planet, x, y, atmosphere)
