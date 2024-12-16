import os
from datetime import datetime,date


class SingleFieldRecord:
    # def __int__(self,val):
    #     self.val=val
    #     return self.val if val is int else raiseExceptions

    def __init__(self, *args):
        self.pkt: date = datetime.strptime(args[0],'%Y-%m-%d').date()
        self.max_temperature: int = int(args[1])
        self.mean_temperature: int = int(args[2])
        self.min_temperature: int = int(args[3])
        self.max_dew_point: int = int(args[4])
        self.mean_dew_point: int = int(args[5])
        self.min_dew_point: int = int(args[6])
        self.max_humidity: int = int(args[7])
        self.mean_humidity: int = int(args[8])
        self.min_humidity: int = int(args[9])
        self.max_sea_level_pressure: float = float(args[10])
        self.mean_sea_level_pressure: float = float(args[11])
        self.min_sea_level_pressure: float = float(args[12])
        self.max_visibility: float = float(args[13])
        self.mean_visibility: float = float(args[14])
        self.min_visibility: float = float(args[15])
        self.max_wind_speed: int = int(args[16])
        self.mean_wind_speed: int = int(args[17])
        self.max_gust_speed: int = int(args[18])
        self.precipitation: float = float(args[19])
        self.cloud_cover: int = int(args[20])
        self.events: str = str(args[21])
        self.wind_dir_degrees: int = int(args[22])

    # def __str__(self):
    #     return (f'Max temperature:{self.max_temperature}\n'
    #             f'Min Temperature:{self.min_temperature}\n'
    #             f'Max Humidity:{self.max_humidity}\n'
    #             f'Min Humidity:{self.min_humidity}')

#load,read and store all record
class LRSAllRecord:
    def __init__(self,relative_path):
        self.relative_path=relative_path
        #list to store instances
        self.instance_list=[]
    def read_path(self):
        cwd=os.getcwd()
        abs_path=os.path.join(cwd,self.relative_path)
        files_list = os.listdir(abs_path)
        for file_name in files_list:
            single_file_path = os.path.join(abs_path, file_name)
            if os.path.isfile(single_file_path):
                with open(single_file_path, 'r') as report:
                    # Header line of every file
                    report.readline()
                    for line in report:
                        record = line.split(',')
                        record = [item.strip() for item in record]
                        if len(record) <= 0:
                            continue
                        else:
                            updated_record = [None if item == '' else item for item in record]
                            single_field_instance = SingleFieldRecord(*updated_record)
                            self.instance_list.append(single_field_instance)
        return self.instance_list

class ReportGenerator:
    def __init__(self,selected_instances):
        self.selected_instances=selected_instances
    def task1(self):
        # for finding maximum temperature
        max_temperature=self.selected_instances[0].max_temperature
        max_temperature_date=self.selected_instances[0].pkt
        for single_value in self.selected_instances:
            if single_value.max_temperature > max_temperature:
                max_temperature_date=single_value.pkt
                max_temperature = single_value.max_temperature

        # for finding minimum temperature
        min_temperature = self.selected_instances[0].min_temperature
        min_temperature_date = self.selected_instances[0].pkt
        for single_value in self.selected_instances:
            if single_value.min_temperature < min_temperature:
                min_temperature_date = single_value.pkt
                min_temperature = single_value.min_temperature

        #for finding maximum humidity
        max_humidity = self.selected_instances[0].max_humidity
        max_humidity_date = self.selected_instances[0].pkt
        for single_value in self.selected_instances:
            if single_value.max_humidity > max_humidity:
                max_humidity_date = single_value.pkt
                max_humidity = single_value.max_humidity
        print(f'Highest:{max_temperature}C on {max_temperature_date}')
        print(f'Lowest:{min_temperature}C on {min_temperature_date}')
        print(f'Humidity:{max_humidity}% on {max_humidity_date}')

    def task2(self):
        total_count = len(self.selected_instances)

        # for finding average maximum temperature
        total_max_temperature=0
        for single_value in self.selected_instances:
            total_max_temperature+=single_value.max_temperature
        avg_max_temperature=total_max_temperature/total_count

        # for finding average minimum temperature
        total_min_temperature = 0
        for single_value in self.selected_instances:
            total_min_temperature += single_value.min_temperature
        avg_min_temperature = total_min_temperature / total_count

        #for finding average maximum humidity
        total_max_humidity = 0
        for single_value in self.selected_instances:
            total_max_humidity += single_value.max_humidity
        avg_max_humidity = total_max_humidity / total_count
        print(f'Highest:{round(avg_max_temperature,3)}C')
        print(f'Lowest:{round(avg_min_temperature,3)}C')
        print(f'Humidity:{round(avg_max_humidity,3)}%')

    def task3(self):
        blue = '\033[34m'  # Blue color
        red = '\033[31m'  # Red color
        reset = '\033[0m'  # Reset to default color
        for count,single_value in enumerate(self.selected_instances):
            # Number of "+" signs
            max_temperature = single_value.max_temperature
            min_temperature = single_value.min_temperature
            print(count,end='')
            for i in range(max_temperature):
                print(f'{red}+{reset}',end='')
            print(max_temperature,'\n')
            print(count,end='')
            for i in range(min_temperature):
                print(f'{blue}+{reset}',end='')
            print(min_temperature,'\n')

    def task4(self):
        blue = '\033[34m'  # Blue color
        red = '\033[31m'  # Red color
        reset = '\033[0m'  # Reset to default color
        for count,single_value in enumerate(self.selected_instances,1):
            # Number of "+" signs
            max_temperature = single_value.max_temperature
            min_temperature = single_value.min_temperature
            print(count,end='')
            for i in range(min_temperature):
                print(f'{blue}+{reset}',end='')
            for i in range(max_temperature):
                print(f'{red}+{reset}',end='')
            print(f'{min_temperature}C-{max_temperature}C','\n')


class Calculation:
    def __init__(self,instance_record):
        self.instance_record=instance_record
        self.calculated_instance=[]

    def year_calculation(self, year):
        year = int(year) if len(year) == 4 else None
        for instance in self.instance_record:
            if instance.pkt.year == year:
                self.calculated_instance.append(instance)
        return self.calculated_instance
    def monthly_calculation(self, year, month):
        year = int(year) if len(year) == 4 else None
        month = int(month) if len(month) == 2 else None
        for instance in self.instance_record:
            if (instance.pkt.month == month) & (instance.pkt.year == year):
                self.calculated_instance.append(instance)
        return self.calculated_instance