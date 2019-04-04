def check_read(line,string,value=None):
    line = line.strip().split(':',1)
    assert len(line) == 2
    assert line[0] == string
    if value is not None:
        assert line[1] == value, '{} {} / {} {}'.format(line[1], type(line[1]), value, type(value))
    return line[1]