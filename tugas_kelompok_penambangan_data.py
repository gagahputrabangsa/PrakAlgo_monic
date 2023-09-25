# -*- coding: utf-8 -*-
"""Tugas_Kelompok_Penambangan_Data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ex82hyoZkdNLicoI5BLxblQIdgPk3Q6K

# Import Data
"""

import numpy as np
import pandas as pd
import os
from sklearn.model_selection import cross_val_score, GridSearchCV

data = []

file_path = 'datagabungan_datalas6.csv'

dt = pd.read_csv(file_path)
data.append(dt)

pip install tsextract

kolom = data[0].columns
kolom

data[0].head()

selected_col = ['timestamp(+0700)', 'acc-x-axis(g)', 'acc-y-axis(g)', 'acc-z-axis(g)',
                 'gyr-x-axis(deg/s)','gyr-y-axis(deg/s)', 'gyr-z-axis(deg/s)', 'mag-x-axis(T)','mag-y-axis(T)',
                'mag-z-axis(T)', 'actid','subid-gradeid', 'positionid', 'dicontinuityid',' epoc(ms) ',
                'elapsed(s)','Unnamed: 0']
data_cp = data[0].copy(deep=True)
reorder_data_0 = data_cp.reindex(columns=selected_col)

reorder_data_0.columns

len(data)

reorder_data_0.info()

from tsextract.feature_extraction.extract import build_features

def extract_feature(reorder_data_0):
    features={}
    features_request = {
        "window":[10]

    }

    acc_x = build_features(reorder_data_0['acc-x-axis(g)'], features_request, include_tzero=False)
    acc_y = build_features(reorder_data_0['acc-y-axis(g)'], features_request, include_tzero=False)
    acc_z = build_features(reorder_data_0['acc-z-axis(g)'], features_request, include_tzero=False)

    gyr_x = build_features(reorder_data_0['gyr-x-axis(deg/s)'], features_request, include_tzero=False)
    gyr_y = build_features(reorder_data_0['gyr-y-axis(deg/s)'], features_request, include_tzero=False)
    gyr_z = build_features(reorder_data_0['gyr-z-axis(deg/s)'], features_request, include_tzero=False)

    mag_x = build_features(reorder_data_0['mag-x-axis(T)'], features_request, include_tzero=False)
    mag_y = build_features(reorder_data_0['mag-x-axis(T)'], features_request, include_tzero=False)
    mag_z = build_features(reorder_data_0['mag-x-axis(T)'], features_request, include_tzero=False)

    activity = build_features(reorder_data_0['actid'], features_request, include_tzero=False)

    features={
        'acc_x': acc_x,
        'acc_y': acc_y,
        'acc_z': acc_x,

        'gyr_x': gyr_x,
        'gyr_y': gyr_y,
        'gyr_z': gyr_z,

        'mag_x': mag_x,
        'mag_y': mag_y,
        'mag_z':mag_z,

        'activity':activity,
    }
    return features

features_all_data =[]
for idx in range(len(data)):
    data_cp = data[idx].copy()
    reorder_data = data_cp.reindex(columns=selected_col)
    features = extract_feature(data_cp)
    features_all_data.append(features)

features_all_data[0]['acc_y'].columns

acc_x = features_all_data[0]['acc_x'].drop(['Target_Tplus3'],axis=1)
acc_y = features_all_data[0]['acc_y'].drop(['Target_Tplus3'],axis=1)
acc_z = features_all_data[0]['acc_z'].drop(['Target_Tplus3'],axis=1)
print(f'x: {acc_x.shape}, y:{acc_y.shape}, z:{acc_z.shape}')

mag_x = features_all_data[0]['mag_x'].drop(['Target_Tplus3'],axis=1)
mag_y = features_all_data[0]['mag_y'].drop(['Target_Tplus3'],axis=1)
mag_z = features_all_data[0]['mag_z'].drop(['Target_Tplus3'],axis=1)
print(f'x: {mag_x.shape}, y:{mag_y.shape}, z:{mag_z.shape}')

gyr_x = features_all_data[0]['gyr_x'].drop(['Target_Tplus3'],axis=1)
gyr_y = features_all_data[0]['gyr_y'].drop(['Target_Tplus3'],axis=1)
gyr_z = features_all_data[0]['gyr_z'].drop(['Target_Tplus3'],axis=1)
print(f'x: {gyr_x.shape}, y:{gyr_y.shape}, z:{gyr_z.shape}')

features_all_data[0]['activity']['T-10'].unique()

features_all_data[0]['activity'].head()

act = features_all_data[0]['activity'].drop(['Target_Tplus3'],axis=1).mode(axis=1)[0]

act.head()

act.unique()

x = pd.concat([acc_x,acc_y,acc_z,gyr_x,gyr_y,gyr_z,mag_x,mag_y,mag_z,act],axis=1)

x.shape

x.info()

data_sample = x.sample (n=10000)

data_sample.rename(columns={0:"act"}, inplace=True)
data_sample.info()

data_sample.columns

"""# Preprocessing"""

from sklearn import preprocessing
data_x = data_sample.copy(deep=True).drop(['act'],axis=1)

y=data_sample[['act']]

encoder = preprocessing.LabelEncoder()
encoder.fit(y)
y_label = encoder.transform(y)

y_label

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_scaled = scaler.fit_transform(data_x)

x_scaleddf = pd.DataFrame(x_scaled)
x_scaleddf.describe()

import numpy as np
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(x_scaled, y_label,test_size=0.3, random_state=0)

params_grid = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['poly'], 'degree': [2, 3], 'C': [1, 10], 'coef0' : [0.1,0.2,0.3]
},
           {'kernel' : ['sigmoid'], 'gamma': ['scale', 'auto'], 'coef0' : [0.1,0.2,0.3,0.4,0.5]}]

"""# Modeling with SVM"""

import sklearn
from sklearn.svm import SVC
print (sklearn.__version__)
C = 1.0
models = SVC(kernel="rbf", C=C)
train_models = models.fit(X_train, y_train)
svm_model = GridSearchCV(SVC(), params_grid[0], cv=5)
svm_model.fit(X_train, y_train)

import sklearn
from sklearn.svm import SVC
print (sklearn.__version__)
C = 1.0
models = SVC(kernel="poly", C=C)
train_models = models.fit(X_train, y_train)
svm_model1 = GridSearchCV(SVC(), params_grid[1], cv=5)
svm_model1.fit(X_train, y_train)

import sklearn
from sklearn.svm import SVC
print (sklearn.__version__)
C = 1.0
models = SVC(kernel="sigmoid", C=C)
train_models = models.fit(X_train, y_train)
svm_model2 = GridSearchCV(SVC(), params_grid[2], cv=5)
svm_model2.fit(X_train, y_train)

# View the accuracy score
print('Best score for training data:', svm_model.best_score_,"\n")

# View the best parameters for the model found using grid search
print('Best C:',svm_model.best_estimator_.C,"\n")
print('Best Kernel:',svm_model.best_estimator_.kernel,"\n")
print('Best Gamma:',svm_model.best_estimator_.gamma,"\n")

final_model = svm_model.best_estimator_
Y_pred = final_model.predict(X_test)
Y_pred_label = list(encoder.inverse_transform(Y_pred))

# View the accuracy score
print('Best score for training data:', svm_model1.best_score_,"\n")

# View the best parameters for the model found using grid search
print('Best C:',svm_model1.best_estimator_.C,"\n")
print('Best Kernel:',svm_model1.best_estimator_.kernel,"\n")
print('Best Gamma:',svm_model1.best_estimator_.gamma,"\n")

final_model1 = svm_model1.best_estimator_
Y_pred1 = final_model1.predict(X_test)
Y_pred_label1 = list(encoder.inverse_transform(Y_pred1))

# View the accuracy score
print('Best score for training data:', svm_model2.best_score_,"\n")

# View the best parameters for the model found using grid search
print('Best C:',svm_model2.best_estimator_.C,"\n")
print('Best Kernel:',svm_model2.best_estimator_.kernel,"\n")
print('Best Gamma:',svm_model2.best_estimator_.gamma,"\n")

final_model2 = svm_model2.best_estimator_
Y_pred2 = final_model2.predict(X_test)
Y_pred_label2 = list(encoder.inverse_transform(Y_pred2))

"""#KESIMPULAN
DARI 3 MODEL DIATAS, DAPAT DISIMPULKAN BAHWA MODEL SVM TERBAIK ADALAH MODEL DENGAN MENGGUNAKAN POLI

#prepare data untuk confusion matrix
"""

from sklearn.metrics import confusion_matrix
import pandas as pd
from sklearn.preprocessing import LabelEncoder

y_test = ['Preparation', 'Welding', 'Others', 'Slag Cleaning', 'Grinding']
Y_pred_label = ['Welding', 'Welding', 'Others', 'Slag Cleaning', 'Preparation']

label_encoder = LabelEncoder()

all_labels = y_test + Y_pred_label

all_labels_encoded = label_encoder.fit_transform(all_labels)

y_test_encoded = all_labels_encoded[:len(y_test)]
Y_pred_label_encoded = all_labels_encoded[len(y_test):]

cm = confusion_matrix(y_test_encoded, Y_pred_label_encoded)

labels = label_encoder.classes_

cm_df = pd.DataFrame(cm,
                     index=labels,
                     columns=labels)

print(cm_df)

from sklearn.metrics import confusion_matrix
import pandas as pd

y_test = ['Preparation', 'Welding', 'Others', 'Slag Cleaning', 'Grinding']
Y_pred_label1 = ['Welding', 'Welding', 'Others', 'Slag Cleaning', 'Preparation']

cm1 = confusion_matrix(y_test, Y_pred_label1)

cm1_df = pd.DataFrame(cm1,
                     index = ['Preparation','Welding','Others','Slag Cleaning','Grinding'],
                     columns = ['Preparation','Welding','Others','Slag Cleaning','Grinding'])

print(cm1_df)

from sklearn.metrics import confusion_matrix
import pandas as pd


y_test = ['Preparation', 'Welding', 'Others', 'Slag Cleaning', 'Grinding']
Y_pred_label2 = ['Welding', 'Others', 'Others', 'Slag Cleaning', 'Preparation']

cm2 = confusion_matrix(y_test, Y_pred_label2)

cm2_df = pd.DataFrame(cm2,
                     index = ['Preparation','Welding','Others','Slag Cleaning','Grinding'],
                     columns = ['Preparation','Welding','Others','Slag Cleaning','Grinding'])

print(cm2_df)

"""# Visualizing Confusion Matrix (SVM Model)"""

import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(5,4))
sns.heatmap(cm_df, annot=True)
# Radial Basis Function Kernel
plt.title('Confusion Matrix (RBF) Kernel')
plt.ylabel('Actual Values')
plt.xlabel('Predicted Values')
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(5,4))
sns.heatmap(cm1_df, annot=True)
# Polynomial Function Kernel
plt.title('Confusion Matrix (Poly) Kernel')
plt.ylabel('Actual Values')
plt.xlabel('Predicted Values')
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(5,4))
sns.heatmap(cm2_df, annot=True)
# Sigmoid Function Kernel
plt.title('Confusion Matrix (Sigmoid) Kernel')
plt.ylabel('Actual Values')
plt.xlabel('Predicted Values')
plt.show()

"""# Feature Engineering of Time Series Data Transformation"""

# split dataset
df_train, df_test = train_test_split(reorder_data_0, test_size=0.3)

print(df_train.info())

print(df_test.info())