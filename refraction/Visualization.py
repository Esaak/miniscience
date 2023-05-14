import matplotlib.pyplot as plt

def one_frame(planet, x,y, atmosphere):
    fig, ax = plt.subplots(figsize = (10, 10))
    ax.scatter(x, y)
    circle1 = plt.Circle((0, 0), planet.R, color='r', fill= False)
    circle2 = plt.Circle((0, 0), atmosphere.height + planet.R, color='b', fill= False)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    # for i in range(len(atmosphere.n)):
    #     ax.add_patch(plt.Circle((0, 0), planet.R + atmosphere.dh*i, color='green', fill= False, linewidth = 0.04))
    ax.set_xlim((-(0.004+6)*1e6, (0.004 + 6)*1e6))
    ax.set_ylim((-(0.04 + 6)*1e6, (0.004+6)*1e6))
    #ax.set_xlim((0, (0.004 + 6) * 1e4))
    #ax.set_ylim((1e6, (0.04 + 6) * 1e6))
    plt.show()
