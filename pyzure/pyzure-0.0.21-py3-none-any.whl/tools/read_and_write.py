def write_in_file(f, content):
    f = open(f + ".txt", "w")
    f.write(content)
    f.close()


def read_file(f):
    f = open(f + ".txt","r")
    return f.read()
