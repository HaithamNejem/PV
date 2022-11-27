import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
from System import PVSys
import simulatin as inf
#from simulation import time_stamp
from datetime import timedelta, date
import datetime
import time
import matplotlib.dates as mdates


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def time_stamp(system:PVSys, time_list, start_date = date(2019, 1, 1), end_date = date(2019, 1, 2)):

    for single_date in daterange(start_date, end_date):
        time_list.append(str(single_date.strftime("%Y-%m-%d")))
        system.dates.append(single_date)
        for hour in range(1, 24):
            if hour < 10:
                time_list.append((str(f'0{hour}:00')))
            else:
                time_list.append(str(f'{hour}:00'))


system = PVSys()
inf.input_data(system)
time_ax = []
time_stamp(system,time_ax, system.start_date, system.finish_date)
#time_rep = time.copy()
system.time = time_ax.copy()

plt.style.use('ggplot')
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))

#plt.tight_layout()

plt.xticks(rotation=30, ha="right", rotation_mode="anchor")#rotate the x-axis values
plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen


start = system.start_date_str
end = dt.date.today()

#start = str(f'{system.start_date.month}/01/2019')
#end = str(f'{system.finish_date.month}/30/2019')

choice = str("$")
symbol = '^GSPC', choice  # S&P500 symbol and your choice for comparison
source = 'yahoo'
data = web.DataReader(symbol, source, start, end)['Adj Close']

## adjust data shares for even start:
#numer = data.iat[0, 0]
#denom = data.iat[0, 1]  # call starting date value for chosen symbol
#shares = numer / denom  # compute number of shares for even start

#data[choice] = shares * (pd.DataFrame(data[choice]))  # Shares*share price

x1, y1, y2, y3 = [], [], [], []

def set_date_format(system:PVSys, time_ax):
    for index in range(0,len(time_ax), 24):
        for h in range(0, 24):
            if h < 10:
                insert = f'{time_ax[index]} 0{h}:00'
            else:
                insert = f'{time_ax[index]} {h}:00'
            #a = (str(d.day), str(d.month), str(h), 0)
            system.time_axis.append(time.mktime(datetime.datetime.strptime(insert,"%Y-%m-%d %H:%M").timetuple()))


#axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
set_date_format(system, time_ax)
#print('aaaa')

def init():
        pass

def animate(i):
        print(i)
        if (len(system.house.consumption_data) - 1)==i or (len(system.array.production)-1 == i):
           anim.event_source.stop()

        #if i % 9 == 0:
        #fig.gca().relim()
        #fig.gca().autoscale_view()

        x1.append(time_ax[i])

        y1.append(system.house.consumption_data[i])
        y2.append((data[choice].values[i]))
        #y3.append(system.array.production[i])
        #x1.append(data['^GSPC'].index[i])
        # y1.append((data['^GSPC'].values[i]))

        #for label in axes.get_xticklabels(which='major'):
        #    label.set(rotation=30, horizontalaligment='right')

        axes.plot(x1, y1, color="red", label='Line 1')
        axes.plot(x1, y2, color="blue", label='Line 2')
        #axes.plot(x1, y3, color="black")



try:
        anim = FuncAnimation(fig, animate, init_func=init, interval=200, frames=500)
        # plt.plot(data)
        plt.xlabel('Days')
        plt.ylabel('Watt')
        plt.title('House Consumption')
        # legend(['S&P500', choice])
        plt.show()
except IndexError as e:
        print(e)
        print(sys.exc_type)

#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])