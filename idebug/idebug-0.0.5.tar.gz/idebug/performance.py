
from idebug import *
from ilib import inumber


class LoopReporter:

    def __init__(self, title, len):
        self.title = title
        self.start_dt = datetime.now()
        self.count = 1
        self.len = len

    def report(self, addi_info='...'):
        if self.count <= self.len:
            cum_runtime = (datetime.now() - self.start_dt).total_seconds()
            avg_runtime = cum_runtime / self.count
            expected_total_runtime = avg_runtime * self.len
            expected_remaining_runtime = avg_runtime * (self.len - self.count)

            tpls = [
                ('평균실행시간', avg_runtime),
                ("누적실행시간", cum_runtime),
                ('전체실행시간', expected_total_runtime),
                ('잔여실행시간', expected_remaining_runtime)
            ]
            title = f"{self.title} --> {addi_info}"
            print(f"\n{'*'*60}\n {__class__.__name__} : {title}\n 반복횟수현황 : {self.count}/{self.len}")
            for tpl in tpls:
                print_converted_timeunit(title=tpl[0], seconds=tpl[1])
            self.count += 1

def print_converted_timeunit(title, seconds):
    """새줄 띄어쓰기 하지말것"""
    timeexp, unit = inumber.convert_timeunit(seconds)
    print(f" {title} : {timeexp}")

class RuntimeLogger:

    def __init__(self, currentframe):
        self.start_dt = datetime.now().astimezone()
        self.frameinfo = inspect.getframeinfo(currentframe)
        print(f"\n frameinfo :\n\n {self.frameinfo}")

    def report(self):
        title = self.frameinfo.function
        seconds = (datetime.now().astimezone() - self.start_dt).total_seconds()
        print_converted_timeunit(title, seconds)
