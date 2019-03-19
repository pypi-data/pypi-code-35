from __future__ import print_function

from sklearn import metrics
from imutils import paths
from frimcla import prediction

import json


#Este archivo se usa para calcular los accuracies de los modelos con los conjuntos de test. Asi calculamos realmente
# el % de acierto que tiene cada uno de los modelos y si realmente funciona como se ha marcado en el entrenamiento.


# from frimcla.shallowmodels import classificationModelFactory, modelFactory
# print(classificationModelFactory.ListClassificationModels())
# print(modelFactory.listFeatureExtractors())

outputPath = "/home/magarcd/Escritorio/output/BORRRA2222222222222222"
datasetPath= "/Mias"
featureExtractors = []
datasetName = datasetPath[datasetPath.rfind("/")+1:]
print(outputPath + "/" + datasetName +'/ConfModel.json')

imagePaths = "/home/magarcd/Escritorio/dataset/MiasRecortadasTEST"

with open(outputPath + "/" + datasetName +'/ConfModel.json') as data:
    datos = json.load(data)

# prediction.prediction(["inception","False"], "MLP", imagePaths, outputPath, datasetName)

extractors = datos["featureExtractors"]
classifiers = ["GradientBoost","RandomForest", "SVM","KNN","LogisticRegression", "MLP"]

for ex in extractors:
    featureExtractor = [str(ex["model"]), ex["params"]]
    featureExtractors.append(featureExtractor)

del extractors
# Poner la ruta de las imagenes para que luego el método se encargue de listar las imagenes de la carpeta y se puedan tratar
prediction.predictionEnsemble(featureExtractors, classifiers, imagePaths, outputPath, datasetName)

auxPath = outputPath + "/" + datasetName
filePrediction = auxPath +"/predictionResults.csv"
predictions = []
groundTruth = []

csvfile = open(filePrediction, "rb")
csvfile.readline()
for line in csvfile:
    line = line.split(",")
    realclass = line[0].split("/")[-2]
    if(realclass =="Uninfected"):
        groundTruth.append(1)
    else:
        groundTruth.append(0)
    # line = line.split("\n")[0]
    predictions.append(int(line[1]))

#
# groundTruthFile = "/home/magarcd/Escritorio/frimcla/mias.csv"
# groundTruth = []
# csvfile2 = open(groundTruthFile, "r")
# for line in csvfile2:
#     line = line.split(",")
#     for image in imagePaths:
#         image =image[image.rfind("/")+1:]
#         if (image.split(".")[0]==line[0]):
#             if (line[2]=="NORM\r\n"):
#                 groundTruth.append(1)
#             else:
#                 groundTruth.append(0)
#
# # print(groundTruth)
# # groundTruthFile = "/home/magarcd/Escritorio/frimcla/mias.csv"
# # groundTruth = []
# # csvfile2 = open(groundTruthFile, "r")
# # for line in csvfile2:
# #     line = line.split(",")
# #     groundTruth.append(int(float(line[1])))
#
#
print("Ground Truth")
print (groundTruth)
print("Predictions")
print(predictions)
f = open(auxPath + "/TESTaccuracy.txt","w")
# f.write("Ground Truth\n")
# f.write(groundTruth)
# f.write("\nPredictions\n")
# f.write(predictions)
f.write("Auroc\n")
f.write(str(metrics.roc_auc_score(groundTruth, predictions)))
f.write("\nAccuracy\n")
f.write(str(metrics.accuracy_score(groundTruth,predictions)))


print(metrics.roc_auc_score(groundTruth, predictions))
print(metrics.accuracy_score(groundTruth,predictions))


#
#
#
# outputPath = "../output"
# datasetName= "/dataAugmentation"
#
# auxPath = outputPath + datasetName
# filePrediction = auxPath +"/predictionResults.csv"
# predictions = []
# csvfile = open(filePrediction, "r")
# csvfile.readline()
# for line in csvfile:
#     line = line.split(",")
#     predictions.append(int(line[1]))
#
#
#
#
# groundTruthFile = "../test_GroundTruth.csv"
# groundTruth = []
# csvfile2 = open(groundTruthFile, "r")
# csvfile2.readline()
# for line in csvfile2:
#     line = line.split(",")
#     groundTruth.append(int(float(line[1])))
#
# print("Ground Truth")
# print (groundTruth)
# print("Predictions")
# print(predictions)
#
# print(metrics.roc_auc_score(groundTruth, predictions))
# print(metrics.accuracy_score(groundTruth,predictions))