def ex_add():
    return 1+2


def package_data_show():
    file = open('data.txt').readlines()
    for line in file:
        print(line)
