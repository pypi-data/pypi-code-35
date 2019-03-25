import csv

from datetime import datetime, timedelta
from .dir_and_path_helpers import mk_file_path, check_file
from .time_and_date_helpers import get_sec

def today_report(dir):
    total_in_sec = 0
    if check_file(mk_file_path(dir)):
        print("[+] Generating daily report for {0}...".format(dir))

        today = str(datetime.now().strftime("%Y-%m-%d"))

        with open(mk_file_path(dir), 'r', newline='') as myFile:
            reader = list(csv.reader(myFile))
            if len(reader[-1]) == 2:
                print("[-] You are in the middle of tracking, end this session with `devtracker stop` before generation a report.")
            else:
                reader.pop(0)
                for row in reader:
                    if row[0] == today:
                        total_in_sec += get_sec(row[4])

                print("[+] You have worked on {0} for a total of {1} today.  Way to go!".format(dir, str(timedelta(seconds=total_in_sec))))
    else:
        print("[-] 'devtracker report' was entered.  You must run 'devtracker start' to create project tracking file.")

def weekly_report(dir, week_num):
    total_in_sec = 0
    if check_file(mk_file_path(dir)):
        print("[+] Generating weekly report for {0}...".format(dir))

        today = datetime.now()
        week_ago = today - timedelta(days=7 * week_num +1)

        with open(mk_file_path(dir), 'r', newline='') as myFile:
            reader = list(csv.reader(myFile))
            if len(reader[-1]) == 2:
                print("[-] You are in the middle of tracking, end this session with `devtracker stop` before generation a report.")
            else:
                reader.pop(0)
                for row in reader:
                    if datetime.fromisoformat(row[0]) >= week_ago:
                        total_in_sec += get_sec(row[4])

                print("[+] You have worked on {0} for a total of {1} the last {2} weeks.  Way to go!".format(dir, str(timedelta(seconds=total_in_sec)), week_num))
    else:
        print("[-] 'devtracker report' was entered.  You must run 'devtracker start' to create project tracking file.")

def report(dir):
    total_in_sec = 0
    if check_file(mk_file_path(dir)):
        with open(mk_file_path(dir), 'r', newline='') as myFile:
            reader = list(csv.reader(myFile))
            if len(reader[-1]) == 2:
                print("[-] You are in the middle of tracking, end this session with `devtracker stop` before generation a report.")
            else:
                reader.pop(0)
                for row in reader:
                    total_in_sec += get_sec(row[4])

                print("[+] You have worked on {0} for a total of {1}.  Way to go!".format(dir, str(timedelta(seconds=total_in_sec))))
    else:
        print("[-] 'devtracker report' was entered.  You must run 'devtracker start' to create project tracking file.")

def full_report(dir):
    print("[+] Generating Full Report")
    def pad_col(col, max_width):
        return col.ljust(max_width)

    with open(mk_file_path(dir), 'r', newline='') as myFile:
        reader = csv.reader(myFile)
        all_rows = []
        all_rows.append(next(reader, None))
        for row in reader:
            row_format = []
            counter = 0
            for i in row:
                if counter == 0 or counter == 2:
                    date = datetime.strptime(i, "%Y-%m-%d")
                    row_format.append(date.strftime("%B %e, %Y"))
                    counter += 1
                elif counter == 1 or counter == 3:
                    time = datetime.strptime(i, "%H:%M:%S")
                    row_format.append(time.strftime("%l:%M %p"))
                    counter += 1
                else:
                    row_format.append(i)
            all_rows.append(row_format)

    max_col_width = [0] * len(all_rows[0])
    for row in all_rows:
        for idx, col in enumerate(row):
            max_col_width[idx] = max(len(col), max_col_width[idx])

    for row in all_rows:
        to_print = ""
        for idx, col in enumerate(row):
            to_print += pad_col(col, max_col_width[idx]) + " | "
        print("-"*len(to_print))
        print(to_print)
    print("\n")
    report(dir)

