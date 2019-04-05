import math

def check_read(line,string,value=None):
    line = line.strip().split(':',1)
    assert len(line) == 2
    assert line[0] == string
    if value is not None:
        assert line[1] == value, '{} {} / {} {}'.format(line[1], type(line[1]), value, type(value))
    return line[1]

def log_loss(probs, labels):
    assert len(probs) == len(labels)
    total_logloss = 0.
    for p,y in zip(probs, labels):
        total_logloss -= y * math.log(p) + (1.-y) * math.log(1.-p)
    return total_logloss/len(probs)