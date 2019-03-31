import sys

if len(sys.argv) > 1:
    eval(sys.argv[1])

class Translator:
    
    def __init__(self, oriented=False, templates=False, template=''):
        self.templates = templates
        self.oriented = oriented
        self.template = template
    
    def command_line(self, inpul='', command='', python='', splitter=' '):
        command = str(command)
        pythonr = {}
        if self.templates is True:
            code = input('=>')
            with open(self.template) as temp:
                for line in temp.readlines():
                    try:
                        eval(line)
                    except SyntaxError:
                        try:
                            exec(line)
                        except:
                            print('error in file "' + temp.name + '"\n    line "' + line + '"')
        
        else:
            inpu = inpul.split(splitter)
            code = command.split()
            python = str(python)
            for word in code:
                if '<' in word and '>' in word:
                    python = python.replace(word, inpu[code.index(word)])
            try:
                eval(python)
            except:
                try:
                    exec(python)
                except:
                    print("invalid command '{0}'".format(python))
    def __str__(self):
        return 'compilere/pycompile/java'




def compile(code, crc_list, python_list):
    for crc, python in zip(crc_list, python_list):
        code = str(code).replace(crc, python)
    eval(code)