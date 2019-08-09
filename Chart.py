import pandas as pd
import numpy as np
import math
from datetime import datetime

class Chart:
    def __init__(self, path):
        self.path = path
        headers = ['time', 'bid', 'ask', 'bidvolume', 'askvolume']
        df = pd.read_csv(path, names=headers)
        self.length = df.shape[0]

        #self.bid = np.empty(self.length, dtype='float32') #bid hind
        #self.ask = np.empty(self.length, dtype='float32') #ask hind (kõrgem)

        self.deltat = np.empty(self.length, dtype='float32')
        self.deltabid = np.empty(self.length, dtype='float32')
        self.clock = np.array(df['time'])
        self.bid = df['bid'].values #bid hind
        self.ask = df['ask'].values #ask hind (kõrgem)
        spread = (self.ask - self.bid) * 100000 #arvutame spreadi (pippides)

        #Paneb esimesed nulliks
        self.deltat[0] = 0
        self.deltabid[0] = 0

        timeFormat = '%H:%M:%S.%f'
        for i in range(1, self.length): #Arvutab timestampide järgi igale tickile aja mis kulus eelmisest tickist millisekundites
            diff = datetime.strptime(df.at[i, 'time'], timeFormat) - datetime.strptime(df.at[i - 1, 'time'], timeFormat)
            self.deltat[i] = diff.microseconds / 1000 + diff.seconds * 1000
            self.deltabid[i] = (self.bid[i] - self.bid[i - 1]) * 100000 #Arvutab hinna muutuse (tuletise) pippides

    def calculate_moving_average(self, period):
        length = self.length
        ma = np.zeros(length, dtype='float32')
        sd = np.zeros(length, dtype='float32')
        average = 0.0
        avdevsum = 0.0
        for i in range(0, period): #arvutab liugkeskmise
            average += self.bid[i]
            ma[i] = average / (i + 1)
            avdevsum += (self.bid[i] - ma[i]) ** 2
        for i in range(period, length): #arvutab ühe standardhälbe väärtuse
            average += self.bid[i]
            average -= self.bid[i - period]
            ma[i] += average / period
            avdevsum += (self.bid[i] - ma[i]) ** 2
            avdevsum -= (self.bid[i - period] - ma[i - period]) ** 2
            sd[i] = math.sqrt(avdevsum / period)
        for i in range(0, period): #Paneb kõige esimesed standardhälbed selleks mis esimesena arvutati
            sd[i] = sd[period]
        return (ma, sd)

    def normalize(x): #Normaliseerib mingi teatud jada
        def sigmoid(x):
            for i in range(len(x)):
                x[i] = 1 / (1 + math.exp(-x[i]))
            return x
        return sigmoid(x) * 2 - 1