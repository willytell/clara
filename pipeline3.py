"""
This pipeline3.py uses as input
   1. original image files
   2. shifted and labeled mask files, (preprocessed by pipeline1.py and pipeline2.py respectively).
   3. tcia_diagnosis.xls, which contains the diagnosis of some nodules.

Using 1., 2. and 3. this code calculate the features extraction with the PyRadiomic package and save them
in an excel file.

https://drive.google.com/open?id=1UGpoQyLhae2KpVrn2mkni-gRBBzYJNZA
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC


######################## Input #########################################
databasePath = '/home/willytell/Desktop'
ctPath = 'LungCTDataBase/LIDC-IDRI/Nii_Vol/CT_nii'
ctmaskPath = 'output/pipeline2/CTlabeledshiftedmask_nii'
filename = '/home/willytell/Desktop/tcia_diagnosis.xls'
sheet_name = 'NoduleMalignancy'
paramPath = os.path.join('config', 'Params.yaml')
########################################################################

######################## Output ########################################
outputPath = '/home/willytell/Desktop/output/pipeline2'
extracted_features = os.path.join(outputPath, 'features.xlsx')
########################################################################


print("Start.")

df = pd.read_excel('extractedFeatures.xlsx')
df2 = df[df.columns[4:]]
X = df2.values
df3 = df[df.columns[3]]
y = df3.values
clf = SVC(gamma='auto')
param_dist = dict(C=[1.0, 0.6, 0.7, 0.8, 0.9], gamma=['auto', 'scale', 0.3, 0.5], kernel=['rbf', 'linear', 'poly', 'sigmoid'])
rand = RandomizedSearchCV(clf, param_dist, cv=3, scoring='accuracy', n_iter=2, random_state=5, n_jobs=7)
rand.fit(X,y)


print("Finish.")