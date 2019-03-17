import os


def read_file_lines(filename):
    lines = None
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as reader:
                lines = reader.readlines()
        finally:
            reader.close()
    return lines



def read_file_line(filename, func):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as reader:
                for line in reader:
                    func(line)
        finally:
            reader.close()


def read_file(filename):
    file = None
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as reader:
                file = reader.read()
        finally:
            reader.close()
    return file


def write_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as w:
        w.write(data)


def write_file_feed(self, filename, data):
    with open(filename, 'w', encoding='utf-8') as w:
        w.write(data)
        w.write('\n')


def remove(filename):
    if os.path.exists(filename):
        os.remove(filename)

def empty(filename):
    write_file(filename, '')