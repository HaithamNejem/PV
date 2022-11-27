from datetime import timedelta, date

class Array:
    def __init__(self, cells_num, cell_area, efficiency):
        self.efficiency = efficiency
        self.cells_num = cells_num
        self.cell_area = cell_area
        self.production = []
        self.production_monthly = []

class Battery:
    def __init__(self, capacity):
        self.capacity = capacity
        self.curr_storage = 0

        # DATA to save
        self.storage = [0]

class House:
    def __init__(self):
        self.input_power_PV = 0
        self.input_power_Battery = 0
        # DATA to save
        self.consumption_data = []    # list of days lists
        self.consumption_from_pv = []
        self.consumption_from_ba = []

    '''
    set input power and save the input data - per hour
        inputs : the current hour of the year, power that PV and Battery could supply
        return : the consumption from PV, Battery
    '''
    def set_power(self, glob_hour, power_pv, power_ba):
        if self.consumption_data[glob_hour] > power_pv:
            self.consumption_from_pv.append(power_pv)
            self.consumption_from_ba.append(0)
            return power_pv, 0
        elif power_pv > 0:
            self.consumption_from_pv.append(self.consumption_data[glob_hour])
            self.consumption_from_ba.append(0)
            return self.consumption_data[glob_hour], 0
        elif self.consumption_data[glob_hour] > power_ba:
            self.consumption_from_pv.append(0)
            self.consumption_from_ba.append(power_ba)
            return 0, power_ba
        elif power_ba > 0:
            self.consumption_from_pv.append(0)
            self.consumption_from_ba.append(self.consumption_data[glob_hour])
            return 0, self.consumption_data[glob_hour]
        else:
            print("WARNING - Battery method, should not get here!")

class Car:
    def __init__(self):
        self.cons_hourly = 3000
        self.battery_capacity = 12000
        self.charging_time = []

        #DATA
        self.battery_hourly = [0]


class Inverter:
    def __init__(self):
        self.output_factor = 1000/1350

class Hour:
    def __init__(self):
        self.hour = 0
    def inc_hour(self):
        self.hour = (self.hour + 1)%24
    def get_hour_as_str(self):
        if self.hour < 10:
            return f'0{self.hour}:00'
        else:
            return f'{self.hour}:00'


class PVSys:
    def __init__(self, cell_area=2.52, efficiency=0.2, battery_capacity=1000, cells_num=40):

        # Objects definition:
        self.array = Array(cells_num, cell_area, efficiency)
        self.battery = Battery(battery_capacity)
        self.house = House()
        self.car = Car()


        # DATA to save
        # Radiation
        self.radiation_data_monthly = []
        self.radiation_data_hourly = []

        # Dates & Time:
        self.start_month = 10
        self.finish_month = 12
        self.start_date = date(2019, 10, 1)
        self.finish_date = date(2019, 12, 30)
        self.start_date_str = "2019-11-01"
        self.finish_date_str = "2019-11-30"

        self.dates = []
        self.time_axis = []

        # hour = Hour()

        #self.inverter = Inverter(v_dc, p_dc)

        # Cables definition:
        self.PV_WC = 0
        self.PV_BA = 0
        self.PV_INV = 0
        self.B_WC = 0
        self.B_INV = 0
        self.INV_HO = 0
        self.GRID_HO = 0
