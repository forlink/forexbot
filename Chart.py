import pandas as pd
import numpy as np
import math
from datetime import datetime
import matplotlib.pyplot as plt

class Chart:
    def generate_direction(self, pricepoints): #Genereerib graafiku mis näitab kas antud hetkel peaks võtma buy või selli. pricepoints ütleb kui palju peab hind liikuma

        pricepoints = pricepoints/100000
        self.direction = np.zeros(self.length, dtype='float32')
        for i in range(self.length-1):
            j = i+1
            price = self.close[i]
            while(abs(self.close[j]-price)<pricepoints and j<self.length-1):j+=1  #Liigub edasi kuni in jõudnud kohani kus j hind erineb i hinnast pricepoints võrra
            if(self.close[j]>price):self.direction[i] = 1
        print("Created direction chart")

    def generate_direction_time(self, minutes):
        self.direction = np.zeros(self.length, dtype='int32')
        for i in range(self.length-minutes):
            if(self.close[i+minutes]>self.close[i]):
                self.direction[i] = 1
    def calculate_moving_average(self, period):
        length = self.length
        ma = np.zeros(length, dtype='float32')
        sd = np.zeros(length, dtype='float32')
        average = 0.0
        avdevsum = 0.0
        for i in range(0, period):
            average += self.close[i]
            ma[i] = average / (i + 1)
            avdevsum += (self.close[i] - ma[i]) ** 2
        for i in range(period, length): #arvutab liugkeskmise ja ühe standardhälbe väärtuse
            average += self.close[i]
            average -= self.close[i - period]
            ma[i] += average / period
            avdevsum += (self.close[i] - ma[i]) ** 2
            avdevsum -= (self.close[i - period] - ma[i - period]) ** 2
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
            if(self.delta[i] < 0):sum_loss-=self.delta[i]
            else:sum_gain+=self.delta[i]

        for i in range(period, length):
            if (self.delta[i] < 0):sum_loss-=self.delta[i]
            else:sum_gain += self.delta[i]
            if (self.delta[i-period] < 0):sum_loss+=self.delta[i-period]
            else:sum_gain -= self.delta[i-period]
            rsi[i] = 100-100/(sum_gain/sum_loss+1)
        for i in range(0, period):
            rsi[i] = rsi[period]
        return rsi

    def __init__(self, path):
        self.path = path
        headers = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
        df = pd.read_csv(path, names=headers)
        self.length = df.shape[0]

        #self.bid = np.empty(self.length, dtype='float32') #bid hind
        #self.ask = np.empty(self.length, dtype='float32') #ask hind (kõrgem)

        self.delta = np.empty(self.length, dtype='float32')
        self.clock = np.array(df['time'])
        self.open = df['open'].values #bid hind
        self.high = df['high'].values
        self.low = df['low'].values
        self.close = df['close'].values
        self.volume = df['volume'].values

        for i in range(1, self.length):
            self.delta[i] = self.close[i]-self.close[i-1]
        self.delta[0]=0

        #Paneb esimesed nulliks

        dateFormat = '%Y,%m,%d'
        timeFormat = '%S,%M,%S'

        # for i in range(0, self.length):
        #     timestr = df.at[i, 'date'] + df.at[i, 'time']
        self.ma5, self.sd5 = self.calculate_moving_average(5)
        self.ma25, self.sd25 = self.calculate_moving_average(25)
        self.ma125, self.sd125 = self.calculate_moving_average(125)
        self.dev5 = (self.close - self.ma5) / self.sd5
        self.dev25 = (self.ma5 - self.ma25) / self.sd25
        self.dev125 = (self.ma25 - self.ma125) / self.sd125
        self.rsi = self.calculate_RSI(30)
        self.generate_direction_time(5)

    def normalize(x): #Normaliseerib mingi teatud jada
        def sigmoid(x):
            for i in range(len(x)):
                x[i] = 1 / (1 + math.exp(-x[i]))
            return x
        return sigmoid(x) * 2 - 1