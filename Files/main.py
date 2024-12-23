from data_storage_class import *
import sys


def user_input(relative_path, *flags_and_dates_list):
    WeatherRecord.load_path(relative_path)
    ReportGenerator.report_caller(*flags_and_dates_list)


if __name__ == "__main__":
    user_input_path, *flags_and_dates = ArgumentParser(
        *sys.argv[1:]
    ).argument_generator()
    user_input(user_input_path, *flags_and_dates)
