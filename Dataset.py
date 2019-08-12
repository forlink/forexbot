import numpy as np
import matplotlib.pyplot as plt
def __init__(self, chart):
    img = image(np.array([1, 2, -3, -2, 1, 0, 1, 4, 5, 1, 2, -3]))
    plot_image(img)
def image(dchart):
    length = dchart.shape[0]
    img = np.zeros((length), 13)
    for i in length:
        ypos = int(dchart[i])+6
        if ypos<0: ypos = 0
        elif ypos>12: ypos = 12
        img[i, ypos] = 1
    return img
def plot_image(img):
    plt.imshow(img, cmap="gray")
    plt.show()