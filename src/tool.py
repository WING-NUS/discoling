import json
import os
from pprint import pprint
#import Tree_algorithm as ta
import json
from sklearn.feature_extraction.text import CountVectorizer
import random
from collections import Counter

# This is to assign the weight to instances all instances are used
def Instance_weighting(instances):
    return instances

# This is to integrate all features into one feature list, transfer feature format
def Feature_vector_string(instances):
    X = []
    y = []
    for ins in instances:
        #print ins
        all_feature=[]
        for string_align_pair in instances[ins]["Alignment"]:
            for feature_type in ["Lexical_Feature", "Position_Feature"]:
                for feature in instances[ins]["Alignment"][string_align_pair][feature_type]:
                     all_feature.append(feature)
            all_feature.append(instances[ins]["Alignment"][string_align_pair]["AlignType"])
        X.append(" ".join(all_feature))
        y.append(instances[ins]["Label"])
    return X, y

# This is to compose data set to do binary classification
def Data_preparation(instances, input_type, relation):# input_type can be [random, pre_selected, all_weighting, not_training]
    # compose training and testing data
    for ins in instances:
        if instances[ins]["Sense"].find(relation)!=-1:
            instances[ins]["Label"]=True
        else:
            instances[ins]["Label"]=False
    if input_type=="random":
        #pos_list, neg_list=Seperate_pos_neg(instances, relation)
        pos_list=[x for x in instances if instances[x]["Label"]==True]
        neg_list=[x for x in instances if instances[x]["Label"]==False]
        min_length=min(len(pos_list),len(neg_list))
        pos_list=random.sample(pos_list,min_length)
        neg_list=random.sample(neg_list,min_length)
        all_keys=instances.keys()
        #for ins in all_keys:
        #    if ins not in pos_list+neg_list:
         #       del instances[ins]
        new_instances={}
        for ins in pos_list+neg_list:
            new_instances[ins]=instances[ins]
        return new_instances
    if input_type=="pre_selected":
        if relation=="Comparison":
            with open(constant.path_all+constant.im_comp_balance) as f:
                instances=json.load(f)
        elif relation=="Contingency":
            with open(constant.path_all+constant.im_cont_balance) as f:
                instances=json.load(f)
        elif relation=="Expansion":
            with open(constant.path_all+constant.im_exp_balance) as f:
                instances=json.load(f)
        else:
            with open(constant.path_all+constant.im_temp_balance) as f:
                instances=json.load(f)
        return instances

    if input_type=="all_weighting":
        weight=[]
        pos_list=[x for x in instances if instances[x]["Label"]==True]
        neg_list=[x for x in instances if instances[x]["Label"]==False]
        num_pos=len(pos_list)
        num_neg=len(neg_list)
        numerator=min(num_neg,num_pos)
        for ins in instances:
            if instances[ins]["Label"]==True:
                weight.append(float(numerator)/float(num_pos))
            else:
                weight.append(float(numerator)/float(num_neg))
        return instances, weight
    if input_type=="not_training":
        return instances

def Get_ins(arg,text_span):#find instances satisfying a certain condition
    #perform stats and corss validation only on training data
    files=["exDev","exExtradev","exTrain","exTest","imDev","imExtradev","imTrain","imTest"]
    #path_all="D:\\WenqiangWorkspace\\data\\json_comparison_all"
    results=[]
    for f in files:
        with open(os.path.join(constant.path_all,f),"r") as ff:
            instances=json.load(ff)
            for ins in instances:
                if instances[ins][arg]["RawText"].find(text_span)!=-1:
                    results.append((f, ins))
                    print f+": "+ins
                    print "Arg1:"+instances[ins]["Arg1"]["RawText"]
                    print "Arg2:"+instances[ins]["Arg2"]["RawText"]
                    print instances[ins]["Sense"]
                    print "########################"
    return results


def Feature_vec(instances):
    X=[]
    y=[]
    for ins in instances:
        feature_string = ""
        #print "feature vector conversion"+ins
        for feature in ["Baseline"]:
        #for feature in ["AllAlignFeatures"]:
            feature_string=feature_string+" "+ instances[ins][feature]
        X.append(feature_string.strip())
        y.append(instances[ins]["Label"])
    return X,y

def Print_ins(ins): #print crucial information of each instance
    print ins["Arg1"]["RawText"]
    print ins["Arg2"]["RawText"]
    print ins["Conn"]
    print ins["Sense"]
    #print instances[ins]["Label"]
    pprint(ins["Monolingual_align"])
    pprint(ins["Coref"])


def feature_for_nltk(X, y, selected_feature_list, weight, data_set):
    selected_feature_list=set(selected_feature_list)
    instances_for_classifier=[]
    #print "Y:"+ str(len(y))
    #print "X:"+ str(len(X))
    for index in range(len(X)):
        splitted=set(X[index].split(" "))
        feature_list=list(splitted.intersection(selected_feature_list))
        feature_dict=dict(Counter(feature_list))

        if data_set=="train":
            instance=(feature_dict,y[index],weight[index])
        else:
            instance=feature_dict
        instances_for_classifier.append(instance)

    return instances_for_classifier
'''
# read in data to do preparation
path_full_data=""
path_train="D:\\WenqiangWorkspace\\data\\comparison_feature_generation\\imTrainBalancedCorenlpMonolingual_alignALLAlignedFeature"
path_test="D:\\WenqiangWorkspace\\data\\comparison_feature_generation\\imTestCorenlpMonolingual_alignALLAlignedFeature"
path_dev="D:\\WenqiangWorkspace\\data\\comparison_feature_generation\\imDevCorenlpMonolingual_alignALLAlignedFeature"
with open(path_train,"r") as f:
    data_train=json.load(f)
with open(path_test,"r") as f:
    data_test=json.load(f)
with open(path_dev,"r") as f:
    data_dev=json.load(f)

#prepare data for comparision
relation="Comparison"
instances_train=Data_preparation(data_train, "random", relation)
instances_dev=Data_preparation(data_dev, "not_training", relation)
instances_train=Data_preparation(data_test, "not_training", relation)
'''
#print Get_ins("Arg1","Drugs were a major issue in")