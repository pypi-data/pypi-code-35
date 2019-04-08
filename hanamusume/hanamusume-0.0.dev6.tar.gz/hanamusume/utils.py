import math
import random
import os

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

def generate_cv(filename, output_folder, n_fold=5, seed=None):
    random.seed(seed)
    orig_filename = filename
    filename = filename[filename.rfind('/')+1:]
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    train_f_list = []
    test_f_list = []
    train_fn_list = []
    test_fn_list = []
    for fold in range(n_fold):
        train_fn = '{}/{}.{}.tr'.format(output_folder, filename, fold) 
        test_fn = '{}/{}.{}.ts'.format(output_folder, filename, fold)
        train_fn_list.append(train_fn)
        test_fn_list.append(test_fn)
        train_f_list.append(open(train_fn,'w'))
        test_f_list.append(open(test_fn,'w'))
    
    with open(orig_filename) as f:
        for line in f.readlines():
            ind = random.randint(0,n_fold-1)
            for i in range(n_fold):
                if i == ind:
                    test_f_list[i].write(line)
                else:
                    train_f_list[i].write(line)
    for f in train_f_list:
        f.close()
    for f in test_f_list:
        f.close()

    return train_fn_list, test_fn_list
