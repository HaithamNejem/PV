import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
from System import PVSys
import simulatin as sim
from datetime import timedelta, date
import matplotlib.dates as mdate


def set_date_format(system:PVSys, time_ax):
    for index in range(0,len(time_ax), 24):
        for h in range(0, 24):
            if h < 10:
                insert = f'{time_ax[index]} 0{h}:00'
            else:
                insert = f'{time_ax[index]} {h}:00'

            system.time_axis.append(insert)


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
sim.input_data(system)
sim.simulate(system)
sim.plots(system)
time_ax = []
time_stamp(system,time_ax, system.start_date, system.finish_date)

# set up start/end dates
start = system.start_date_str
end = dt.date.today()


############ plot defenisions ############

choice = str('$')
symbol = '^GSPC', choice
source = 'yahoo'
data = web.DataReader(symbol, source, start, end)['Adj Close']
numer = data.iat[0, 0]
denom = data.iat[0, 1]  # call starting date value for chosen symbol
shares = numer / denom  # compute number of shares for even start
data[choice] = shares * (pd.DataFrame(data[choice]))  # Shares*share price


##############################################
#           start animated graphs            #
##############################################


        ############ start animated graph - two days ############
x1, y1, y2, y3, y4 = [], [], [], [], []

plt.clf()

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
#axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
set_date_format(system, time_ax)    # date & time format
plt.style.use('ggplot')
fig2, axes2 = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))
plt.xticks(rotation=60, ha="right", rotation_mode="anchor")#rotate the x-axis values
plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen


def init():
        pass

def animate_day(i):
        if (len(system.car.battery_hourly) - 1) == i or (len(system.battery.storage) - 1 == i) or i == 48:
           anim.event_source.stop()

        x1.append(system.time_axis[i])

        y1.append(system.car.battery_hourly[i])
        y2.append((data[choice].values[i]))
        y3.append(system.battery.storage[i])
        y4.append(max(system.array.production[i] - system.house.consumption_data[i], 0))

        axes2.plot(x1, y1, color="red", label='Car charging')
        axes2.plot(x1, y2, color="blue")
        axes2.plot(x1, y3, color="blue", label='Reserve Battery')
        axes2.plot(x1, y4, color="green", label='excess charge')
        if i == 0:
            plt.legend(loc="upper left")
        #axes2.plot(x1, y3, color="black")



try:
        anim = FuncAnimation(fig2, animate_day, init_func=init, interval=300)
        plt.xlabel('Time')
        plt.ylabel('Watt')
        plt.title('Car & Reserve Battery')
        plt.legend(loc="upper left")
        plt.show()
except IndexError as e:
        print(e)
        print(sys.exc_type)



        ############ start animated graph - infinity ############

x1, y1, y2, y3 = [], [], [], []

plt.clf()

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
set_date_format(system, time_ax)    # date & time format
plt.style.use('ggplot')
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))
plt.xticks(rotation=60, ha="right", rotation_mode="anchor")#rotate the x-axis values
plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen

def animate(i):
    if (len(system.house.consumption_data) - 1) == i or (len(system.array.production) - 1 == i):
        anim.event_source.stop()

    x1.append(system.time_axis[i])

    y1.append(system.house.consumption_data[i])
    y2.append((data[choice].values[i]))
    y3.append(system.array.production[i])
    # x1.append(data['^GSPC'].index[i])
    # y1.append((data['^GSPC'].values[i]))

    # for label in axes.get_xticklabels(which='major'):
    #    label.set(rotation=30, horizontalaligment='right')

    axes.plot(x1, y1, color="red", label='House Consumption')
    axes.plot(x1, y2, color="blue")
    axes.plot(x1, y3, color="blue", label='PV Producing')
    # axes.plot(x1, y3, color="black")
    if i == 0:
        plt.legend(loc="upper left")


try:
        anim = FuncAnimation(fig, animate, init_func=init, interval=300)
        # plt.plot(data)
        plt.xlabel('Time')
        plt.ylabel('Watt')
        plt.title('House & Array Panels')
        plt.legend(loc="upper left")
        plt.show()
except IndexError as e:
        print(e)
        print(sys.exc_type)