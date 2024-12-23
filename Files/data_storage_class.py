import os, sys
from datetime import datetime


class WeatherRecord:
    all_record_objects = []

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "PKT":  # Handle 'pkt' separately (as a date)
                setattr(
                    self,
                    "pkt",
                    (
                        datetime.strptime(value.lower(), "%Y-%m-%d").date()
                        if value and 10 >= len(value) > 5
                        else None
                    ),
                )
            elif key == "Events":  # Handle 'Events' as a string
                setattr(
                    self,
                    "events",
                    str(value).replace(" ", "_").lower() if value is not None else None,
                )
            else:  # Handle all other values as float
                setattr(
                    self,
                    key.replace(" ", "_").lower()[:-1],
                    float(value) if value is not None else None,
                )

    @classmethod
    def required_objects_calculation(cls, single_date):
        user_required_objects = []
        for single_object in cls.all_record_objects:
            try:
                if single_date == "Y":
                    if single_date.year == single_object.pkt.year:
                        user_required_objects.append(single_object)
                else:
                    if (single_date.year == single_object.pkt.year) and (
                        single_date.month == single_object.pkt.month
                    ):
                        user_required_objects.append(single_object)
            except AttributeError as e:
                pass
        return user_required_objects

    # Store every line of file
    @classmethod
    def store_data(cls, single_line, heading):
        record = single_line.split(",")
        heading = heading.split(",")
        record = [item.strip() for item in record]
        heading = [item.strip() for item in heading]
        if len(record) <= 1:
            pass
        else:
            single_record = [None if item == "" else item for item in record]
            temp_dic = dict(zip(heading, single_record))
            temp_object = cls(**temp_dic)
            cls.all_record_objects.append(temp_object)

    # Open every file to read the data
    @classmethod
    def read_path(cls, single_file_path):
        if os.path.isfile(single_file_path):
            with open(single_file_path, "r") as report:
                # Header line of every file
                heading = report.readline()
                for single_line in report:
                    cls.store_data(single_line, heading)

    # Get folder path from user and make a list of abs path for all weather record file
    @classmethod
    def load_path(cls, relative_path):
        cwd = os.getcwd()
        abs_path = os.path.join(cwd, relative_path)
        files_list = os.listdir(abs_path)
        for file_name in files_list:
            single_file_path = os.path.join(abs_path, file_name)
            cls.read_path(single_file_path)


class ReportGenerator:
    @staticmethod
    def task1(selected_instances):
        max_value_instance = max(selected_instances, key=lambda x: x.max_temperature)
        max_temperature = max_value_instance.max_temperature
        max_temperature_date = max_value_instance.pkt
        # for finding minimum temperature
        min_value_instance = max(selected_instances, key=lambda x: x.min_temperature)
        min_temperature = min_value_instance.min_temperature
        min_temperature_date = min_value_instance.pkt

        # for finding maximum humidity
        max_humidity_instance = max(selected_instances, key=lambda x: x.max_humidit)
        max_humidity = max_humidity_instance.max_humidit
        max_humidity_date = max_humidity_instance.pkt
        print(f"Highest:{max_temperature}C on {max_temperature_date}")
        print(f"Lowest:{min_temperature}C on {min_temperature_date}")
        print(f"Humidity:{max_humidity}% on {max_humidity_date}")

    @staticmethod
    def task2(selected_instances):
        total_count = len(selected_instances)

        # for finding average maximum temperature
        total_max_temperature = 0
        for single_value in selected_instances:
            total_max_temperature += single_value.max_temperature
        avg_max_temperature = total_max_temperature / total_count

        # for finding average minimum temperature
        total_min_temperature = 0
        for single_value in selected_instances:
            total_min_temperature += single_value.min_temperature
        avg_min_temperature = total_min_temperature / total_count

        # for finding average maximum humidity
        total_max_humidity = 0
        for single_value in selected_instances:
            total_max_humidity += single_value.max_humidit
        avg_max_humidity = total_max_humidity / total_count
        print(f"Highest:{round(avg_max_temperature,2)}C")
        print(f"Lowest:{round(avg_min_temperature,2)}C")
        print(f"Humidity:{round(avg_max_humidity,2)}%")

    @staticmethod
    def task3(selected_instances):
        blue = "\033[34m"  # Blue color
        red = "\033[31m"  # Red color
        reset = "\033[0m"  # Reset to default color
        for count, single_value in enumerate(selected_instances):
            # Number of "+" signs
            max_temperature = single_value.max_temperature
            min_temperature = single_value.min_temperature
            print(count, end="")
            for i in range(max_temperature):
                print(f"{red}+{reset}", end="")
            print(max_temperature, "\n")
            print(count, end="")
            for i in range(min_temperature):
                print(f"{blue}+{reset}", end="")
            print(min_temperature, "\n")

    @staticmethod
    def task4(selected_instances):
        blue = "\033[34m"  # Blue color
        red = "\033[31m"  # Red color
        reset = "\033[0m"  # Reset to default color
        for count, single_value in enumerate(selected_instances, 1):
            # Number of "+" signs
            max_temperature = single_value.max_temperature
            min_temperature = single_value.min_temperature
            print(count, end="")
            for i in range(min_temperature):
                print(f"{blue}+{reset}", end="")
            for i in range(max_temperature):
                print(f"{red}+{reset}", end="")
            print(f"{min_temperature}C-{max_temperature}C", "\n")

    @classmethod
    def report_caller(cls, *flags_and_dates):
        for i, single_value in enumerate(flags_and_dates, start=1):
            flag = single_value[1]
            single_date = single_value[0]
            req_instances = WeatherRecord.required_objects_calculation(single_date)
            print("Report ", i)
            if flag == "-e":
                print("Task 1")
                cls.task1(req_instances)
            elif flag == "-a":
                print("Task 2")
                cls.task2(req_instances)
            elif flag == "-c":
                print("Task 3")
                cls.task3(req_instances)
                print("Task 4")
                cls.task4(req_instances)
            else:
                pass


class ArgumentParser:
    def __init__(self, *args):
        self.path = args[0]
        self.flags_and_dates = []

    def argument_generator(self):
        skip_loop = False
        for index in range(2, len(sys.argv[2:]) + 2):
            if skip_loop:
                skip_loop = False
                continue
            elif len(sys.argv[index]) == 2:
                if len(sys.argv[index + 1]) == 4:  # The string contains only the year
                    temp_date = datetime.strptime(
                        sys.argv[index + 1], "%Y"
                    ).date()  # Only year
                    self.flags_and_dates.append((temp_date, sys.argv[index], "Y"))
                else:  # The string contains year and month
                    temp_date = datetime.strptime(
                        sys.argv[index + 1], "%Y/%m"
                    ).date()  # Year and month
                    self.flags_and_dates.append((temp_date, sys.argv[index], "YM"))
                skip_loop = True
            else:
                if len(sys.argv[index]) == 4:  # The string contains only the year
                    temp_date = datetime.strptime(
                        sys.argv[index], "%Y"
                    ).date()  # Only year
                    self.flags_and_dates.append((temp_date, "-n", "Y"))
                else:  # The string contains year and month
                    temp_date = datetime.strptime(
                        sys.argv[index], "%Y/%m"
                    ).date()  # Year and month
                    self.flags_and_dates.append((temp_date, "-n", "YM"))
        return self.path, *self.flags_and_dates
