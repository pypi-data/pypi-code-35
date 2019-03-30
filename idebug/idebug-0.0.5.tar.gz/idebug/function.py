
from idebug import *
from ilib import inumber
import re


class FuncReporter:

    def __init__(self, currentframe):
        self.start_dt = datetime.now().astimezone()
        self.currentframe = currentframe
        #dbg.currentframe(currentframe)
        self.inputs = currentframe.f_locals

        frameinfo = inspect.getframeinfo(frame=currentframe)
        #dbg.getframeinfo(frameinfo)
        self.filename = frameinfo.filename
        self.funcname = frameinfo.function

        argvalues = inspect.getargvalues(frame=currentframe)
        #dbg.getargvalues(argvalues)
        self.inputs = argvalues.locals
        #dbg.obj(self)

    def report_init(self):
        """함수가 시작되었음을 알리는 구분선과 입력변수를 프린트."""
        light_inputs = self.invisible_inputs_byReg(self.inputs)
        print(f"\n{'*'*60}\n {__class__.__name__} : {inspect.stack()[0][3]}")
        pp.pprint({
            'modulename': self.filename,
            'funcname':self.funcname,
            'light_inputs':light_inputs})
        return self

    def report_fin(self, RunTimeout=60):
        """함수실행시간 체크, 함수실행시간에 영향을 미치는 입력 파라미터는 무엇인지 나중에 조사."""
        self.end_dt = datetime.now().astimezone()
        self.runtime = (datetime.now().astimezone() - self.start_dt).total_seconds()

        t, unit = inumber.convert_timeunit(self.runtime)
        print(f"\n{'*'*60}\n {__class__.__name__} : {inspect.stack()[0][3]}")
        pp.pprint({
            'modulename': self.filename,
            'funcname': self.funcname,
            'start_dt': self.start_dt,
            'end_dt': self.end_dt,
            'runtime':t })

    def invisible_inputs_byReg(self, inputs, regs=[]):
        """input_param_중에_list를_포함한_query는_프린트하지않는다"""
        regs = regs if len(regs) is not 0 else ['^query', 'df|df\d+', '.+li', '^r$', '^whoami', '^soup', '^js']
        light_inputs = inputs.copy()
        for reg in regs:
            #print(f"\n{'-'*60}\n invisible_inputs_byReg | regex : {reg}")
            p = re.compile(pattern=reg)
            for key, val in inputs.items():
                if p.search(string=key) is not None:
                    del(light_inputs[key])
        #dbg.dic(light_inputs, 'light_inputs')
        return light_inputs
