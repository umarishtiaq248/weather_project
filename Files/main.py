from data_storage_class import *
import sys

if __name__ == "__main__":
    path, flag_and_date_list = ApplicationManager.parse_and_extract_args(sys.argv)
    ApplicationManager.load_read_store(path)
    ApplicationManager.process_report(flag_and_date_list)
