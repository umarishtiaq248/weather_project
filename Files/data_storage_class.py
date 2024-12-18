import os
from datetime import datetime,date

class WeatherRecords:
    all_record_object = []
    user_required_object = []
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'PKT':  # Handle 'PKT' separately (as a date)
                setattr(self, 'PKT', datetime.strptime(value, '%Y-%m-%d').date() if value and len(value) > 5 else None)
            elif key == 'Events':  # Handle 'Events' as a string
                setattr(self, 'Events', str(value) if value is not None else None)
            else:  # Handle all other values as float
                setattr(self, key, float(value) if value is not None else None)

    # def user_required_calculations(self,single_instance,*user_input_date):
    #     for single_date in user_input_date:
    #         try:
    #             if single_date[1]=="Y":
    #                 if single_date[0].year==single_instance.pkt.year:
    #                     instance_record.user_required_instance.append(single_instance)
    #             else:
    #                 if (single_date[0].year==single_instance.pkt.year) and (single_date[0].month==single_instance.pkt.month):
    #                     instance_record.user_required_instance.append(single_instance)
    #         except AttributeError as e:
    #             pass
    #Store every line of file
    @staticmethod
    def store_data(single_line,heading):
        record = single_line.split(',')
        heading=heading.split(',')
        record = [item.strip() for item in record]
        heading = [item.strip() for item in heading]
        if len(record) <= 1:
            pass
        else:
            single_record = [None if item == '' else item for item in record]
            temp_dic=dict(zip(heading, single_record))
            temp_object = WeatherRecords(**temp_dic)
            WeatherRecords.all_record_object.append(temp_object)
    #Open every file to read the data
    @staticmethod
    def read_path(single_file_path):
        if os.path.isfile(single_file_path):
            with open(single_file_path, 'r') as report:
                # Header line of every file
                heading=report.readline()
                for single_line in report:
                    WeatherRecords.store_data(single_line,heading)
    # Get folder path from user and make a list of abs path for all weather record file
    @classmethod
    def load_path(cls,relative_path):
        cwd=os.getcwd()
        abs_path=os.path.join(cwd,relative_path)
        files_list = os.listdir(abs_path)
        for file_name in files_list:
            single_file_path = os.path.join(abs_path, file_name)
            cls.read_path(single_file_path)

#
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

