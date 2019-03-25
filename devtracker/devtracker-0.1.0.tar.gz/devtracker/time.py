import csv

from .dir_and_path_helpers import mk_file_path, check_file
from .time_and_date_helpers import get_date, get_time, total_time

def make_project_csv(dir):
    if check_file(mk_file_path(dir)):
        start_time(dir)
    else:
        print("[+] First time working on {0}, creating file...".format(dir))
        initalize_list = ["start_date", "start_time", "end_date", "end_time", "total"]
        with open(mk_file_path(dir), 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(initalize_list)
        start_time(dir)

def start_time(dir):
    start_arr = [get_date(), get_time()]

    with open(mk_file_path(dir), 'r', newline='') as myFile:
        reader = list(csv.reader(myFile))
        last_row = reader.pop()
        if len(last_row) == 2:
            print("[-] You are already tracking this project.")
        else:
            with open(mk_file_path(dir), 'a', newline='') as myfile:
                wr = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                wr.writerow(start_arr)
            print("[+] Starting work on {0}".format(dir))


def end_time(dir):
    end_date = get_date()
    end_time = get_time()

    if check_file(mk_file_path(dir)):
        with open(mk_file_path(dir), 'r', newline='') as myFile:
            reader = list(csv.reader(myFile))
            last_row = reader.pop()
            if len(last_row) == 2:
                total = total_time(last_row[1], end_time)
                last_row.extend([end_date, end_time, total])
                reader.append(last_row)
                with open(mk_file_path(dir), 'w', newline='') as myfile:
                    wr = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                    for i in reader:
                        wr.writerow(i)
                    print("[+] Stopped tracking in {0}, with a total time of {1}!".format(dir, total))
            else:
                reader.append(last_row)
                print("[-] 'devtracker stop' was entered.  You must run 'devtracker start' first to start tracking time first.")

    else:
        print("[-] 'devtracker stop' was entered.  You must run 'devtracker start' to create project tracking file.")

def current_status(dir):
    if check_file(mk_file_path(dir)):
        with open(mk_file_path(dir), 'r', newline='') as myFile:
            reader = list(csv.reader(myFile))
            last_row = reader.pop()
            if len(last_row) == 2:
                temp_time = get_time()
                total = total_time(last_row[1], temp_time)
                print("[+] You have been working on {0} for {1} so far. \n"
                      "Use 'devtracker stop' to stop working or continue working on this project.".format(dir, total))
            else:
                print("[+] Status report for '{0}':  You have not started work on this project yet.".format(dir))
    else:
        print("[-] 'devtracker status' was entered.  You must run 'devtracker start' to create project tracking file.")