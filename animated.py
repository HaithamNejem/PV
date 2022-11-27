import config

import matplotlib.pyplot as plt
from datetime import datetime
import System as sys
from simulatin import input_data


################### Date Time ###################
from datetime import timedelta, date
import matplotlib.dates as mdate

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def time_stamp(time_list, start_date = date(2019, 1, 1), end_date = date(2019, 1, 2)):

    for single_date in daterange(start_date, end_date):
        time_list.append(str(single_date.strftime("%Y-%m-%d")))
        for hour in range(1, 24):
            if hour < 10:
                time_list.append(str(f'0{hour}:00'))
            else:
                time_list.append(str(f'{hour}:00'))


################### Animated Plot ###################

import itertools
import numpy as np
import matplotlib.animation as animation

def data_gen():
    for cnt in itertools.count():
        t = cnt / 10
        yield t, system.array.production[cnt]
        #yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)


def init():
    ax.set_ylim(min(system.array.production), max(system.array.production))
    ax.set_xlim(0, 1)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,


def run(data):
    # update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    iteration[0] = iteration[0] + 1
    xmin, xmax = ax.get_xlim()

    #ax.set_xlim(xmin, 2 * xmax)
    #ax.figure.canvas.draw()
    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,


################### Code starts here ###################
system = sys.PVSys()
input_data(system)
time = []
time_stamp(time, system.start_date, system.finish_date)


fig, ax = plt.subplots()
ax.cla()
ax.set_xlabel("Time")
ax.set_ylabel("yyyy")
ax.grid()
#ax.xaxis.set_major_formatter(str)
ax.xaxis.set_units(str)


line, = ax.plot([], [], lw=2)

xdata, ydata = [], []
iteration = [0, 0]
ani = animation.FuncAnimation(fig, run, data_gen, interval=100, init_func=init)
print('gggggggfgfggfg')
plt.show()
print('gfgfggfg')

