import matplotlib.pyplot as plt

def one_frame(planet, x,y, atmosphere):
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    circle1 = plt.Circle((0, 0), planet.R, color='r', fill= False)
    circle2 = plt.Circle((0, 0), atmosphere.height + planet.R, color='b', fill= False)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.set_xlim((-2000, 2000))
    ax.set_ylim((-2000, 2000))
    plt.show()
