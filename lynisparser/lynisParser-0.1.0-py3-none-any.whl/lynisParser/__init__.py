class LynisParser:
    def __init__(self):
        pass

    def openFile(self, inputFileName):
        fileObj = open(inputFileName, 'r')
        fileData = fileObj.readlines()
        fileData = str(fileData).split("================================================================================")
        return fileData

    def stripTrash(self, inputText):
        inputText = inputText.replace("',", "")
        inputText = inputText.replace(" '", "")
        inputText = inputText.replace("#", "")
        inputText = inputText.replace("[]", "")
        inputText = inputText.replace("- ", "")
        inputText = inputText.replace("  ", "")
        return inputText

    def processKeyDataFromLynis(self, inputKeyData):
        issueData = ",;".join(inputKeyData).replace("'","").replace("! ", "* ").split("* ")
        issueData = [entry for entry in issueData if len(issueData) > 1]
        issueList = []
        for entry in issueData:
            entry = entry.replace('",',"").replace('"',"").replace("https:", "URL : https:")
            if "Follow-up:" in entry:
                entry = entry.split('Follow-up:')[0]
            entrySplit = entry.split(',;')
            entrySplit = [entry for entry in entrySplit if len(entry) > 0]
            entryDict = {}
            entryKey = entrySplit[0]
            if entryKey == '----------------------------':
                continue
            entryDict[entryKey] = {}
            for entry in entrySplit:
                entrySplitData = entry.split(" : ")
                if len(entrySplitData) == 2:
                    entryDict[entryKey][entrySplitData[0]] = entrySplitData[1]
            issueList.append(entryDict)
        return issueList

    def splitDataFromLynis(self, inputCleanText):
        keyNames = []
        keyData = []
        for key in str(inputCleanText).split('):'):
            keySplit = key.split("', '")
            keyName = keySplit[-1].split(" ")[0]
            if 'Use' not in keyName:
                keyNames.append(keyName)
            keyDataSet = []
            for entry in keySplit:
                if entry not in keyName:
                    keyDataSet.append(entry)
            keyDataSetDict = self.processKeyDataFromLynis(keyDataSet)
            if len(keyDataSetDict) > 0:
                keyData.append(keyDataSetDict)
        return [keyNames, keyData]

    def assembleResultsFromLynis(self, inputKeyNames, inputKeyData):
        resultsDict = {}
        keyIndex = 0
        for keyName in inputKeyNames:
            resultsDict[keyName] = inputKeyData[keyIndex]
            keyIndex = keyIndex + 1
        return resultsDict

    def parseReport(self, reportFileName):
        fileData = self.openFile(reportFileName)
        dataIssues = [entry for entry in self.stripTrash(fileData[1]).split("\\n") if len(entry) > 5]
        dataSummary = [entry for entry in self.stripTrash(fileData[2]).split("\\n") if len(entry) > 5]
        issuesKeyNames, issuesKeyData = self.splitDataFromLynis(dataIssues)
        issueResults = self.assembleResultsFromLynis(issuesKeyNames, issuesKeyData)
        return issueResults
