# output the confusion matrix; store the confusion matrix
import os
import json
from collections import Counter
import time
import numpy as np
import csv
import copy
#all_relations=set(["Comparison","Contingency","Temporal", "Expansion"])

ave_num = 0
ave = 0

def evaluation_old(predicted, instances, relation): #need to make some changes for four way classification
    TP, TN, FP, FN = [], [], [], []
    #print "num of instances in predicted: %d" % len(predicted)
    #print "num of instances in gold: %d" % len(instances)
    predicted_tmp = copy.deepcopy(predicted)
    instances_tmp = copy.deepcopy(instances)
    '''
    for i in range(len(predicted_tmp)):
        if predicted_tmp[i] == relation:
            predicted_tmp[i] = relation
        else:
            predicted_tmp[i] = "none-" + relation
        for j in range(len(instances_tmp[i]["clf_label"])):
            if(relation in instances_tmp[i]["clf_label"][j]):
                instances_tmp[i]["clf_label"][j] = relation
            else:
                instances_tmp[i]["clf_label"][j] = "none-" + relation
    '''
    for i in range(len(predicted_tmp)):
        if predicted_tmp[i]==relation:
            if predicted_tmp[i] in instances_tmp[i]["clf_label"]:
                TP.append(str(instances_tmp[i]["fileName"])+"-"+str(instances_tmp[i]["location"]))
            else:
                FP.append(str(instances_tmp[i]["fileName"])+"-"+str(instances_tmp[i]["location"]))
        elif predicted_tmp[i] !=relation:
            if relation not in instances_tmp[i]["clf_label"] or len(instances_tmp[i]["clf_label"])>1:
            #if (all_relations-set([relation])).intersection(set(instances[i]["clf_label"])):
                TN.append(str(instances_tmp[i]["fileName"])+"-"+str(instances_tmp[i]["location"]))
            else:
                FN.append(str(instances_tmp[i]["fileName"])+"-"+str(instances_tmp[i]["location"]))
    print "TP: %d, TN: %d, FP: %d, FN: %d" % (len(TP), len(TN), len(FP), len(FN))
    P=float(len(TP))/(len(TP)+len(FP))
    R=float(len(TP))/(len(TP)+len(FN))
    F=2.0*P*R/(P+R)

    global ave, ave_num
    ave_num = ave_num + 1
    ave = ave + F
    ave_tmp = float(ave)/ave_num
    print "average:", ave_tmp
    #all_label_list=[]
    #for ins in instances:
    #    all_label_list+=ins["clf_label"]
    with open("./log/results_trace_back--"+ relation, "w") as f:
        f.write(" ".join(TP) + "\n" + " ".join(TN) + "\n" + " ".join(FP) + "\n" + " ".join(FN))
    with open("./log/Prediction--"+relation, "w") as f:
        f.write(" ".join(predicted))
    print "statistics in all labels:"
    #print Counter(all_label_list)
    print "label:", relation
    print "TP: %d, TN: %d, FP: %d, FN: %d" % (len(TP), len(TN), len(FP), len(FN))
    print "P: %f, R: %f, F: %f" % (P, R, F)
    print "\n"
    return F

def showConfusionMatrix(confusionMatrixDict):
    #first print the parameters
    #then print the confusion matrix
    allLabels = []
    for key in confusionMatrixDict["Matrix"].keys():
        subKeys = key.split("+")
        for subkey in subKeys:
            if(subkey not in allLabels):
                allLabels.append(subkey)
    #config output format a = {0:8d} {1:8d} {2:8d} ......
    a = []
    for i in range(len(allLabels)):
        a.append("{" + str(i) + ":8d} ")
    a = "".join(a)

    allData = []
    for onePrediction in allLabels:
        list_tmp = []
        for oneLabel in allLabels:
            key = onePrediction + "+" + oneLabel
            try:
                list_tmp.append(len(confusionMatrixDict["Matrix"][key]))#number
            except KeyError:
                list_tmp.append(0)
        allData.append(list_tmp)
    allData = np.array(allData)
    print confusionMatrixDict["parameters"]
    print "keys: ", confusionMatrixDict["Matrix"].keys()
    row_format ="{:>35}" * (len(allLabels) + 1)
    print row_format.format("", *allLabels)
    for team, row in zip(allLabels, allData):
        print row_format.format(team, *row)

def createAndSaveConfusionMatrix(predicted, instances, parameters, savePath):
    confusionMatrixDict = {"Matrix":{},"parameters":{}}
    #path_json_out = "/Users/xiangyuanxin/PycharmProjects/imBaselineAttr/imTestCorenlp.Bas.fourway"
    for i in range(len(predicted)):
        #instances[i]["Predictionfourway"] = predicted[i]

        labelList = instances[i]["clf_label"]
        match = 0
        for j in range(len(labelList)):
            if(predicted[i] == labelList[j]):
                key = predicted[i] + "+" + labelList[j]
                if(key in confusionMatrixDict["Matrix"]):
                    confusionMatrixDict["Matrix"][key].append(i)
                else:
                    confusionMatrixDict["Matrix"][key] = []
                    confusionMatrixDict["Matrix"][key].append(i)
                match = 1
                break
        if(match == 0):
            key = predicted[i] + "+" + labelList[0]
            if(key in confusionMatrixDict["Matrix"]):
                confusionMatrixDict["Matrix"][key].append(i)
            else:
                confusionMatrixDict["Matrix"][key] = []
                confusionMatrixDict["Matrix"][key].append(i)

    #with open(path_json_out, "w") as f:
    #    json.dump(instances, f, encoding="latin1")


    confusionMatrixDict["parameters"] = parameters
    timeStr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    #save confusionMatrix as file
    file = savePath + "_" + "confusionMatrix_" + timeStr
    with open(file, "w") as f:
        json.dump(confusionMatrixDict, f, encoding="latin1")
    #save confusionMatrix as .csv file
    writeMatrixPath = savePath + "_" + "confusionMatrix" + "_" + timeStr + ".csv"
    writeMatrix = open(writeMatrixPath, "w+")
    wm = csv.writer(writeMatrix)

    allLabels = []
    for key in confusionMatrixDict["Matrix"].keys():
        subKeys = key.split("+")
        for subkey in subKeys:
            if(subkey not in allLabels):
                allLabels.append(subkey)
    allLabels.sort()
    print allLabels
    #write csv head line
    allLabels.insert(0,"")
    wm.writerow(allLabels)
    del allLabels[0]#delete emputy cell

    for predictkey in allLabels:
        list_tmp2 = []
        list_tmp2.append(predictkey)
        for labelksy in allLabels:
            key = predictkey + "+" + labelksy
            list_tmp2.append(len(confusionMatrixDict["Matrix"][key]))
        wm.writerow(list_tmp2)
    showConfusionMatrix(confusionMatrixDict)



def getLevel2(ss): # get the level 2 relation. If it is not exist, return the level 1 relation
    if len(ss.split("."))==3:
        return ss.split(".")[0]+"."+ss.split(".")[1]
    else:
        return ss

def multiClassEvaluation(predicted, instances):
    No_corr=0
#    print "=======in the evaluation script========="
#    print "predicted:"
#    print Counter(predicted)
#    print "in the real data:"
#    label_dis = []
#    for ins in instances:
#        for label in ins["LabelList"]:
            # print label
#            label_dis.append(getLevel2(label))
#    print Counter(label_dis)
#    print "======in the evaluation script============"
    for index in range(len(predicted)):
        if predicted[index] in instances[index]["clf_label"]:
                No_corr+=1
    print "The ACC of the multiClass classification results:" + str(float(No_corr)/len(predicted))
    print len(predicted)
    print len(instances)

    path_json_out = "/Users/xiangyuanxin/PycharmProjects/imBaselineAttr/imTrainCorenlp.Bas.multiClass"
    for i in range(len(predicted)):
        instances[i]["PredictionMultiClass"] = predicted[i]
    with open(path_json_out, "w") as f:
        json.dump(instances, f, encoding="latin1")
    #print "ACC of multiClass result: %f" % float(No_corr)/len(predicted)

def evaluation(predicted, instances, parameters, saveLogPath, saveConfusionMatrixPath):
    print parameters
    F = -1
    relation = parameters["relation"]
    if(relation.lower() == "multiclass"):
        multiClassEvaluation(predicted, instances)
    elif(relation.lower() == "fourway"):
        #call the evaluation script four times
        label_dis = []
        for i in range(len(predicted)):
            label_dis.append(predicted[i])
        print "evaluation:", Counter(label_dis)

        for relation_all in ["Contingency", "Expansion", "Comparison", "Temporal"]:
            evaluation_old(predicted, instances, relation_all)
        createAndSaveConfusionMatrix(predicted, instances, parameters, saveConfusionMatrixPath)
    else:
        F = evaluation_old(predicted, instances, relation)
        #createAndSaveConfusionMatrix(predicted, instances, parameters, saveConfusionMatrixPath)
    return F



