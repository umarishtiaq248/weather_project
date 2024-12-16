from  data_storage_class import *
import sys
from datetime import datetime
def user_input(relative_path,*user_input_date):
    print(relative_path)
    all_instance_list=LRSAllRecord(relative_path).read_path()

    # result_instance = Calculation(all_instance_list)

    # # calculated_yearly_instances=result_instance.year_calculation(year)
    # calculated_monthly_instances = result_instance.monthly_calculation(year,month)
    # report_generator=ReportGenerator(calculated_monthly_instances)

    # print('Task 1\n')
    # report_generator.task1()
    # print('Task 2\n')
    # report_generator.task2()
    # print('Task 3\n')
    # report_generator.task3()
    # print('Task 4\n')
    # report_generator.task4()



path='/home/umar-ishtiaq/Projects/Weather Data/Data/weather_files'

if __name__ == '__main__':
    path = sys.argv[1]
    user_input_date=[]
    for i in sys.argv[2:]:
        if len(i) == 4:  # The string contains only the year
            temp_date = datetime.strptime(i, "%Y").date()  # Only year
            user_input_date.append(temp_date)
        else:  # The string contains year and month
            temp_date = datetime.strptime(i, "%Y/%m").date()  # Year and month
            user_input_date.append(temp_date)
    user_input(path,*user_input_date)
