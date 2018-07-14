# try general inquirer lexicon feature
import json
from sklearn.feature_extraction.text import CountVectorizer
import tool as tl
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_selection import chi2
import nltk
from sklearn import svm
from pprint import pprint
import os
from sklearn.feature_selection import SelectPercentile
from sklearn.linear_model import LogisticRegression
from collections import Counter
import evaluation
multiRelations=['Contingency.Cause', 'Expansion.Restatement', 'Expansion.Conjunction', 'Comparison.Contrast', \
                'Expansion.Instantiation','Temporal.Asynchronous', 'Temporal.Synchrony', 'Comparison.Concession', \
                'Expansion.List', 'Expansion.Alternative', 'Contingency.Pragmatic cause']

def getLevel2(ss): # get the level 2 relation. If it is not exist, return the level 1 relation
    if len(ss.split("."))==3:
        return ss.split(".")[0]+"."+ss.split(".")[1]
    else:
        return ss

def getLevel1(ss): # get the level 1 relation.
    return ss.split(".")[0]


def prepareTest(instances, relation):
    new_instances=[]
    label_dis = []
    if relation=="multiClass":
        for ins in instances:
            ins["clf_label"]=[getLevel2(label) for label in ins["LabelList"]]
            if  set(ins["clf_label"]) - set(multiRelations)==set([]):
                new_instances.append(ins)
    elif(relation == "fourway"):
        for ins in instances:
            ins["clf_label"] = [getLevel1(label) for label in ins["LabelList"]]

            for element in ins["clf_label"]:
                label_dis.append(element)
            #print "ins[clf_label]", ins["clf_label"]
            new_instances.append(ins)
    else:
        for ins in instances:
            ins["clf_label"] = []
            for label in ins["LabelList"]:
                if label.find(relation)!=-1:
                    ins["clf_label"].append(relation)
                else:
                    ins["clf_label"].append("none-"+relation)
            new_instances.append(ins)
    #print "Test:",Counter(label_dis)
    return new_instances

def prepareTrain(instances, relation, ex_fac): # copy instances in this function
    new_instances=[]
    label_dis = []
    for ins in instances:
        #for label in ins["clf_label"]:
        ins["Sense"]=ins["clf_label"][0]
        label_dis.append(ins["Sense"])
        new_instances.append(ins)
    #print "Train:", Counter(label_dis)
    training_labels = [x["Sense"] for x in new_instances]
    label_count = Counter(training_labels)
    #print "Distribution of training instances: " + str(label_count)
    numerator=float(min(label_count.values()))
    weight = [ex_fac[x["Sense"]] * numerator / label_count[x["Sense"]] for x in new_instances]
    #print "Instance weight distribution:" + str(Counter(weight))
    if relation=="multiClass" or relation=="fourway":
        #weightDict = {"Expansion": 1, "Contingency": 1.5, "Comparison": 1.5, "Temporal": 2.5}
        #weight = [weightDict[x["Sense"]] for x in new_instances]
        #weight = [1 for x in new_instances]
        #!!weightDict = {"Expansion": 1.5, "Contingency": 3.5, "Comparison": 3, "Temporal": 7.0}#weightDict = {"Expansion": 2, "Contingency": 6, "Comparison": 6.5, "Temporal": 7.0}
        weightDict = {"Expansion": 2.5, "Contingency": 6, "Comparison": 5.5, "Temporal": 4.0}
        #weightDict = {"Expansion": 2.5, "Contingency": 5.5, "Comparison": 4.5, "Temporal": 4.0}
        #weightDict = {"Expansion": 2.5, "Contingency": 5, "Comparison": 4.5, "Temporal": 7.0}
        weight = [weightDict[x["Sense"]] for x in new_instances]
    return new_instances, weight



def Data_preparation(instances, isTraining, ex_fac, relation="Comparison"):# input_type can be [random, pre_selected, all_weighting, not_training]
#ex_fac should use default dictionary
#this function also convert the label

    #for ins in instances:
    #    index = instances.index(ins)
    #    if relation!="multiClass": # preparing data for
    #        if ins["Sense"].find(relation)==-1:
    #            instances[index]["clf_label"]="none-"+ relation
    #        else:
    #            instances[index]["clf_label"]=relation
    #    else:# for multiClass prediction, we need the first two level labels
    #        if len(ins["Sense"].split("."))==3:
    #            lvl1,lvl2,lvl3=ins["Sense"].split(".")
    #            instances[index]["clf_label"]=lvl1+"."+lvl2
    #        else:
    #            instances[index]["clf_label"]=ins["Sense"]
    instances=prepareTest(instances,relation)
    if isTraining == True: #only training data need to be re-weighted
        #training_labels=[x["clf_label"] for x in instances]
        #label_count=Counter(training_labels)
        #numerator=float(min(label_count.values()))
        #weight = [ex_fac[x["clf_label"]] * numerator / label_count[x["clf_label"]] for x in instances]
        #if relation=="multiClass":
        #    weight = [1 for x in instances]
        return prepareTrain(instances, relation, ex_fac)
    else:
        return instances

def PreProcessing(train, test, relation, prun_off_threshold, percent, ex_fac):
    #including instance weighting, necessary data preparation
    # assign label for each kind of relation, compose balanced data set
    train, instance_weight= Data_preparation(train, True, ex_fac, relation)
    test = Data_preparation(test, False, ex_fac, relation)
    #print "data preparation done"

    # convert feature list to feature string, for both baseline feature and my own feature.
    X_train, y_train = [x["features"] for x in train], [x["Sense"] for x in train]
    X_test, y_test= [x["features"] for x in test], [x["clf_label"] for x in test] # y_test is actually useless, I put it here just to fit the nltk data structure
    #print "feature string done"


    vectorizer = CountVectorizer(min_df=prun_off_threshold, token_pattern='[^ ]{1,}', binary=True, lowercase=False)
    vectorizer.fit_transform(X_train)
    X_train_vec = vectorizer.transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    #print "data transformation done"

    #here, we can do some feature selection
    selection=SelectPercentile(chi2, percent).fit(X_train_vec, y_train)
    X_train_selected=selection.transform(X_train_vec)
    X_test_selected=selection.transform(X_test_vec)
    selected_index=selection.get_support(True)
    #print "feature selection done"

    feature_list=vectorizer.get_feature_names()
    selected_feature_list=[feature_list[x] for x in selected_index]

    #print "original data scale: "+ str(X_train_vec.shape)
    #print "feature dimension after selection: "+ str(len(selected_feature_list))
    #155570
    return X_train_selected, y_train, X_test_selected, instance_weight, X_train, X_test, y_test, selected_feature_list, test


#following is the usage of of scikit learn NB
def Sk_Learn(X_train_selected, y_train, instance_weight, X_test_selected, y_test, alpha=1,classifier="BNB"):
    # perform classification
    #clf = svm.SVC()
    #clf = MultinomialNB(alpha)
    if classifier=="BNB":
        clf = BernoulliNB(alpha)
    elif classifier=="MNB":
        clf = MultinomialNB(alpha)
    elif classifier=="LG":
        clf = svm.SVC()
        #clf = LogisticRegression(solver="sag")
    elif classifier=="GNB":
        clf = GaussianNB()
    clf.fit(X_train_selected, y_train, instance_weight)
    #y_train_predicted = clf.predict(X_train_vec)
    y_test_predicted = clf.predict(X_test_selected)

    return y_test_predicted



def Nltk_Nb(X_train, y_train, X_test, y_test, instance_weight, selected_feature_list):
    #preparing data formate for nltk
    #feature_token = tl.feature_tokens(X_train,threshold)#convert feature into list and discard low frequency feature
    train_for_clf=tl.feature_for_nltk(X_train, y_train, selected_feature_list, instance_weight, "train")
    #print [x[2] for x in train_for_clf]
    #print Counter([x[2] for x in train_for_clf])

    weight_for_test=[1 for x in y_test]
    test_for_clf=tl.feature_for_nltk(X_test,y_test,selected_feature_list,weight_for_test,"test")

    #print Counter(y_train)
    #print len(Counter(y_train))
    #print Counter(y_test)
    #print len(Counter(y_test))
    #pprint(train_for_clf)
    classifier = nltk.NaiveBayesClassifier.train_weighted(train_for_clf)
    print "-----------------------Most informative Features---------------------"
    classifier.show_most_informative_features(n=20)
    print "-----------------------Most informative Features---------------------"
    y_test_predicted=[]
    for i in range(len(test_for_clf)):
        #if("AttrAct_exist" in test_for_clf[i].keys() and "none-Contingency" in test_for_clf[i].keys() and "Contingency" in y_test[i]):
        #    print "Value == 1"
        #if(i == 50):
        #    print "i == 50"
        y_test_predicted.append(classifier.classify(test_for_clf[i]))

    #print Counter(y_test_predicted)
    return y_test_predicted


'''
paraDict={
    'featureList':featureList, "relation": relation,
    'incremental': False, 'clf': clf, 'percentile':percentile, 'featureSelect':'chi2', "min_df":5,
    'extraFac': defaultdict(lambda :1.0,{"Comparison":0.8, "Contingency": 0.55, "Temporal": 1, "Expansion":1})
}
"sk_MNB", 'sk_LG','nltk_NB'
'''
def classification(train, test, paraDict, log_path, confusionM_path):
    min_def=paraDict["min_df"]
    ex_fac=paraDict["extraFac"]
    clf=paraDict["clf"]
    featureSelect=paraDict["featureSelect"]
    percentile=paraDict["percentile"]
    relation=paraDict["relation"]
    #print "starting data preprocessing"

    X_train_selected, y_train, X_test_selected, instance_weight, X_train, X_test, y_test, selected_feature_list, test \
        = PreProcessing(train,test,relation,prun_off_threshold=min_def,percent=percentile, ex_fac=ex_fac)


    #print "Distribution of y_train:"
    #print Counter(y_train)
    #print len(Counter(y_train).keys())
    #print "instance weight distribution:"
    #print Counter(instance_weight)
    #print "start to building model"
    #P, R, F, ACC = Nltk_Nb(X_train, y_train, X_test, y_test, instance_weight, selected_feature_list)
    #print "nltk P:%s\nR:%s\nF:%s\nACC:%s\n" % (P, R, F, ACC)

    #P, R, F, ACC = Sk_Learn(X_train_selected, y_train, instance_weight, X_test_selected, y_test, alpha=0.5,classifier="BNB")
    #print "Bernoulli P:%s\nR:%s\nF:%s\nACC:%s\n" % (P, R, F, ACC)

    #P, R, F, ACC = Sk_Learn(X_train_selected, y_train, instance_weight, X_test_selected, y_test, alpha=0.5,classifier="MNB")
    #print "multinomial P:%s\nR:%s\nF:%s\nACC:%s\n" % (P, R, F, ACC)

    #P, R, F, ACC = Sk_Learn(X_train_selected, y_train, instance_weight, X_test_selected, y_test, alpha=0.5,classifier="LG")
    #print "LG P:%s\nR:%s\nF:%s\nACC:%s\n" % (P, R, F, ACC)
    #print "starting training"
    if clf=="nltk_NB":
        y_test_predicted=Nltk_Nb(X_train, y_train, X_test, y_test, instance_weight, selected_feature_list)
    if clf=="sk_MNB":
        y_test_predicted=Sk_Learn(X_train_selected, y_train, instance_weight, X_test_selected, y_test, alpha=0.5,classifier="MNB")
    if clf == "sk_BNB":
        y_test_predicted = Sk_Learn(X_train_selected, y_train, instance_weight, X_test_selected, y_test, alpha=0.5,classifier="BNB")
    if clf=="sk_LG":
        y_test_predicted=Sk_Learn(X_train_selected, y_train, instance_weight, X_test_selected, y_test, alpha=0.5,classifier="LG")
    if clf=="sk_GNB":
        y_test_predicted = Sk_Learn(X_train_selected, y_train, instance_weight, X_test_selected, y_test, alpha=0.5,classifier="GNB")
    return y_test_predicted, test
