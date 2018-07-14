import argparse


parser = argparse.ArgumentParser(description='Some configurations')

parser.add_argument('-evaluate_relation', type=str, default="fourway", choices=["Comparison", "Contingency", "Expansion", "Temporal", "fourway"],
                    help='specify which relation you want to predict')
parser.add_argument('-train_path', type=str, default="../imBaselineAttr/imTrainCorenlp.Leave1000.Bas.fourway3",
                    help='training data path')
parser.add_argument('-test_path', type=str, default="../imBaselineAttr/imTestCorenlp.splitSubjFeature3",
                    help='testing data path')
parser.add_argument('-log_path', type=str, help='')
parser.add_argument('-confusionM_path', type=str, default="log/", help='')


args = parser.parse_args()