import pandas as pd
import numpy as np
import math
from datetime import datetime

class Chart:
    def generate_direction(self, pricepoints): #Genereerib graafiku mis näitab kas antud hetkel peaks võtma buy või selli. pricepoints ütleb kui palju peab hind liikuma
        pricepoints = pricepoints/100000
        self.direction = np.zeros(self.length, dtype='float32')
        for i in range(self.length-1):
            j = i+1
            price = self.bid[i]
            while(abs(self.bid[j]-price)<pricepoints and j<self.length-1):j+=1  #Liigub edasi kuni in jõudnud kohani kus j hind erineb i hinnast pricepoints võrra
            if(self.bid[j]>price):self.direction[i] = 1
        print("Created direction chart")

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
        self.generate_direction(1)

    def calculate_moving_average(self, period):
        length = self.length
        ma = np.zeros(length, dtype='float32')
        sd = np.zeros(length, dtype='float32')
        average = 0.0
        avdevsum = 0.0
        for i in range(0, period):
            average += self.bid[i]
            ma[i] = average / (i + 1)
            avdevsum += (self.bid[i] - ma[i]) ** 2
        for i in range(period, length): #arvutab liugkeskmise ja ühe standardhälbe väärtuse
            average += self.bid[i]
            average -= self.bid[i - period]
            ma[i] += average / period
            avdevsum += (self.bid[i] - ma[i]) ** 2
            avdevsum -= (self.bid[i - period] - ma[i - period]) ** 2
            sd[i] = math.sqrt(avdevsum / period)
        for i in range(0, period): #Paneb kõige esimesed standardhälbed selleks mis esimesena arvutati
            sd[i] = sd[period]
        return (ma, sd)

    def calculate_RSI(self, period): #Arvutab relative strength indexi
        length = self.length
        rsi = np.zeros(length, dtype='float32')
        sum_gain = 0
        sum_loss = 0

        for i in range(0, period):
            if(self.deltabid[i] < 0):sum_loss-=self.deltabid[i]
            else:sum_gain+=self.deltabid[i]

        for i in range(period, length):
            if (self.deltabid[i] < 0):sum_loss-=self.deltabid[i]
            else:sum_gain += self.deltabid[i]
            if (self.deltabid[i-period] < 0):sum_loss+=self.deltabid[i-period]
            else:sum_gain -= self.deltabid[i-period]
            rsi[i] = 100-100/(sum_gain/sum_loss+1)
        for i in range(0, period):
            rsi[i] = rsi[period]
        return rsi


    def normalize(x): #Normaliseerib mingi teatud jada
        def sigmoid(x):
            for i in range(len(x)):
                x[i] = 1 / (1 + math.exp(-x[i]))
            return x
        return sigmoid(x) * 2 - 1