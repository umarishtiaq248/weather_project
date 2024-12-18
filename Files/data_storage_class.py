import os
from datetime import datetime,date


class InstanceRecord:
    all_record_instance=[]
    user_required_instance = []

instance_record=InstanceRecord()

class WeatherRecords:
    all_record_instance = []
    user_required_instance = []
    def __init__(self, *args):
        self.pkt: date = datetime.strptime(args[0],'%Y-%m-%d').date() if args[0] and 10>=len(args[0])>5 else None
        self.max_temperature: int = int(args[1]) if args[1] is not None else None
        self.mean_temperature: int = int(args[2]) if args[2] is not None else None
        self.min_temperature: int = int(args[3]) if args[3] is not None else None
        self.max_dew_point: int = int(args[4]) if args[4] is not None else None
        self.mean_dew_point: int = int(args[5]) if args[5] is not None else None
        self.min_dew_point: int = int(args[6]) if args[6] is not None else None
        self.max_humidity: int = int(args[7]) if args[7] is not None else None
        self.mean_humidity: int = int(args[8]) if args[8] is not None else None
        self.min_humidity: int = int(args[9]) if args[9] is not None else None
        self.max_sea_level_pressure: float = float(args[10]) if args[10] is not None else None
        self.mean_sea_level_pressure: float = float(args[11]) if args[11] is not None else None
        self.min_sea_level_pressure: float = float(args[12]) if args[12] is not None else None
        self.max_visibility: float = float(args[13]) if args[13] is not None else None
        self.mean_visibility: float = float(args[14]) if args[14] is not None else None
        self.min_visibility: float = float(args[15]) if args[15] is not None else None
        self.max_wind_speed: int = int(args[16]) if args[16] is not None else None
        self.mean_wind_speed: int = int(args[17]) if args[17] is not None else None
        self.max_gust_speed: int = int(args[18]) if args[18] is not None else None
        self.precipitation: float = float(args[19]) if args[19] is not None else None
        self.cloud_cover: int = int(args[20]) if args[20] is not None else None
        self.events: str = str(args[21]) if args[21] is not None else None
        self.wind_dir_degrees: int = int(args[22]) if args[22] is not None else None

    def user_required_calculations(self,single_instance,*user_input_date):
        for single_date in user_input_date:
            try:
                if single_date[1]=="Y":
                    if single_date[0].year==single_instance.pkt.year:
                        instance_record.user_required_instance.append(single_instance)
                else:
                    if (single_date[0].year==single_instance.pkt.year) and (single_date[0].month==single_instance.pkt.month):
                        instance_record.user_required_instance.append(single_instance)
            except AttributeError as e:
                pass

#load and read all record
class LoadReadAllRecords:
    def __init__(self,relative_path):
        self.relative_path=relative_path
        self.instance_record=instance_record
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
                        if len(record) <= 1:
                            continue
                        else:
                            updated_record = [None if item == '' else item for item in record]
                            single_field_instance = StoreCalculateUserRecords(*updated_record)
                            self.instance_record.all_record_instance.append(single_field_instance)

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
        print(f'Highest:{round(avg_max_temperature,2)}C')
        print(f'Lowest:{round(avg_min_temperature,2)}C')
        print(f'Humidity:{round(avg_max_humidity,2)}%')

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

