import os
import csv
import time

from datetime import datetime
from datetime import timedelta
from pathlib import Path
from .dir_and_path_helpers import get_working_dir, mk_file_path, check_file
from .time_and_date_helpers import get_date, get_sec, get_time, total_time
from .time import current_status, start_time, end_time, make_project_csv
from .report import today_report, full_report

# dir_and_path_helpers tests
# -----------------------------------------------------------------------------------
home = str(Path.home())

path = home + "/devtrack_projects"
if os.path.exists(path):
    pass
else:
    os.mkdir(path)

def test_install_project_folder():
    path = home + "/devtrack_projects"
    assert os.path.exists(path) == True

def test_get_working_dir():
    assert get_working_dir() == 'devtracker'

def test_mk_file_path():
    assert mk_file_path('test') == '{}/devtrack_projects/test.csv'.format(home)

def test_check_file():
    test_path = mk_file_path('test') == '{}/devtrack_projects/test.csv'.format(home)
    assert check_file(test_path) == True


# time_and_date_helpers tests
# -----------------------------------------------------------------------------------

def test_get_date():
    assert get_date() == datetime.today().strftime("%Y-%m-%d")

def test_get_time():
    assert get_time() == datetime.today().strftime("%H:%M:%S")

def test_get_sec():
    assert get_sec('00:01:00') == 60

def test_total_time():
    now = datetime.now()
    later = datetime.now() + timedelta(minutes=15)
    assert total_time(now.strftime("%H:%M:%S"), later.strftime("%H:%M:%S")) == timedelta(minutes=15)


# main method tests
# -----------------------------------------------------------------------------------
path = home + "/devtrack_projects/" + "test.csv"
make_project_csv('test')
new_start_date = datetime.today().strftime("%Y-%m-%d")
new_start_time = datetime.today().strftime("%H:%M:%S")

def test_make_project_csv():
    assert os.path.isfile(path) == True

def test_make_project_csv_initalize():
    initalize_list = ["start_date", "start_time", "end_date", "end_time", "total"]
    with open(path, 'r') as myfile:
        reader = csv.reader(myfile)
        headers = next(reader)

    assert initalize_list == headers

def test_start_time():
    with open(path, 'r') as myfile:
        reader = csv.reader(myfile)
        next(reader)
        start_info = next(reader)

    assert start_info == [new_start_date, new_start_time]

def test_end_time_total():
    time.sleep(5)
    end_time("test")
    new_end_date = str(datetime.today().strftime("%Y-%m-%d"))
    new_end_time = str(datetime.today().strftime("%H:%M:%S"))
    FMT = "%H:%M:%S"
    new_total = str(datetime.strptime(new_end_time, FMT) - datetime.strptime(new_start_time, FMT))
    with open(path, 'r') as myfile:
        reader = csv.reader(myfile)
        next(reader)
        full_entry = next(reader)

    assert full_entry == [new_start_date, new_start_time, new_end_date, new_end_time, new_total]

def test_current_status(capsys):
    current_status("test")
    captured = capsys.readouterr()
    assert captured.out == "[+] Status report for 'test':  You have not started work on this project yet.\n"



# report test
# -----------------------------------------------------------------------------------
def test_today_report_success(capsys):
    today_report("test")
    captured = capsys.readouterr()
    res_one = "[+] Generating daily report for test...\n[+] You have worked on test for a total of 0:00:05 today.  Way to go!\n"
    res_two = "[+] Generating daily report for test...\n[+] You have worked on test for a total of 0:00:06 today.  Way to go!\n"
    assert captured.out == res_one or res_two

def test_add_start():
    start_time("test")

def test_today_report_err_one(capsys):
    today_report("test")
    captured = capsys.readouterr()
    assert captured.out == "[+] Generating daily report for test...\n[-] You are in the middle of tracking, end this session with `devtracker stop` before generation a report.\n"

def test_no_dir_error(capsys):
    today_report("no_dir")
    captured = capsys.readouterr()
    assert captured.out == "[-] 'devtracker report' was entered.  You must run 'devtracker start' to create project tracking file.\n"

def test_full_report(capsys):
    next_line = ['1999-01-01', '00:00:00', '1999-01-01', '00:00:00', '00:00:00']
    following_line = ['1999-01-02', '00:00:01', '1999-01-02', '00:00:02', '00:00:01']

    with open(path, 'r', newline='') as myFile:
        reader = list(csv.reader(myFile))
        reader.pop()
        reader.pop()
        with open(path, 'w', newline='') as myfile:
            wr = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            for i in reader:
                wr.writerow(i)
            wr.writerow(next_line)
            wr.writerow(following_line)

    full_report("test")
    captured = capsys.readouterr()
    assert captured.out == """[+] Generating Full Report
-------------------------------------------------------------------------
start_date       | start_time | end_date         | end_time | total    | 
-------------------------------------------------------------------------
January  1, 1999 | 12:00 AM   | January  1, 1999 | 12:00 AM | 00:00:00 | 
-------------------------------------------------------------------------
January  2, 1999 | 12:00 AM   | January  2, 1999 | 12:00 AM | 00:00:01 | 


[+] You have worked on test for a total of 0:00:01.  Way to go!
"""


def test_remove():
    os.remove(path)


