import pandas as pd
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
import random
import PySimpleGUI as sg
from datetime import timedelta, date


# System Data impoting
import sys

# Class importing
sys.path.append(".")
from System import PVSys
from System import Array
from System import Battery
from System import Inverter
from System import House




################### Gui - arguments ###################

def get_input_args():
    budget_settings = [[sg.Text('Start date:'), sg.In(key="Start_date"),
                    sg.CalendarButton("Choose", default_date_m_d_y=(12, 16, 2019), format="%d-%m-%Y")],

                   [sg.Text('Finish date:'), sg.In(key="Finish_date"),
                    sg.CalendarButton("Choose", default_date_m_d_y=(12, 16, 2019), format="%d-%m-%Y")],

                   [sg.Text('Number of Panels:'), sg.In(size=5, key="PV_size")],

                   [sg.Text('Battery Capacity [KWh]:'), sg.In(size=10, key="Battery_capacity")],

                   [sg.Text('Car Battery Capacity [KWh]:'), sg.In(size=10, key="car")],

                   [sg.Button('Start Simulation')]]

    #sg.theme('LightGreen3')

    input_dates = sg.Window(title="Insert simulation settings", layout=budget_settings, margins=(100, 50)).read()
    #extracting
    start_month = int((input_dates[1])['Start_date'][3])*10 + int((input_dates[1])['Start_date'][4])
    finish_month = int((input_dates[1])['Finish_date'][3])*10 + int((input_dates[1])['Finish_date'][4])
    start_date, finish_date = (input_dates[1])['Start_date'], (input_dates[1])['Finish_date']
    pv_size = int((input_dates[1])['PV_size'])
    battery_capacity = int((input_dates[1])['Battery_capacity'])
    car = int((input_dates[1])['car'])

    return start_date, finish_date, start_month, finish_month, pv_size, battery_capacity, car

# --------- Input file analysing for the system ----------
# insert system arguments & house consumption into system Data Structure
def input_data(system:PVSys):

    #system arguments & dates
    st_date, f_date, system.start_month, system.finish_month, \
    system.array.cells_num, system.battery.capacity, system.car.battery_capacity = get_input_args()
    #system.start_month, system.finish_month, \
    #system.array.cells_num, system.battery.capacity = 11, 12, 50, 5000

    st_date, f_date = st_date.split('-'), f_date.split('-')
    st_date,  f_date = tuple(st_date), tuple(f_date)
    system.start_date = date(int(st_date[2]),int(st_date[1]),int(st_date[0]))
    system.finish_date = date(int(f_date[2]),int(f_date[1]),int(f_date[0]))
    system.start_date_str = str(system.start_date)
    system.finish_date_str = str(system.finish_date)

    mo = 1
    for file in glob.glob(r"./radiation_data_csv/*.csv"):
        v = pd.read_csv(file)
        if not(mo < system.start_month or mo > system.finish_month):
            system.radiation_data_monthly.append(list(v['solarradiation']))
            system.radiation_data_hourly = system.radiation_data_hourly + system.radiation_data_monthly[len(system.radiation_data_monthly)-1]
        mo = mo + 1

    # PV production
    for rad in system.radiation_data_hourly:
        system.array.production.append(rad * system.array.cells_num * system.array.cell_area * system.array.efficiency)
    for month in range(len(system.radiation_data_monthly)):
        system.array.production_monthly.append([])
        for rad in system.radiation_data_monthly[month]:
            system.array.production_monthly[month].append(rad * system.array.cells_num * system.array.cell_area * system.array.efficiency)


    # HOUSE
    system.battery.capacity = system.battery.capacity * 1000
    # house consumptions
    house_consum = open(".\household_power_consumption.txt", 'r')
    line = house_consum.readline()
    while True:
        line = house_consum.readline()
        if line == '':
            break
        line = line.split(';')
        system.house.consumption_data.append(float(line[2])*60)
        for i in range(1,59):
            line = house_consum.readline()
            if line == '':
                break

    for i in range(len(system.house.consumption_data)):
        if system.house.consumption_data[i] > 130:
            system.house.consumption_data[i] = random.randint(70, 130)
    for i in range(len(system.house.consumption_data)):
        system.house.consumption_data[i] = system.house.consumption_data[i] * 35

    # CAR
    system.car.battery_capacity = system.car.battery_capacity * 1000
    system.car.cons_hourly = system.car.battery_capacity / 4
    # car charging time
    for day in range(7):
        for hour in range(24):
            if day == 1 and 11 < hour and hour < 16:
                system.car.charging_time.append(1)
            elif day == 3 and 16 < hour and hour < 21:
                system.car.charging_time.append(1)
            elif day == 6 and 16 < hour and hour < 21:
                system.car.charging_time.append(1)
            else:
                system.car.charging_time.append(0)

    return system

def input_car_data(system:PVSys):
    for day in range(len(system.house.consumption_data)):                      # ----------------- change number of days
        '''
        # house consumption
        consumption_pre_hour = []
        for hour in range(24):
            if (hour >= 0 and hour <=6) or hour >= 21:
                consumption_pre_hour.append(int(random.uniform(500, 1500)))
            elif (hour >= 14 and hour <= 19):
                consumption_pre_hour.append(int(random.uniform(4000, 5200)))
            else:
                consumption_pre_hour.append(int(random.uniform(1500, 2500)))
        system.house.consumption_data.append(consumption_pre_hour)
        

        # charging time of the car
        if day % 2 == 1:    # charging once per two days
            system.charging_time_per_day.append(-1)             # if -1 ignore
            continue
        charging_time_rand = random.uniform(0, 1000)
        if charging_time_rand < 500:    # 50%
            system.charging_time_per_day.append(int(random.uniform(17, 18)))
        elif charging_time_rand <= 500 and charging_time_rand < 700:  # 20%
            system.charging_time_per_day.append(int(random.uniform(13, 16)))
        else:   # 30%
            system.charging_time_per_day.append(int(random.uniform(19, 26)) % 24)
        '''



            ############ Simulation ############

# simulate the whole system per hour
def simulate(system:PVSys):

    for hour in range(min(len(system.house.consumption_data), len(system.array.production))):

        system.battery.curr_storage = system.battery.storage[len(system.battery.storage) - 1]
        # Production > Consumption
        if system.array.production[hour] > system.house.consumption_data[hour]:
            curr_volt = system.array.production[hour]
            curr_volt = curr_volt - system.house.consumption_data[hour]

            # CAR is connected
            if system.car.charging_time[hour % len(system.car.charging_time)]:
                system.car.battery_hourly.append(system.car.battery_hourly \
                    [len(system.car.battery_hourly) - 1] + system.car.cons_hourly)


                # charging CAR from PV
                if curr_volt > 0:
                    curr_volt = max(curr_volt - system.car.cons_hourly, 0)  # charging
                    needed_from_battery = system.car.cons_hourly - curr_volt

                    # charging CAR from BATTERY
                    if needed_from_battery > 0:
                        system.battery.curr_storage = max(system.battery.curr_storage - needed_from_battery, 0)

                    # excess charge go to BATTERY
                    # BATTERY isn't full
                    if system.battery.curr_storage < system.battery.capacity:
                        diff = system.battery.capacity - system.battery.curr_storage
                        system.battery.curr_storage = min(system.battery.curr_storage +\
                                                     curr_volt, system.battery.capacity)

                        curr_volt = max( curr_volt - diff, 0)
                        system.battery.storage.append(system.battery.curr_storage)
                        continue
                # discharge BATTERY to CAR
                elif system.battery.curr_storage > 0:
                    system.battery.curr_storage = max(system.battery.curr_storage - \
                                                            system.car.cons_hourly, 0)

                    system.battery.storage.append(system.battery.curr_storage)
                    continue
                # else:
                #   charge from GRID
            else:
                system.car.battery_hourly.append(0)
                system.battery.curr_storage = min(system.battery.curr_storage + curr_volt, \
                                                                    system.battery.capacity)
                system.battery.storage.append(system.battery.curr_storage)
                continue

        # Production < Consumption
        else:
            needed_volt = system.house.consumption_data[hour]
            needed_volt = needed_volt - system.array.production[hour]

            # discharge BATTERY to HOUSE
            if system.battery.curr_storage > 0:
                diff = system.battery.curr_storage - needed_volt
                needed_volt = max( needed_volt - system.battery.curr_storage, 0)
                # BATTERY is empity
                if needed_volt > 0:
                    system.battery.curr_storage = 0
                    # discharge BATTERY to CAR
                    if system.car.charging_time[hour % len(system.car.charging_time)]:
                        system.car.battery_hourly.append(system.car.battery_hourly \
                            [len(system.car.battery_hourly) - 1] + system.car.cons_hourly)
                        system.battery.curr_storage = max(system.battery.curr_storage - \
                                                          system.car.cons_hourly, 0)
                    else:
                        system.car.battery_hourly.append(0)
                    system.battery.storage.append(system.battery.curr_storage)
                    continue

                # BATTERY has excess charge
                else:
                    system.battery.curr_storage = diff

                    # discharge BATTERY to CAR
                    if system.car.charging_time[hour % len(system.car.charging_time)]:
                        system.car.battery_hourly.append(system.car.battery_hourly \
                            [len(system.car.battery_hourly) - 1] + system.car.cons_hourly)
                        system.battery.curr_storage = max(system.battery.curr_storage - \
                                                          system.car.cons_hourly, 0)
                    else:
                        system.car.battery_hourly.append(0)
                    system.battery.storage.append(system.battery.curr_storage)
                    continue
            else:
                if system.car.charging_time[hour % len(system.car.charging_time)]:
                    system.car.battery_hourly.append(system.car.battery_hourly \
                        [len(system.car.battery_hourly) - 1] + system.car.cons_hourly)
                else:
                    system.car.battery_hourly.append(0)

                system.battery.storage.append(0)        #battery is empity



        ########## Average Plots ##########

# Solar pannels - power producing - hourly
def plots(system):

    # iterations per hour
    power_24 = [0]*24
    for hour in range(len(system.radiation_data_hourly)):
        rad = system.radiation_data_hourly[hour]
        power_24[hour%24] = power_24[hour%24] + ((int(rad) * system.array.cells_num * \
             system.array.cell_area * system.array.efficiency * 24) / len(system.radiation_data_hourly))


    # -------------------- PLOTS --------------------
    # printing average radiation of the sun - for one year per hour
    #year_hours = np.arange(0,len(system.radiation_data_hourly),1)
    #

    # printing average power of the solar pannel - for one year hourly and monthly
    mpl.rcParams['lines.linewidth'] = 2
    #mpl.rcParams['lines.linestyle'] = '--'
    plt.plot(power_24)
    plt.xlabel('Time (hour)')
    plt.ylabel('Power (Watt)')
    plt.title("Solar Panel's average power per hour ")
    plt.grid()
    plt.show()

