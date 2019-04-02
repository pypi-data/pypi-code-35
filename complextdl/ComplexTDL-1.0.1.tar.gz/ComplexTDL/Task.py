#! /Users/xiaotian/anaconda3/bin/python3.6
#coding=utf-8

import tinydb as td
from datetime import datetime, timedelta
import sys
import re
import pyperclip
import os.path as ospath
import json
from ComplexTDL import sysXXt
from ComplexTDL.CurrentPath import *

## init tinydb

db = td.TinyDB(BASEPATH + 'db.json')
taskDB = db.table('task')
relationshipDB = db.table('relationship')
logDB = db.table('log')

## read the job information

with open(BASEPATH + "WorkType.txt") as f:
    exec(f.read())

'''
the structure of task

no Number
mo Module / Group / List
ti Title
de Description and Update
st Start time
en End time or Check time
ra Completion rate, -1 for pause
pa Parent task number
pe person in charge
pr priority
'''

'''
the structure of relationship

pa Parent
ch children
'''

'''
the structure of log

ti time
no Task number
'''

# apply a new task number
def NewNumber():

    t = 0
    with open(BASEPATH + 'number.txt', 'r') as f:
        n = f.read()
        t = str(int(n) + 1)
    
    with open(BASEPATH + 'number.txt', 'w') as f:
        f.write(t)
    
    return t


# delete a task and its subtasks
def DeleteRecord(formData):

    q = td.Query()

    # Delete the subtasks
    i = 0
    children = relationshipDB.search(q.pa == formData['no'])
    while i < len(children):

        child = children[i]
        i += 1
        
        childNumber = child['ch']
        grandchildren = relationshipDB.search(q.pa == childNumber)
        if grandchildren == []: # no subtask for the subtask, delete the subtask directly
            taskDB.remove(q.no == childNumber)
            relationshipDB.remove(q.ch == childNumber)

        else: # add the subtasks of the subtask to the list
            i -= 1
            for g in grandchildren:
                children.insert(i, g)
    
    # Delete the task
    if taskDB.remove(q.no == formData['no']) == []:
        return 'None'

    # Delete the relationship
    relationshipDB.remove(q.ch == formData['no'])

    return formData['no']


# update a task or insert a new task
def UpdateData(formDataF):

    formData = formDataF.copy()
    q = td.Query()
    today = '=== ' + datetime.strftime(datetime.today(), '%Y-%m-%d') + ' ===\n'

    # doing some convertion before insert

    if formData['pa'] != None and formData['pa'] != '': # keep the module of the task the same of its parent
        try:
            parent = taskDB.search(q.no == formData['pa'])[0]
            formData['mo'] = parent['mo']
        except:
            print('Parent number %s not found'%formData['pa'])

    if formData['de']: # convert the \\ to \n
        formData['de'] = formData['de'].replace('\\', '\n')
    
    if formData['ra'] == 100 and formData['de'] == '': # if the task is done, add "Done" to the description
        formData['de'] = 'Done.\n\n' + formData['de']

    # prepare to insert

    if formData['no'] == '': # new task
 
        formData['no'] = NewNumber()
        if formData['de'] != '': formData['de'] = today + formData['de']
        taskDB.insert(formData)

    else: # edit the task

        number = formData['no']
        taskF = taskDB.search(q.no == number)
        if taskF == []:
            print('Task number %s not found'%number)
        else:
            taskF = taskF[0]

            # if there is no changes happening, doing nothing

            same = True
            for k in formData.keys():

                if formData[k] == None: # Keep same if the field is "None"

                    if k in taskF.keys(): formData[k] = taskF[k]

                elif k == 'de' and len(formData[k]) > 0:

                    if formData[k][0] == '+': # update the describtion
                        if taskF['de'] != '': formData[k] = today + formData[k][1:] + '\n\n' + taskF['de']
                        else:
                            formData[k] = today + formData[k][1:]
                    else:
                        formData[k] = today + formData[k]

                    if formData[k] != taskF[k]: same = False

                elif not k in taskF or formData[k] != taskF[k]: # new field or field content different
                    same = False

            if same == True: return formData['no'] + 'x'

            taskDB.update(formData, q.no == number)

            # update the subtask
            children = relationshipDB.search(q.pa == number)
            if children != []:

                commonInfo = {}
                if formDataF['mo'] != None: commonInfo['mo'] = formDataF['mo']
                if formDataF['pr'] != None: commonInfo['pr'] = formDataF['pr']
                if formDataF['ra'] == 100: commonInfo['ra'] = 100
                
                if commonInfo != {}:
                    while len(children) != 0:
                        childNo = children[0]['ch']
                        taskDB.update(commonInfo, q.no == childNo)
                        children.extend(relationshipDB.search(q.pa == childNo))
                        children.remove(children[0])

        # update the parent
        relationshipDB.remove(q.ch == number)
        if formData['pa'] != None: relationshipDB.insert({'pa': formData['pa'], 'ch': formData['no']})

    # update the log
    if (formDataF['de'] != '' and formDataF['de'] != None and formDataF['no'] != '') or (formDataF['ra'] != None and formDataF['ra'] != 0):
        logDB.insert({'no': formData['no'], 'ti': datetime.strftime(datetime.today(), '%Y-%m-%d'), 'me': 'u'})
    else:
        logDB.insert({'no': formData['no'], 'ti': datetime.strftime(datetime.today(), '%Y-%m-%d'), 'me': 'n'})
    return formData['no']