from datetime import datetime

def get_date():
    return str(datetime.now().strftime("%Y-%m-%d"))

def get_time():
    return str(datetime.now().strftime("%H:%M:%S"))

def total_time(start, end):
    FMT = "%H:%M:%S"
    tdelta = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
    return tdelta

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

