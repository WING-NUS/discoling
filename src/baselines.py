import json
import operator
from pprint import pprint
from config.constants import evaluate_relation_l

evaluate_relation = evaluate_relation_l

def getStrongFeatures(relation, percentil, Path):
    FeaturesList = []
    with open(Path) as f:
        FeaturesDict = json.load(f, encoding="latin1")
    for key in FeaturesDict.keys():
        if(float(FeaturesDict[key]["rate"]) >= percentil):
            if(int(FeaturesDict[key][relation]) >= 5):
                #if(key != "arg2NegPure"):
                FeaturesList.append(key)
    return FeaturesList

def getSortedFeatures(relation, Path):
    NewFeaturesDict = {}
    with open(Path) as f:
        FeaturesDict = json.load(f, encoding="latin1")
    for key in FeaturesDict.keys():
        if (int(FeaturesDict[key][relation]) >= 5):
            NewFeaturesDict[key] = FeaturesDict[key]
    sortedList = sorted(NewFeaturesDict, key=lambda x: NewFeaturesDict[x]["rate"])
    return sortedList

def getSelectedFeatures(TopK, relation, sortedList):
    FeaturesList = []
    for i in range(1, TopK):
        FeaturesList.append(sortedList[-i])
    return FeaturesList
printCount = 0
path_json1 = "../WordNetTask/ComparisonFeaturesDict"  # source
path_json2 = "../WordNetTask/ContingencyFeaturesDict"  # source
path_json3 = "../WordNetTask/ExpansionFeaturesDict"  # source
path_json4 = "../WordNetTask/TemporalFeaturesDict"  # source

#path_json1_filter = "/Users/xiangyuanxin/PycharmProjects/WordNetTask/ComparisonFeaturesDict_AfterFilter"  # source
#path_json2_filter = "/Users/xiangyuanxin/PycharmProjects/WordNetTask/ContingencyFeaturesDict_AfterFilter"  # source
#path_json3_filter = "/Users/xiangyuanxin/PycharmProjects/WordNetTask/ExpansionFeaturesDict_AfterFilter"  # source
#path_json4_filter = "/Users/xiangyuanxin/PycharmProjects/WordNetTask/TemporalFeaturesDict_AfterFilter"  # source


ComparisonFeatures = getStrongFeatures("Comparison", 0.182, path_json1)#0.182
ContingencyFeatures = getStrongFeatures("Contingency", 0.432, path_json2)#0.431
ExpansionFeatures = getStrongFeatures("Expansion", 0.63, path_json3)#0.63
TemporalFeatures = getStrongFeatures("Temporal", 0.21, path_json4)#0.20

#ComparisonFeatures = getStrongFeatures("Comparison", 0.17, path_json1)#TOP10
#ContingencyFeatures = getStrongFeatures("Contingency", 0.430, path_json2)#TOP10
#ExpansionFeatures = getStrongFeatures("Expansion", 0.548, path_json3)#Top10
#TemporalFeatures = getStrongFeatures("Temporal", 0.0727, path_json4)#TOP5
def baselineFeature(ins):
    if "Baseline" in ins.keys():
        return ins["Baseline"]
    else:# TO Do
        pass


def UseFeature(ins):
    tmp = ""
    tmp = Features(ins)
    #tmp = baselineFeature(ins)

        #UseComparisonPrediction(ins)\
          #+ " " + UseComparisonArg2NegPure_Arg2Predi_Arg1(ins)\
          #+ " " + UseComparisonArg1NegPure_Arg1Predi_Arg2(ins)\
          #+ " " + UseComparisonArg2NegPure_Agr2Subj_Arg1(ins)\
          #+ " " + UseComparisonArg1NegPure_Arg1Subj_Arg2(ins)

            #UsePredictionResultAsFeature(ins)+ " " + UseIntentionSay(ins) \
          # + " " + UseSubjectWord(ins)# + " " + UseIntentionDo(ins)
            #+ " " + UseExtensionSameNPSameVP(ins)
    #tmp = AttrActFeature(ins) + " " + UsePredictionResultAsFeature(ins)
    tmp.strip()
    return tmp

def Features(ins):
    global printCount
    resultString = ""
    if ("contingency" in ins.keys()):
        if ("XX_Intention_Do" not in ins.keys()):
            return resultString
        parameter = ins["comparePattern"]
        attr = parameter["attr"]
        coref_both = parameter["coref_both"]
        negete = parameter["negete"]
        ner = parameter["ner"]
        subjsubjRepeatResreict = parameter["subjsubjRepeatResreict"]
        subj_subjRepeat = parameter["subj_subjRepeat"]
        resultDict_SubjPrediCorefOther = parameter["resultDict_SubjPrediCorefOther"]
        resultDict_SubjPrediCorefOtherEvidence = parameter["evidence_SubjPrediCorefOther"]
        # arg1Neg = (negete[0] or negete[2]) and not negete[5]
        # arg2Neg = (negete[1] or negete[3]) and not negete[4]
        sent1NegativeWords = parameter["sent1NegativeWords"]
        sent2NegativeWords = parameter["sent2NegativeWords"]

        nega1_1 = sent1NegativeWords["mainVerbNeg"] ^ sent1NegativeWords["mainVerbModNeg"] ^ sent1NegativeWords[
            "mainVerbConjNeg"] ^ \
                  sent1NegativeWords["mainVerbModModNeg"] ^ negete[0]
        nega1_2 = negete[2] ^ sent1NegativeWords["xcompNeg"] ^ sent1NegativeWords["ccompNeg"]

        nega2_1 = sent2NegativeWords["mainVerbNeg"] ^ sent2NegativeWords["mainVerbModNeg"] ^ sent2NegativeWords[
            "mainVerbConjNeg"] ^ \
                  sent2NegativeWords["mainVerbModModNeg"] ^ negete[1]
        nega2_2 = negete[3] ^ sent2NegativeWords["xcompNeg"] ^ sent2NegativeWords["ccompNeg"]
        # arg1Neg = nega1_1 or nega1_2
        # arg2Neg = nega2_1 or nega2_2
        arg1Neg = ((negete[0] ^ negete[2]))  # and not negete[4]
        arg2Neg = ((negete[1] ^ negete[3]))  # and not negete[5]
        arg1NegPure = 1 if (arg1Neg and not arg2Neg) else 0
        arg2NegPure = 1 if (arg2Neg and not arg1Neg) else 0

        Arg1Subj_Repeat_Arg2 = resultDict_SubjPrediCorefOther["Arg1Subj_Repeat_Arg2"]
        Arg1Subj_Coref_Arg2 = resultDict_SubjPrediCorefOther["Arg1Subj_Coref_Arg2"]
        Arg2Subj_Repeat_Arg1 = resultDict_SubjPrediCorefOther["Arg2Subj_Repeat_Arg1"]
        Arg2Subj_Coref_Arg1 = resultDict_SubjPrediCorefOther["Arg2Subj_Coref_Arg1"]

        Arg1Predi_Repeat_Arg2 = resultDict_SubjPrediCorefOther["Arg1Predi_Arg2"]
        Arg2Predi_Repeat_Arg1 = resultDict_SubjPrediCorefOther["Arg2Predi_Arg1"]

        Arg1Subj_RepeatAttr2Relation = resultDict_SubjPrediCorefOther["Arg1Subj_RepeatAttr2Relation"]
        Arg2Subj_RepeatAttr1Relation = resultDict_SubjPrediCorefOther["Arg2Subj_RepeatAttr1Relation"]

        Arg1Predi_RepeatAttr2Relation = resultDict_SubjPrediCorefOther["Arg1Predi_RepeatAttr2Relation"]
        Arg2Predi_RepeatAttr1Relation = resultDict_SubjPrediCorefOther["Arg2Predi_RepeatAttr1Relation"]

        parameter2 = ins["expansionPattern"]
        extensionNERValue = parameter2["extensionNERValue"]
        extensionArg2NPhasNERorModifierValue = parameter2["extensionArg2NPhasNERorModifierValue"]
        extensionHasINDEFWordValue = parameter2["extensionHasINDEFWordValue"]

        contingency = ins["contingency"]
        intension = contingency["Intension"]
        sent1xxintensionDo = (intension["sent1HasIntensionWord"] and not intension["sent2HasIntensionWord"]) and \
                             (coref_both[0] or coref_both[1]) and intension["sent2ReallyDo"]["value"]
        sent2xxintensionDo = (intension["sent2HasIntensionWord"] and not intension["sent1HasIntensionWord"]) and \
                             (coref_both[0] or coref_both[1]) and intension["sent1ReallyDo"]["value"]
        xxintensionDo = sent1xxintensionDo ^ sent2xxintensionDo

        # intension = ins["tmp"]["Intension"]
        sent1xxintensionSay = (intension["sent1HasIntensionWord"] and not intension["sent2HasIntensionWord"]) and \
                              (intension["sent1SubjCorefSent2Attr"] or intension["sent1SubjCorefsent1RelaAttr"])
        sent2xxintensionSay = (intension["sent2HasIntensionWord"] and not intension["sent1HasIntensionWord"]) and \
                              (intension["sent2SubjCorefSent1Attr"] or intension["sent2SubjCorefsent2RelaAttr"])
        xxintensionSay = sent1xxintensionSay ^ sent2xxintensionSay
        # intension = contingency["Intension"]

        sent1xxingDo = ((intension["sent1HasIng"] and not intension["sent2HasIng"]) and (
        coref_both[1] or coref_both[0])) and \
                       intension["sent2ReallyDo"]["value"]
        sent2xxingDo = ((intension["sent2HasIng"] and not intension["sent1HasIng"]) and (
        coref_both[1] or coref_both[0])) and \
                       intension["sent1ReallyDo"]["value"]
        xxingDo = sent1xxingDo ^ sent2xxingDo
        sent1xxingSay = (intension["sent1HasIng"] and (
            intension["sent1SubjCorefSent2Attr"] or intension["sent1SubjCorefsent1RelaAttr"]))
        sent2xxingSay = (intension["sent2HasIng"] and (
            intension["sent2SubjCorefSent1Attr"] or intension["sent2SubjCorefsent2RelaAttr"]))
        xxingSay = sent1xxingSay ^ sent2xxingSay
        xxWeareding = intension["sent1Wearedoing"] ^ intension["sent2Wearedoing"]
        hasWeAre = intension["sent1HasWeare"] ^ intension["sent2HasWeare"]
        hasSubjectWordResultDict = contingency["hasSubjectWord"]
        hasSubjectWord_attr1 = hasSubjectWordResultDict["hasSubjectWord_attr1"]
        hasSubjectWord_attr2 = hasSubjectWordResultDict["hasSubjectWord_attr2"]
        hasSubjectWord_RelaAttr = hasSubjectWordResultDict["hasSubjectWord_RelaAttr"]
        subjectiveWord = contingency["subjectiveWord"]
        mainVerbSubjectiveResultDict = contingency["mainVerbSubjectiveResultDict"]
        arg1SubjectiveArg2DoNot = mainVerbSubjectiveResultDict["splitFeatures"]["arg1SubjectiveArg2DoNot"]
        arg2SubjectiveArg1DoNot = mainVerbSubjectiveResultDict["splitFeatures"]["arg2SubjectiveArg1DoNot"]
        # SubjectiveArg1NegBe = mainVerbSubjectiveResultDict["splitFeatures"]["SubjectiveArg1NegBe"]
        # SubjectiveArg2NegBe = mainVerbSubjectiveResultDict["splitFeatures"]["SubjectiveArg2NegBe"]

        arg1SubjectiveArg2DoNot_1 = mainVerbSubjectiveResultDict["splitFeatures"]["arg1SubjectiveArg2DoNot_1"]
        arg1SubjectiveArg2DoNot_2 = mainVerbSubjectiveResultDict["splitFeatures"]["arg1SubjectiveArg2DoNot_2"]
        arg1SubjectiveArg2DoNot_3 = mainVerbSubjectiveResultDict["splitFeatures"]["arg1SubjectiveArg2DoNot_3"]
        arg1SubjectiveArg2DoNot_4 = mainVerbSubjectiveResultDict["splitFeatures"]["arg1SubjectiveArg2DoNot_4"]

        arg2SubjectiveArg1DoNot_1 = mainVerbSubjectiveResultDict["splitFeatures"]["arg2SubjectiveArg1DoNot_1"]
        arg2SubjectiveArg1DoNot_2 = mainVerbSubjectiveResultDict["splitFeatures"]["arg2SubjectiveArg1DoNot_2"]
        arg2SubjectiveArg1DoNot_3 = mainVerbSubjectiveResultDict["splitFeatures"]["arg2SubjectiveArg1DoNot_3"]
        arg2SubjectiveArg1DoNot_4 = mainVerbSubjectiveResultDict["splitFeatures"]["arg2SubjectiveArg1DoNot_4"]

        Weare = contingency["hasWeare"]
        AttrbutionMainVerb = contingency["intensionMainVerb"]

        RelationLevel_Span = int(len(contingency["RelationLevel_Span"]) > 0)
        intensionAttrInDefWordNerValue = contingency["intensionAttrInDefWordNerValue"]
        intensionAttrInDefWordNerEvidence = contingency["intensionAttrInDefWordNerEvidence"]
        extensionHasINDEFWordValue2 = parameter2["extensionHasINDEFWordValue2"]
        extensionHasINDEFWordEvidence = parameter2["extensionHasINDEFWordEvidence"]

        key = []
        keyOrder = []

        if evaluate_relation == "fourway":
            if (ins["Predictionfourway"] == "Expansion"):
                key.append(1)
            else:
                key.append(0)
            keyOrder.append("FourWayExpansion")
            if (ins["Predictionfourway"] == "Contingency"):
                key.append(1)
            else:
                key.append(0)
            keyOrder.append("FourWayContingency")
            if (ins["Predictionfourway"] == "Comparison"):
                key.append(1)
            else:
                key.append(0)
            keyOrder.append("FourWayComparison")
            if (ins["Predictionfourway"] == "Temporal"):
                key.append(1)
            else:
                key.append(0)
            keyOrder.append("FourWayTemporal")

        DiscourseRelation_SpecificInteraction_Comparison = []
        DiscourseRelation_SpecificInteractionName_Comparison = []

        DiscourseRelation_SpecificInteraction_Contingency = []
        DiscourseRelation_SpecificInteractionName_Contingency = []

        ##################### negation
        DiscourseRelation_SpecificInteraction_Comparison.append(arg1NegPure)
        DiscourseRelation_SpecificInteractionName_Comparison.append("arg1NegPure")

        DiscourseRelation_SpecificInteraction_Comparison.append(arg2NegPure)
        DiscourseRelation_SpecificInteractionName_Comparison.append("arg2NegPure")
        ##################### negation

        ##################### intesion
        arg1_intension = int((intension["sent1HasIntensionWord"] and not intension["sent2HasIntensionWord"]))
        DiscourseRelation_SpecificInteraction_Contingency.append(arg1_intension)
        DiscourseRelation_SpecificInteractionName_Contingency.append("arg1_intension")

        arg2_intension = int((intension["sent2HasIntensionWord"] and not intension["sent1HasIntensionWord"]))
        DiscourseRelation_SpecificInteraction_Contingency.append(arg2_intension)
        DiscourseRelation_SpecificInteractionName_Contingency.append("arg2_intension")

        DiscourseRelation_SpecificInteraction_Contingency.append(int(Weare))
        DiscourseRelation_SpecificInteractionName_Contingency.append("Weare")
        ###################### intesion

        ################### subjective
        DiscourseRelation_SpecificInteraction_Contingency.append(arg1SubjectiveArg2DoNot_1 \
                                                                 or arg1SubjectiveArg2DoNot_2 \
                                                                 or arg1SubjectiveArg2DoNot_3 \
                                                                 or arg1SubjectiveArg2DoNot_4)
        DiscourseRelation_SpecificInteractionName_Contingency.append("arg1SubjectiveArg2DoNot_1_2_3_4")

        DiscourseRelation_SpecificInteraction_Contingency.append(arg2SubjectiveArg1DoNot_1 or \
                                                                 arg2SubjectiveArg1DoNot_2 or \
                                                                 arg2SubjectiveArg1DoNot_3 or \
                                                                 arg2SubjectiveArg1DoNot_4)
        DiscourseRelation_SpecificInteractionName_Contingency.append("arg2SubjectiveArg1DoNot_1_2_3_4")
        ################### subjective

        AttributionAndCoref_Comparison = []
        AttributionAndCorefName_Comparison = []

        AttributionAndCoref_Contingency = []
        AttributionAndCorefName_Contingency = []

        #AttributionAndCoref_Contingency.append(int(coref_both[0] or coref_both[1]))  # subj_subj coref AND repeat
        #AttributionAndCorefName_Contingency.append("subjCorefRepeat")

        ################### intesion
        AttributionAndCoref_Contingency.append(int(coref_both[0]))  # subj_subj  repeat
        AttributionAndCorefName_Contingency.append("argsubjRepeatsubj")

        AttributionAndCoref_Contingency.append(int(coref_both[1]))  # subj_subj coref
        AttributionAndCorefName_Contingency.append("argsubjCorefsubj")

        AttributionAndCoref_Contingency.append(
            intension["sent1SubjCorefSent2Attr"] or intension["sent1SubjCorefsent1RelaAttr"])
        AttributionAndCorefName_Contingency.append("sent1SubjCorefSent2Attr")

        AttributionAndCoref_Contingency.append(
            intension["sent2SubjCorefSent1Attr"] or intension["sent2SubjCorefsent2RelaAttr"])
        AttributionAndCorefName_Contingency.append("sent2SubjCorefSent1Attr")

        AttributionAndCoref_Contingency.append(Arg1Subj_RepeatAttr2Relation)
        AttributionAndCorefName_Contingency.append("sent1SubjRepeatSent2Attr")

        AttributionAndCoref_Contingency.append(Arg2Subj_RepeatAttr1Relation)
        AttributionAndCorefName_Contingency.append("sent2SubjRepeatSent1Attr")
        ###################### intension

        ################### subjective
        AttributionAndCoref_Contingency.append(RelationLevel_Span)
        AttributionAndCorefName_Contingency.append("RelationLevel_Span")
        ################## subjective

        ##################### negation
        AttributionAndCoref_Comparison.append(Arg1Subj_Repeat_Arg2 or Arg1Subj_RepeatAttr2Relation)
        AttributionAndCorefName_Comparison.append("Arg1SubjRepeat_Arg2andAttr2Rela")

        AttributionAndCoref_Comparison.append(Arg2Subj_Repeat_Arg1 or Arg2Subj_RepeatAttr1Relation)
        AttributionAndCorefName_Comparison.append("Arg2SubjRepeat_Arg1andAttr1Rela")

        AttributionAndCoref_Comparison.append(
            Arg1Subj_Coref_Arg2 or intension["sent1SubjCorefSent2Attr"] or intension["sent1SubjCorefsent1RelaAttr"])
        AttributionAndCorefName_Comparison.append("Arg1SubjCoref_Arg2andAttr2Rela")

        AttributionAndCoref_Comparison.append(
            Arg2Subj_Coref_Arg1 or intension["sent2SubjCorefSent1Attr"] or intension["sent2SubjCorefsent2RelaAttr"])
        AttributionAndCorefName_Comparison.append("Arg2SubjCoref_Arg1andAttr1Rela")

        AttributionAndCoref_Comparison.append(Arg1Predi_Repeat_Arg2 or Arg1Predi_RepeatAttr2Relation)
        AttributionAndCorefName_Comparison.append("Arg1PrediRepeat_Arg2andAttr2Rela")

        AttributionAndCoref_Comparison.append(Arg2Predi_Repeat_Arg1 or Arg2Predi_RepeatAttr1Relation)
        AttributionAndCorefName_Comparison.append("Arg2PrediRepeat_Arg1andAttr1Rela")
        ##################### negation

        for i in range(len(DiscourseRelation_SpecificInteraction_Comparison)):
            discourseRelation = DiscourseRelation_SpecificInteraction_Comparison[i]
            key.append(discourseRelation)
            keyOrder.append(DiscourseRelation_SpecificInteractionName_Comparison[i])

            for j in range(len(AttributionAndCoref_Comparison)):
                attrAndCoref = AttributionAndCoref_Comparison[j]
                key.append(int(discourseRelation and attrAndCoref))
                keyOrder.append(DiscourseRelation_SpecificInteractionName_Comparison[i] + "+" +
                                AttributionAndCorefName_Comparison[j])

        for i in range(len(AttributionAndCoref_Comparison)):
            key.append(AttributionAndCoref_Comparison[i])
            keyOrder.append(AttributionAndCorefName_Comparison[i])

        for i in range(len(DiscourseRelation_SpecificInteraction_Contingency)):
            discourseRelation = DiscourseRelation_SpecificInteraction_Contingency[i]
            key.append(discourseRelation)
            keyOrder.append(DiscourseRelation_SpecificInteractionName_Contingency[i])

            for j in range(len(AttributionAndCoref_Contingency)):
                attrAndCoref = AttributionAndCoref_Contingency[j]
                key.append(int(discourseRelation and attrAndCoref))
                keyOrder.append(DiscourseRelation_SpecificInteractionName_Contingency[i] + "+" +
                                AttributionAndCorefName_Contingency[j])

        for i in range(len(AttributionAndCoref_Contingency)):
            key.append(AttributionAndCoref_Contingency[i])
            keyOrder.append(AttributionAndCorefName_Contingency[i])

        ##################### subjective
        key.append(int(hasSubjectWord_attr1))
        keyOrder.append("hasSubjectWord_attr1")

        key.append(int(hasSubjectWord_attr2))
        keyOrder.append("hasSubjectWord_attr2")

        key.append(int(hasSubjectWord_RelaAttr))
        keyOrder.append("hasSubjectWord_RelaAttr")
        ##################### subjective

        #################### expansion
        key.append(int(extensionNERValue))
        keyOrder.append("extensionNERValue")

        key.append(int(extensionHasINDEFWordValue or intensionAttrInDefWordNerValue))
        keyOrder.append("extensionHasINDEFWordValue")
        #################### expansion

        key_Selected = []
        keyOrder_Selected = []

        if evaluate_relation == "Expansion":
            manuallySelectKey = [
                "PredictionComparison", "PredictionContingency", "PredictionExpansion", "PredictionTemporal",
                                 ]
            notInKey = [
                "arg2NegPure",
                'arg2NegPure+Arg1SubjCoref_Arg2andAttr2Rela',
                'Arg2SubjRepeat_Arg1andAttr1Rela',
                'arg1SubjectiveArg2DoNot_1_2_3_4+sent2SubjCorefSent1Attr',
                'arg2SubjectiveArg1DoNot_1_2_3_4+RelationLevel_Span',
                'arg1SubjectiveArg2DoNot_1_2_3_4+argsubjCorefsubj',
                'hasSubjectWord_RelaAttr',
                'Weare+RelationLevel_Span',

            ]
        elif evaluate_relation == "Comparison":
            manuallySelectKey = [
                "PredictionComparison",
                "PredictionContingency",
                "PredictionExpansion",
                "PredictionTemporal",
                "RelationLevel_Span",
            ]
            notInKey = [
                "arg2NegPure",
                'arg2NegPure+Arg1SubjCoref_Arg2andAttr2Rela',
                'Arg2SubjRepeat_Arg1andAttr1Rela',
                ###################
                ###################
            ]
        elif evaluate_relation == "fourway":
            manuallySelectKey = [
                "FourWayExpansion", "FourWayContingency", "FourWayComparison", "FourWayTemporal",
            ]
            notInKey = [
                "arg2NegPure",
                'arg2NegPure+Arg1SubjCoref_Arg2andAttr2Rela',
                'Arg2SubjRepeat_Arg1andAttr1Rela',
                'Arg1SubjRepeat_Arg2andAttr2Rela',
                'arg1SubjectiveArg2DoNot_1_2_3_4+argsubjCorefsubj',
                'arg1SubjectiveArg2DoNot_1_2_3_4+sent2SubjCorefSent1Attr',
                'arg1SubjectiveArg2DoNot_1_2_3_4+RelationLevel_Span',
                'arg2SubjectiveArg1DoNot_1_2_3_4+argsubjRepeatsubj',
                'arg2SubjectiveArg1DoNot_1_2_3_4+sent1SubjCorefSent2Attr',
                'arg2SubjectiveArg1DoNot_1_2_3_4+RelationLevel_Span',
            ]
        elif evaluate_relation == "Contingency":
            manuallySelectKey = [
                "PredictionComparison", "PredictionContingency", "PredictionExpansion", "PredictionTemporal",
            ]
            notInKey = [
                "arg2NegPure",
                'arg2NegPure+Arg1SubjCoref_Arg2andAttr2Rela',
            ]
        else:
            manuallySelectKey = [
                "PredictionComparison", "PredictionContingency", "PredictionExpansion", "PredictionTemporal",
                "RelationLevel_Span",
                "arg2NegPure+Arg2SubjCoref_Arg1andAttr1Rela", "arg2NegPure+Arg2PrediRepeat_Arg1andAttr1Rela",
                "hasSubjectWord_attr1", "arg1SubjectiveArg2DoNot_1_2_3_4+RelationLevel_Span",
                "extensionNERValue",
            ]
            notInKey = [
                "arg2NegPure",
                'arg2NegPure+Arg1SubjCoref_Arg2andAttr2Rela',
                'Arg2SubjRepeat_Arg1andAttr1Rela',
                'Arg1SubjRepeat_Arg2andAttr2Rela',
                'arg1SubjectiveArg2DoNot_1_2_3_4+argsubjCorefsubj',
                'arg1SubjectiveArg2DoNot_1_2_3_4+sent2SubjCorefSent1Attr',
                'arg1SubjectiveArg2DoNot_1_2_3_4+RelationLevel_Span',
                'arg2SubjectiveArg1DoNot_1_2_3_4+argsubjRepeatsubj',
                'arg2SubjectiveArg1DoNot_1_2_3_4+sent1SubjCorefSent2Attr',
                'arg2SubjectiveArg1DoNot_1_2_3_4+RelationLevel_Span',
                'arg1SubjectiveArg2DoNot_1_2_3_4+argsubjCorefsubj',
                'hasSubjectWord_attr1',
                'hasSubjectWord_RelaAttr',
                'arg2_intension+RelationLevel_Span',
                'Weare+RelationLevel_Span',

            ]
        for i in range(len(key)):
            if (
                    keyOrder[i] in ComparisonFeatures or
                    keyOrder[i] in ContingencyFeatures or
                    keyOrder[i] in ExpansionFeatures or
                    keyOrder[i] in TemporalFeatures or
                    keyOrder[i] in manuallySelectKey
                ):
                if (keyOrder[i] not in notInKey):
                    key_Selected.append(key[i])
                    keyOrder_Selected.append(keyOrder[i])

        if evaluate_relation != "fourway":
            name_relation = "Prediction" + evaluate_relation#Prediction + "Comparison"/"Contingency"/"Expansion"
            if (ins[name_relation] == evaluate_relation):
                key_Selected.append(1)
            else:
                key_Selected.append(0)
            keyOrder_Selected.append(name_relation)

        if(printCount == 0):
            pprint(keyOrder_Selected)
            printCount = 1
        resultString = ""
        for i in range(len(key_Selected)):
            if(key_Selected[i]):
                resultString = resultString + keyOrder_Selected[i] + " "
            else:
                resultString = resultString + "none-" + keyOrder_Selected[i] + " "
        resultString = resultString.strip()
        #print resultString

    return resultString


