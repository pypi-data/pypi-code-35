# MIT License
#
# Copyright (c) 2019 Anderson Vitor Bento
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import csv
from os import walk, path, remove
from tempfile import NamedTemporaryFile
import shutil

class CSVbase():

    def __init__(self, Path = '.'):
        self.path = Path + '/'
        if not path.exists(self.path):
            print('\x1b[41m\x1b[37m', 'Database root folder not exists! Please create a folder named "' + Path + '"', '\x1b[0m')
            return None
        print('\x1b[42m\x1b[37m', 'Database initialized with success!', '\x1b[0m')
        return None

    def getPath(self):
        return self.path

    def checkFile(self, table_name = ''):
        return path.exists(self.path + table_name + '.csv')
    
    def createTable(self, table_name, fields):
        with open(self.path + table_name + '.csv', mode='w+') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(fields)
    
    def dropTable(self,table_name):
        try:
            remove(self.path + table_name + '.csv')
            return 'Table removed with success!'
        except:
            return 'Table not removed!'

    def create(self, table_name, data):
        
        if not self.checkFile(table_name): return 'table not exists'
        
        fields = self.findFields(table_name)['fields']
        with open(self.path + table_name + '.csv', mode='a+') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            row = {}
            for i in fields:
                try:
                    row = {**row, i: data[i]}
                except:
                    pass
            writer.writerow(row)
        return 'created with success!'
        
    def read(self, table_name, conditions = None):
        
        if not self.checkFile(table_name): return 'table not exists'

        conds_type = []
        conds_value = []
        if conditions:
            for i in conditions:
                conds_type.append(i)
                conds_value.append(conditions[i])

        output = []
        with open(self.path + table_name  + '.csv', mode='r') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                x = True
                for i in range(len(conds_type)):
                    try:
                        x = x and row[conds_type[i]] == conds_value[i]
                    except:
                        pass
                if x:
                    output.append(row)
            return output

    def update(self, table_name, conditions, newElements):
        
        if not self.checkFile(table_name): return 'table not exists'

        conds_type = []
        conds_value = []
        if conditions:
            for i in conditions:
                conds_type.append(i)
                conds_value.append(conditions[i])
        
        newFile = NamedTemporaryFile(mode='w', delete=False)

        Fields = self.findFields(table_name)
        fields = Fields['fields']
        fieldsDict = Fields['fieldsDict']
        updatedStatus = 'row not found!'
        with open(self.path + table_name + '.csv', 'r', newline='') as oldFile, newFile:
            reader = csv.DictReader(oldFile)
            writer = csv.DictWriter(newFile, fieldnames=fields)
            writer.writerow(fieldsDict)
            for row in reader:
                x = True
                for i in range(len(conds_type)):
                    try:
                        x = x and row[conds_type[i]] == conds_value[i]
                    except:
                        pass
                if x:
                    copy = {**newElements}
                    for i in copy:
                        try:
                            if(fieldsDict[i]):
                                pass                                
                        except:
                            del newElements[i]
                    row = { **row, **newElements }
                    updatedStatus = 'updated with success!'
                writer.writerow(row)

        shutil.move(newFile.name, self.path + table_name + '.csv')
        return updatedStatus

    def delete(self, table_name, conditions):
        
        if not self.checkFile(table_name): return 'table not exists'

        conds_type = []
        conds_value = []
        if conditions:
            for i in conditions:
                conds_type.append(i)
                conds_value.append(conditions[i])
        
        newFile = NamedTemporaryFile(mode='w', delete=False)

        Fields = self.findFields(table_name)
        fields = Fields['fields']
        fieldsDict = Fields['fieldsDict']

        with open(self.path + table_name + '.csv', 'r', newline='') as oldFile, newFile:
            reader = csv.DictReader(oldFile)
            writer = csv.DictWriter(newFile, fieldnames=fields)
            writer.writerow(fieldsDict)
            for row in reader:
                x = True
                for i in range(len(conds_type)):
                    try:
                        x = x and row[conds_type[i]] == conds_value[i]
                    except:
                        pass
                if not x:
                    writer.writerow(row)
                

        shutil.move(newFile.name, self.path + table_name + '.csv')
        return 'removed with success!'

    def listTables(self,p = '', extension = True):
        foo = []
        for (dirpath, dirnames, filenames) in walk("./" + self.path + p):
            if (not extension):
                for i in range(len(filenames)):
                    filenames[i] = filenames[i].split(".csv")[0]
            foo.extend(filenames)
            break
        return foo	

    def findFields(self, table_name):
        fields = []
        fieldsDict = {}

        with open(self.path + table_name + '.csv', mode='r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                for field in row:
                    fields.append(field)
                    fieldsDict = {
                        **fieldsDict,
                        field: field
                    }
                break
        
        return { 'fields': fields, 'fieldsDict': fieldsDict }
