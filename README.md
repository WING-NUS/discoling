# Project Title

Code for the AAAI paper: Linguistic Properties Matter for Implicit Discourse Relation Recognition: Combining Semantic Interaction, Topic Continuity and Attribution.

### Prerequisites

Note that the code use python2.

```
sklearn
nltk
```

## Getting Started

You may first need to configure the training data path: -train_path and testing data path: -test_path before you run this code.
Here is an example: python autoNLP.py -evaluate_relation [the discourse relation you want to predict] -train_path [path/to/your/training/data] -test_path [path/to/your/testing/data] -log_path [path/to/save/logs] -confusionM_path [path/to/save/confusion/matrix]


## Results

For example, if you do fourway prediction, you will see a output like this:

First you will see the features used by this prediction.
['FourWayExpansion',
 'FourWayContingency',
 'FourWayComparison',
 'FourWayTemporal',
 'arg1NegPure+Arg1SubjRepeat_Arg2andAttr2Rela',
....
]

Next the output will show the most informative features. The most efficient features are displayed in reverse order.
-----------------------Most informative Features---------------------
Most Informative Features
none-arg2NegPure+Arg2PrediRepeat_Arg1andAttr1Rela = None           Compar : Tempor =     16.6 : 1.0
arg2NegPure+Arg2PrediRepeat_Arg1andAttr1Rela = 1              Compar : Tempor =     16.6 : 1.0

Final you will see the prediction result:
P: 0.548148, R: 0.542125, F: 0.545120
P, R, F represent precision, recall and F1 score respectively.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

