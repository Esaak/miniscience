import Planet
import Particle
import constants
import Visualization
import numpy as np

def breaking_atmosphere(planet, dh, atmosphere_height):
    n =[]
    coef0 = 2*np.pi*constants.alpha*planet.Po/(constants.k*planet.T)
    coef1 = constants.m*planet.g/(constants.k*planet.T)
    for i in range(int(atmosphere_height/dh)):
        n.append(1 + coef0*(1 - coef1*(dh*i)))
    return Planet.Atmosphere(atmosphere_height, n, dh)

def initialization(particle_numbers, R, g, Po, T, coef_reflection, atmosphere_height, x_start, dh):
    earth = Planet.Planet(R, g, Po, T, coef_reflection)
    particles = []
    for i in range(particle_numbers):
        dy = (R + atmosphere_height)/particle_numbers
        particles.append(Particle.Particle(x_start, i*dy, 1, 0, constants.c))
    atmosphere = breaking_atmosphere(earth, dh, atmosphere_height)

    return earth, atmosphere, particles

def one_step(particle, planet, atmosphere, dt):
    next_x = particle.coord[0] + particle.velocity[0]*particle.velocity[2]*dt
    next_y = particle.coord[1] + particle.velocity[1]*particle.velocity[2]*dt
    r = np.sqrt(next_x**2 + next_y**2)
    if r <= planet.R:
        if np.random.rand() > planet.coef_reflection:
            particle.coord[0] = 0
            particle.coord[1] = 0
            return
        else:
            particle.velocity[0] *=np.sign(particle.coord[0])
            particle.velocity[1] *=np.sign(particle.coord[1])
            particle.coord[0] += particle.velocity[0]*particle.velocity[2]*dt
            particle.coord[1] += particle.velocity[1]*particle.velocity[2]*dt
            return
    if r > planet.R + atmosphere.height and particle.velocity[0]>=0 and np.abs(particle.velocity[1])>0.5:
        particle.coord[0] = 0
        particle.coord[1] = 0
        return
    elif r > planet.R + atmosphere.height:
        particle.coord[0] += particle.velocity[0] *particle.velocity[2] * dt
        particle.coord[1] += particle.velocity[1] *particle.velocity[2]* dt
        return
    next_n = atmosphere.n[int((r-planet.R)/atmosphere.dh)]
    next_v_x = 0
    next_v_y = 0

    if  next_n != constants.c/particle.velocity[2]:
        k1 = particle.velocity[1]/particle.velocity[0]
        k2 = particle.coord[1]/particle.coord[0]
        sina = np.abs(k1-k2)/np.sqrt((k1*k2)**2 + k1**2 + k2**2 + 1)
        #условие на угол Брюстера
        sinb = constants.c/particle.velocity[2] * sina/next_n
        cosX = np.abs(particle.coord[0])/np.sqrt(particle.coord[0]**2 + particle.coord[1]**2)
        sinX = cosX * np.abs(particle.coord[1])/np.abs(particle.coord[0])
        cosb = np.sqrt(1-sinb**2)
        if constants.c/particle.velocity[2] * sina/next_n >=1:
            next_v_x = cosX*cosb + sinX*sinb
            next_v_y = - sinX*cosb + sinb * cosX
        else:
            next_v_x = cosX*cosb + sinX*sinb
            next_v_y = sinX*cosb - sinb * cosX
    particle.coord[0] = next_x
    particle.coord[1] = next_y
    particle.velocity[0] = next_v_x
    particle.velocity[1] = next_v_y
    particle.velocity[2] = constants.c/next_n

def movement(planet, atmosphere, particles, N, dt):
    x = []
    y = []
    for i in range(N):
        for j in range(len(particles)):
            one_step(particles[j], planet, atmosphere, dt)
        for k in particles:
            if k.coord[0] == k.coord[1] == 0:
                particles.remove(k)
            else:
                x.append(k.coord[0])
                y.append(k.coord[1])
    Visualization.one_frame(planet, x, y, atmosphere)



