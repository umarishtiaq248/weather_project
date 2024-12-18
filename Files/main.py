from  data_storage_class import *
import sys
from datetime import datetime,date
instance_record=InstanceRecord()
def user_input(relative_path,*date_list):
    LoadReadAllRecords(relative_path,).read_path()
    for single_instance in instance_record.all_record_instance:
        single_instance.user_required_calculations(single_instance,*date_list)

    report_generator=ReportGenerator(instance_record.user_required_instance)

    print('Task 1\n')
    report_generator.task1()
    print('Task 2\n')
    report_generator.task2()
    print('Task 3\n')
    report_generator.task3()
    print('Task 4\n')
    report_generator.task4()

if __name__ == '__main__':
    path = sys.argv[1]
    user_input_flag_date=[]
    skip_loop=False
    for index in range(2,len(sys.argv[2:])+2):
        if skip_loop:
            skip_loop = False
            continue
        elif len(sys.argv[index])==2:
            if len(sys.argv[index+1]) == 4:# The string contains only the year
                temp_date = datetime.strptime(sys.argv[index+1], "%Y").date()  # Only year
                user_input_flag_date.append((temp_date,sys.argv[index],"Y"))
            else:  # The string contains year and month
                temp_date = datetime.strptime(sys.argv[index+1], "%Y/%m").date()  # Year and month
                user_input_flag_date.append((temp_date,sys.argv[index],"YM"))
            skip_loop = True
        else:
            if len(sys.argv[index]) == 4:  # The string contains only the year
                temp_date = datetime.strptime(sys.argv[index], "%Y").date()  # Only year
                user_input_flag_date.append((temp_date, '-n', "Y"))
            else:  # The string contains year and month
                temp_date = datetime.strptime(sys.argv[index], "%Y/%m").date()  # Year and month
                user_input_flag_date.append((temp_date, '-n', "YM"))
    user_input(path,*user_input_flag_date)
