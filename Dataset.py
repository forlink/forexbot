import numpy as np
import matplotlib.pyplot as plt
import random as rand
class Dataset:
    def plot_image(self, img): #Lihtsalt plottimis funktsioon kontrolliks. Tavaliselt ei kasuta.
        plt.imshow(img, cmap="gray")
        plt.show()
    def image(self, dchart, slice_length):
        length = dchart.shape[0]
        img = np.zeros((length, 13), dtype = 'float32')
        for i in range(length):
            ypos = int(dchart[i])+6
            if ypos<0: ypos = 0
            elif ypos>12: ypos = 12
            img[i, ypos] = 1
        return img
    def visualizer1(self, chart, pos):
        if pos < 500 or pos >= chart.length:pos+=500
        size = 20
        dev5 = chart.dev5[(pos-size+1):(pos+1)]
        dev25 = np.empty(size)
        a = 0
        for i in range((pos-size*5+1), (pos+1), 5):
            dev25[a] = chart.dev25[i]
            a+=1
        dev125 = np.empty(size)
        a = 0
        for i in range((pos-size*25+1), (pos+1), 25):
            dev125[a] = chart.dev125[i]
            a += 1

        data = np.concatenate([dev5, dev25, dev125])
        return data

    def visualizer(self, chart, pos):
        size = 60
        delta = chart.delta[(pos-size+1):(pos+1)]*10000
        rsi = chart.rsi[(pos-size+1):(pos+1)]/50
        dev5 = chart.dev5[(pos - size + 1):(pos + 1)]

        arr = np.vstack([delta, rsi, dev5])

        arr = arr.reshape((size, 3))

        return arr
    def __init__(self, chart, start, stop, amount):
        self.slice_length = 100
        if(start<self.slice_length):start = self.slice_length
        if(stop+2>chart.length):stop=chart.length-1  #Igaks juhuks et mingit out of bounds paska ei tuleks
        if(amount%2==1):amount-=1 #Peab olema paaris

        #Loome listi positsioonidest graafikul mille järgi loome dataseti. List on juba balanced ehk buysid ja selle on ühepalju
        half = amount//2
        buys = np.empty(half, dtype='int32')
        sells = np.empty(half, dtype='int32')
        sellcount = 0
        while(sellcount<half):
            pos = rand.randrange(start, stop) #Võtab suvalise koha graafikul
            if(chart.direction[pos]==0):
                sells[sellcount]=pos
                sellcount+=1
        buycount = 0
        while (buycount < half):
            pos = rand.randrange(start, stop)  # Võtab suvalise koha graafikul
            if (chart.direction[pos] == 1):
                buys[buycount]=pos
                buycount += 1
        trades = np.concatenate([buys, sells])
        np.random.shuffle(trades)
        print("Created indexes")

        self.x = np.empty((amount, 60, 3), dtype='float32')
        self.y = np.empty((amount, 1), dtype='float32')


        for i in range(amount):
            pos = trades[i]
            # arr = chart.deltabid[(pos-self.slice_length+1):(pos+1)]
            self.x[i] = self.visualizer(chart, pos)
            self.y[i, 0] = chart.direction[pos]

