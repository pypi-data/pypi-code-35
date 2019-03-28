"""
Some tools to work with databases
"""
from navipy.database import DataBase


def copy(filename_in, filename_out):
    """ Copy database until in crashed or finish

    :param filename_in: Path to the input database
    :param filename_out: Path to the output database
    """
    dbin = DataBase(filename_in, mode='r')
    dbout = DataBase(filename_out, mode='a')
    for i, posorient in dbin.get_posorients().iterrows():
        print(posorient)
        try:
            image = dbin.read_image(posorient)
        except ValueError:
            break
        dbout.write_image(posorient, image)
