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
    def retrieve_objects_by_date(cls, single_date, data_validator):
        user_required_objects = []
        start_date = max(obj.pkt for obj in cls.all_record_objects)
        end_date = min(obj.pkt for obj in cls.all_record_objects)
        if start_date >= single_date >= end_date:
            for single_object in cls.all_record_objects:
                try:
                    if data_validator == "Y":
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
        else:
            return False

    # Open every file to read the data and store the data in class as object
    @classmethod
    def read_and_store_files(cls, all_file_path):
        for single_file_path in all_file_path:
            if os.path.isfile(single_file_path):
                with open(single_file_path, "r") as report:
                    # Header line of every file
                    heading = report.readline().split(",")
                    heading = [item.strip() for item in heading]
                    for single_line in report:
                        record = single_line.split(",")
                        record = [item.strip() for item in record]
                        if len(record) <= 1:
                            pass
                        else:
                            single_record = [
                                None if item == "" else item for item in record
                            ]
                            temp_object = cls(**dict(zip(heading, single_record)))
                            cls.all_record_objects.append(temp_object)

    # Get folder path from user and make a list of abs path for all weather record file
    @staticmethod
    def load_path(relative_path):
        cwd = os.getcwd()
        abs_path = os.path.join(cwd, relative_path)
        files_list = os.listdir(abs_path)
        all_file_path = []
        for file_name in files_list:
            all_file_path.append(os.path.join(abs_path, file_name))
        return all_file_path


class ReportGenerator:
    @staticmethod
    def task1(selected_instances):
        max_value_instance = max(
            (x for x in selected_instances if x.max_temperature is not None),
            key=lambda x: x.max_temperature,
            default=None,
        )
        max_temperature = max_value_instance.max_temperature
        max_temperature_date = max_value_instance.pkt
        # for finding minimum temperature
        min_value_instance = max(
            (x for x in selected_instances if x.min_temperature is not None),
            key=lambda x: x.min_temperature,
            default=None,
        )
        min_temperature = min_value_instance.min_temperature
        min_temperature_date = min_value_instance.pkt

        # for finding maximum humidity
        max_humidity_instance = max(
            (x for x in selected_instances if x.max_humidit is not None),
            key=lambda x: x.max_humidit,
            default=None,
        )
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
            for i in range(int(max_temperature)):
                print(f"{red}+{reset}", end="")
            print(max_temperature, "\n")
            print(count, end="")
            for i in range(int(min_temperature)):
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
            for i in range(int(min_temperature)):
                print(f"{blue}+{reset}", end="")
            for i in range(int(max_temperature)):
                print(f"{red}+{reset}", end="")
            print(f"{min_temperature}C-{max_temperature}C", "\n")

    @classmethod
    def report_caller(cls, *flags_and_dates):
        for i, single_value in enumerate(flags_and_dates, start=1):
            single_date = single_value[0]
            flag = single_value[1]
            date_validator = single_value[2]
            req_instances = WeatherRecord.retrieve_objects_by_date(
                single_date, date_validator
            )
            if req_instances:
                print("Report ", i)
                if flag == "-e":
                    if date_validator != "Y":
                        print("Flag Invalid")
                    else:
                        print("Report for given year")
                        cls.task1(req_instances)
                elif flag == "-a":
                    if date_validator != "YM":
                        print("Flag Invalid")
                    else:
                        print("Report for given month")
                        cls.task2(req_instances)
                elif flag == "-c":
                    if date_validator != "YM":
                        print("Flag Invalid")
                    else:
                        print(
                            "Separate bars for Max and Min Temperature of given month by days"
                        )
                        cls.task3(req_instances)
                        print(
                            "Single bar for Max and Min Temperature of given month by days"
                        )
                        cls.task4(req_instances)
                else:
                    print(f"No Flag found for report :{i}")
            else:
                print(f"{single_date.year} not found")


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


class ApplicationManager:
    @staticmethod
    def parse_and_extract_args(user_arguments):
        path, *flags_and_dates = ArgumentParser(
            *user_arguments[1:]
        ).argument_generator()
        return path, flags_and_dates

    @staticmethod
    def load_read_store(path):
        all_file_path = WeatherRecord.load_path(path)
        WeatherRecord.read_and_store_files(all_file_path)

    @staticmethod
    def process_report(flag_and_path):
        ReportGenerator.report_caller(*flag_and_path)