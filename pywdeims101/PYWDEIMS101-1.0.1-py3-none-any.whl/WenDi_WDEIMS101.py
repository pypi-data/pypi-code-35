import zipfile
import csv
import xml.dom.minidom 
import uuid
import os

class CompressionHelper:
    @staticmethod
    def CompressFile(sourceFileNameList, zipFileName):
        '''
        压缩文件。该函数使用内置模块zipfile进行简单包装实现。
        '''
        zip = zipfile.ZipFile(zipFileName, "w")

        for sourceFileName in sourceFileNameList:
            zip.write(sourceFileName)
        
        zip.close()

    @staticmethod
    def DecompressFile(zipFileName, targetDir):
        '''
        解压缩文件。该函数使用内置模块zipfile进行简单包装实现。
        '''
        zip = zipfile.ZipFile(zipFileName, "r")
        
        lst_FileName = zip.namelist()
        for fileName in lst_FileName:
            handle = open(targetDir + fileName, "wb")
            handle.write(zip.read(fileName))
            handle.close()
        
        zip.close()

class CSVTXTFileUtility:
    @staticmethod
    def BuildTextFile(outputFileName, lst_Data, blnIncludeHeadLine = False, strXmlHeadDefinition = ""):
        csvFile = open(outputFileName, "w", newline="", encoding = "utf-8-sig")
        writer = csv.writer(csvFile)

        #如果需要标题行，则根据strHeadDefinition参数写入
        lst_HeadFieldInfo = [] #该变量尚未启用
        if blnIncludeHeadLine:
            lst_HeadDesc = []
            
            domTree = xml.dom.minidom.parseString(strXmlHeadDefinition)
            el = domTree.documentElement
            rows = el.getElementsByTagName("RS_ROW")
            for row in rows:
                fieldDesc = row.getAttribute("FIELD_DESC")
                lst_HeadDesc.append(fieldDesc)

                fieldCode = row.getAttribute("FIELD_CODE")
                dataType = row.getAttribute("DATA_TYPE")
                dict_FieldInfo = {
                    "field_code": fieldCode, 
                    "data_type": dataType
                }
                lst_HeadFieldInfo.append(dict_FieldInfo)

            writer.writerow(lst_HeadDesc)
        
        #写入数据到CSV文件中
        writer.writerows(lst_Data)

        csvFile.close()
    
    @staticmethod
    def BuildTextFileViaBatch(zipFileName, lst_Data, maxLineOfBatch, strFileTypeOfBatch = "csv", blnIncludeHeadLine = False, strXmlHeadDefinition = ""):
        ttlLine = len(lst_Data)
        batchNum = 0
        if ttlLine % maxLineOfBatch == 0:
            batchNum = ttlLine // maxLineOfBatch
        else:
            batchNum = ttlLine // maxLineOfBatch + 1

        i = 1
        lst_TxtFileName = []
        while i <= batchNum:
            beginIndex = (i-1)*maxLineOfBatch
            endIndex = maxLineOfBatch*i
            batchData = lst_Data[beginIndex:endIndex]

            uuid = Application.CreateNewUUID()
            strTxtFileName = "%s.%s" % (uuid, strFileTypeOfBatch)
            CSVTXTFileUtility.BuildTextFile(strTxtFileName, batchData, blnIncludeHeadLine, strXmlHeadDefinition)
            lst_TxtFileName.append(strTxtFileName)

            i += 1
        
        CompressionHelper.CompressFile(lst_TxtFileName, zipFileName)

        for fileName in lst_TxtFileName:
            os.remove(fileName)

class Application:
    @staticmethod
    def CreateNewUUID():
        return uuid.uuid4()
    


