from Popdata.Generator import Generator
from Popdata.Analyze import Analyze


class main:

    def __init__(self, file, target):
        ana = Analyze(file, target)
        self.df = ana.read_data()
        self.col_dict, self.row_num = ana.describe_data(self.df)

    def popdata(self, mode, size=None, col_dict=None):
        gen = Generator(mode, size, col_dict)
        new_df = gen.generate(self.row_num, self.col_dict)
        new_df = gen.change_type(new_df, self.col_dict)
        return new_df
