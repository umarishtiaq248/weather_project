from  data_storage_class import *

def user_input(folder_path,year,month):

    all_instance_list=LoadAllFile(folder_path).read_path()

    result_instance = Calculation(all_instance_list)

    # calculated_yearly_instances=result_instance.year_calculation(year)
    calculated_monthly_instances = result_instance.monthly_calculation(year,month)
    report_generator=ReportGenerator(calculated_monthly_instances)

    # print('Task 1\n')
    # report_generator.task1()
    # print('Task 2\n')
    # report_generator.task2()
    # print('Task 3\n')
    # report_generator.task3()
    print('Task 4\n')
    report_generator.task4()





path='/home/umar-ishtiaq/Projects/Weather Data/Data/weather_files'


user_input(path,year='2011',month='09')

