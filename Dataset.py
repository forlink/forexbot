import numpy as np
import matplotlib.pyplot as plt
class Dataset:
    def plot_image(self, img):
        plt.imshow(img, cmap="gray")
        plt.show()
    def image(self, dchart):
        length = dchart.shape[0]
        img = np.zeros((length, 13), dtype = 'float32')
        for i in range(length):
            ypos = int(dchart[i])+6
            if ypos<0: ypos = 0
            elif ypos>12: ypos = 12
            img[i, ypos] = 1
        return img
    def __init__(self):
        arr = np.array([1, 2, -3, -2, 1, 0, 1, 4, 5, 1, 2, -3])
        img = self.image(arr)
        self.plot_image(img)
