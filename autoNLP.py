from collections import defaultdict
from config import constants
import json
from src import baselines
from src import classification
from evaluation import evaluation
from collections import Counter
from pprint import pprint
from config.constants import evaluate_relation_l



def paramGeneration():
    totalParaDict=[]
    featureList=['Prediction','AttrAct', 'UseFeature']#xyx add 'AttrAct'
    #for clf in ["sk_MNB"]:#, 'sk_LG','nltk_NB']:
    for clf in ["nltk_NB",]:
        for percentile in range(100 , 110, 10):#10,110,10
            #for relation in ["Comparison", "Contingency", "Expansion", "Temporal"]:#fourway
            for relation in [ evaluate_relation_l, ]:#["Comparison", "Contingency", "Expansion", "Temporal", "fourway"]
                for rate in range(10,11,1):
                    paraDict={
                        'featureList':featureList, "relation": relation,
                        'incremental': False, 'clf': clf, 'percentile':percentile, 'featureSelect':'chi2', "min_df":5,#Expansion":1.8
                        'extraFac': defaultdict(lambda :1.1,{"Comparison":1.0, "Contingency": 1.4, "Temporal": 1.3, "Expansion":1.8})# contingency 0.65
                    }#"Contingency": 0.65
                    totalParaDict.append(paraDict)
    return totalParaDict

def readInFile():
    with open(constants.train_path) as f:
        train=json.load(f)
    with open(constants.test_path) as f:
        test=json.load(f)
    return train, test

def featureGeneration(instances, paraDict):
    for ins in instances:
        ins["features"]=""
        '''
        if "Baseline" in paraDict["featureList"]:
            ins["features"]=baselines.baselineFeature(ins)
        '''
        '''
        if "AttrAct" in paraDict["featureList"]:
            ins["features"] = baselines.AttrActFeature(ins)
        '''

        if "UseFeature" in paraDict["featureList"]:
            ins["features"] = baselines.UseFeature(ins)
        '''
        if "Contingency" in paraDict["featureList"]:
            ins["features"] = baselines.ContigencyFeature(ins)
        '''
        '''
        if "Prediction" in paraDict["featureList"]:
            ins["features"] = baselines.UsePredictionResultAsFeature(ins)
        '''
        #print ins["features"]
    return instances

baseLineValue = {}
def pipLine(train, test, paraDict):
    # feature generation
    print "currently predicting %s relation" % paraDict["relation"]
    #print "starting feature generation:"
    train = featureGeneration(train, paraDict)
    test = featureGeneration(test, paraDict)

    predicted, test = classification.classification(train, test, paraDict, constants.log_path, constants.confusionM_path)
    '''
    count = 0
    for i in range(len(test)):
        if(test[i]["PredictionTemporal"] != predicted[i]):
            count = count + 1
        if(len(test[i]["contingency"]["RelationLevel_Span"]) > 0):#have relaAttr
            predicted[i] = "none-Temporal"
    print "count: ", count
    #print "length of predicted:", len(predicted)
    #print "Distribution of predicted results:" + str(Counter(predicted))
    '''
    #print "starting evaluation"
    #evaluation
    evaluation.evaluation(predicted, test, paraDict, constants.log_path, constants.confusionM_path)

#if __name__=='main':
# read in files
train,test=readInFile()
totalParaDict=paramGeneration()


#feed data into our pipeline
for paraDict in totalParaDict:
    pipLine(train, test, paraDict)

