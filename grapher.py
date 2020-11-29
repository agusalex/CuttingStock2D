import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from rectangle import Rectangle


def create_rectangle(rectangle: Rectangle):
    # get the right map, and get the color from the map
    color = matplotlib.cm.jet(rectangle.x / 3)
    rec = plt.Rectangle((rectangle.x, rectangle.y), rectangle.width,
                        rectangle.height, color=color, zorder=1, alpha=0.8)
    add_shape(rec)


def add_shape(patch):
    ax = plt.gca()
    ax.add_patch(patch)
    plt.axis('scaled')


def testDraw2():
    c1 = Rectangle(0, 0, 1, 4)
    c2 = Rectangle(3, 4, 2, 4)
    create_rectangle(c1)
    create_rectangle(c2)
    plt.show()


def drawRectangles(drawlist):
    for item in drawlist:
        create_rectangle(item)
    plt.show()


if __name__ == '__main__':
    print("holis")
    testDraw2()

# plt.imsave('demo')
