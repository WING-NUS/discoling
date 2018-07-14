import os
import nltk
import json
from pprint import pprint
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2

#need to modify the label representation, ideally, all strings
def Data_preparation(instances, isTraining, ex_fac, relation="Comparison"):# input_type can be [random, pre_selected, all_weighting, not_training]
    #ex_fac should use default dictionary
    for ins in instances:
        index = instances.index(ins)
        feature_vector=ins["Baseline"]
        if relation!="4-way":
            if ins["Sense"].find(relation)==-1:
                instances[index]["clf_label"]="none-"+ relation
            else:
                instances[index]["clf_label"]=relation#ins["Sense"].split(".")[0]
        else:
            instances[index]["clf_label"] = ins["Sense"].split(".")[0]

    if isTraining == True: #only training data need to be re-weighted
        training_labels=[x["clf_label"] for x in instances]
        label_count=Counter(training_labels)
        numerator=float(min(label_count.values()))
        weight = [ex_fac[x["clf_label"]] * numerator / label_count[x["clf_label"]] for x in instances]
        #weight=[]
        #for x in instances:
        #    weight.append(ex_fac[x["clf_label"]] * numerator / label_count[x["clf_label"]])
        #        print "######data preparation results"
        #        print "label_count:"
        #        print label_count
        #        print "weight before re-weight:"
        #        print [numerator / label_count[x["clf_label"]] for x in instances]
        #        print "weight after re-weight:"
        #        print weight
        return instances, weight
    else:
        return instances



def PreProcessing(train, test, relation, prun_off_threshold, percent, ex_fac):#including instance weighting, necessary data preparation
    # assign label for each kind of relation, compose balanced data set
    train, train_weight= Data_preparation(train, True, ex_fac, relation) # convertig labels for binary classification
    test = Data_preparation(test, False, ex_fac, relation) # The return value of train and test are different
    
    
    # convert feature list to feature string, for both baseline feature and my own feature.
    X_train, y_train = [x["Baseline"] for x in train], [x["clf_label"] for x in train]
    X_test = [x["Baseline"] for x in test]
    
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
    
    #    print "original feature vector dimension: "+ str(X_train_vec.shape)
    #    print "feature dimension after selection"+ str(len(selected_feature_list))
    #    print "training labels:"
    #    print y_train
    #    print "testing data labels:"
    #    print [x["LabelList"] for x in test]
    
    return X_train_selected, y_train, X_test_selected, train_weight, X_train, X_test, selected_feature_list








