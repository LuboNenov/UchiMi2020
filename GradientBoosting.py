import pandas as pd

import sklearn
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn import cross_validation

MalwareDataset = pd.read_csv('MalwareData.csv', sep='|')
Legit = MalwareDataset[0:41323].drop(['legitimate'], axis=1)
Malware = MalwareDataset[41323::].drop(['legitimate'], axis=1)

print('The Number of important features is %i \n' % Legit.shape[1])
Data = MalwareDataset.drop(['Name', 'md5', 'legitimate'], axis=1).values
Target = MalwareDataset['legitimate'].values
FeatSelect = sklearn.ensemble.ExtraTreesClassifier().fit(Data, Target)
Model = SelectFromModel(FeatSelect, prefit=True)
Data_new = Model.transform(Data)

Legit_Train, Legit_Test, Malware_Train, Malware_Test = cross_validation.train_test_split(Data_new, Target ,test_size=0.2)

gbc = sklearn.ensemble.GradientBoostingClassifier(n_estimators=50)
gbc.fit(Legit_Train, Malware_Train)

score = gbc.score(Legit_Test, Malware_Test)
print("The score of Gradient Boosting Classifier is", score*100)

Result = gbc.predict(Legit_Test)
CM = confusion_matrix(Malware_Test, Result)
print("False positive rate : %f %%" % ((CM[0][1] / float(sum(CM[0])))*100))
print('False negative rate : %f %%' % ( (CM[1][0] /float(sum(CM[1]))*100)))