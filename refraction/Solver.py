import Planet
import Particle
import constants
import Visualization
import numpy as np
import threading
from time import time, sleep
import sys
import matplotlib.pyplot as plt
import os
from updateConsole import print_at


def breaking_atmosphere(planet, dh, atmosphere_height):
    n = []
    coef0 = 4 * np.pi * constants.alpha * planet.Po / (constants.k * planet.T)
    coef1 = constants.m * planet.g / (constants.k * planet.T)

    for i in range(int(atmosphere_height / dh) + 1):
        n.append(np.sqrt(1 + coef0 * (np.exp(-coef1 * (dh * i)))))
    print(f"Показатель преломления при h = 0 м, при h = {atmosphere_height} м")
    print(n[0], n[-1])
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
    matrix = np.array([[0, 0], [0, 0]], dtype=np.float64)
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
                                    np.array((np.float64(next_v_csi_eta[0]), np.float64(next_v_csi_eta[1]))))
        particle.velocity[0] = next_v_x
        particle.velocity[1] = next_v_y
        particle.velocity[2] = constants.c / next_n

    particle.coord[0] = next_x
    particle.coord[1] = next_y


def one_particle_way(particle, planet, atmosphere, dt, line_x, line_y, N, j):
    line_x.append(particle.coord[0])
    line_y.append(particle.coord[1])
    persent = N // 4
    for i in range(N):
        one_step(particle, planet, atmosphere, dt)
        if particle.coord[0] == particle.coord[1] == 0:
            break
        if i % 10000 == 0:
            line_x.append(particle.coord[0])
            line_y.append(particle.coord[1])
        # if i % persent == 0:
        #     sys.stdout.write(f"{j:5d} Thread: {int(i/N * 100)}%    ")
        #     sys.stdout.write('\n')
        #     sys.stdout.flush()



    sys.stdout.write(f"{j:5d} Thread end working \n")
    # print_at(0, 0, '')


def movement(planet, atmosphere, particles, N, dt):
    t1 = time()
    lines_x = []
    lines_y = []
    for i in range(len(particles)):
        lines_x.append([])
        lines_y.append([])



    threads = [
        threading.Thread(target=one_particle_way,
                         args=(particles[j], planet, atmosphere, dt, lines_x[j], lines_y[j], N, j))
        for j in range(0, len(particles))
    ]
    for thread in threads:
        thread.start()  # каждый поток должен быть запущен
    for thread in threads:
        thread.join()  # дожидаемся исполнения всех потоков

    #print_at(constants.particle_numbers + 1, 0, '')

    t2 = time()
    print(t2 - t1)
    x = []
    y = []
    for i in range(len(particles)):
        x += lines_x[i]
        y += lines_y[i]

    # save data at file
    try:
        with open(f"data/data_{t2}.txt", 'w') as f:
            f.write("Calculation parameters:\n")
            f.write(f"c = {constants.c}\n")
            f.write(f"m = {constants.m}\n")
            f.write(f"alpha = {constants.alpha}\n")
            f.write(f"k = {constants.k}\n\n")

            f.write(f"dt = {constants.dt}\n")
            f.write(f"dh = {constants.dh}\n")
            f.write(f"eps = {constants.eps}\n")
            f.write(f"particle_numbers = {constants.particle_numbers}\n")
            f.write(f"R = {constants.R}\n")
            f.write(f"g = {constants.g}\n")
            f.write(f"Po = {constants.Po}\n")
            f.write(f"T = {constants.T}\n")
            f.write(f"coef_reflection = {constants.coef_reflection}\n")
            f.write(f"atmosphere_height = {constants.atmosphere_height}\n")
            f.write(f"Light launch interval = [{constants.y_lim[0]}; {constants.y_lim[1]}] \n")
            f.write(f"N = {constants.N}\n\n\n")

            f.write("Data:\n")
            f.write("x,m    y,m\n")
            for i in range(len(particles)):
                f.write(f"{lines_x[i][-1]} {lines_y[i][-1]}\n")
    except:
        print("Error when writing to a file")

    Visualization.one_frame(planet, x, y, atmosphere, t2)
