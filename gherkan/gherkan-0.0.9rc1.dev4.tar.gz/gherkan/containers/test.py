import yaml
import re

with open('templates_dic.yaml','r') as stream:
    try:
        temp_dic = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

#robotXProgram = re.compile(r"(?=.*OR)(?=.*AND)(?=.*robot(?P<robotName>\w+)programnumber)", re.IGNORECASE)#(?=(?P<robotName>\w+)programnumber)\\1+(programended)
#match = robotXProgram.search("AND(OR(robotN3ProgramNumber,robotN4ProgramNumber),programended)")  # parse the string using the regex
#print(match)
#print("Robot name was '{}'".format(match.group("robotName")))


stringToEval = "HalloOnBox"
for index, tmplD in temp_dic.items():
    print(tmplD["TempStr"][0])
    strAll = ''.join(tmplD["TempStr"])
    print(strAll)
    expToMatch = re.compile(r""+tmplD["TempStr"][0], re.IGNORECASE)
    #expToMatch = re.compile(r""+"(?P<subject>\\w+)On(?P<object>\\w+)", re.IGNORECASE)
    match = expToMatch.search(stringToEval)
    if match:
        print(match[0])
        print(match.group)
        print("Robot name was '{}'".format(match.group("subject")))
# dic = {1:{"brand":"ford","type":"mustang","year":"2018"},2:{"brand":"ford1","type":"mustang1","year":"20181"}}
# for index, d in dic.items():
#     print(d["brand"])
#     if "brand" in d.keys():
#         print("hallo maus")
