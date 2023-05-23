import matplotlib.pyplot as plt
import pygame
pygame.init()
def one_frame(planet, x,y, atmosphere, t):
    fig, ax = plt.subplots(figsize = (10, 10))
    ax.scatter(x, y)
    circle1 = plt.Circle((0, 0), planet.R, color='r', fill= False)
    circle2 = plt.Circle((0, 0), atmosphere.height + planet.R, color='b', fill= False)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.axis('equal')
    plt.savefig(f"pictures/graph_{t}.png")
    plt.show()

# def pygame_frame():
#     background_colour = (0, 0, 0)
#     width_m = atmosphere_hieght + 2 * R
#
#     (width, height) = (1000, 1000)
#     m = width / width_m
#     screen = pygame.display.set_mode((width, height))
#     pygame.display.set_caption('planet refraction')
#     screen.fill(background_colour)
#     pygame.display.flip()
#     Color_line = (200, 200, 200)
#     x_0, y_0 = width // 2, height // 2
#     x_pl = 12
#     y_pl = 0
#     pygame.draw.circle(screen, (50, 50, 50), (x_pl + x_0, y_pl + y_0), 150)
#     pygame.draw.circle(screen, (100, 100, 100), (x_pl + x_0, y_pl + y_0), 60)
#     while running:
#         # quitting
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#         # background
#         screen.fill((0, 0, 0))
#
#         # planet
#
#
#
#         # getting data for one frame
#
#         x, y = one_frame(particle_numbers, dy)
#
#         # drawing lines
#         for i in range(len(x)):
#             pygame.draw.circle(screen, (200, 200, 200), (x[i] // 10 + x_0, y[i] // 10 + y_0), 2)
#
#
#         pygame.display.flip()