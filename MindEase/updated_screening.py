# -*- coding: utf-8 -*-
"""screening.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j3GhxcXvDNs1syL4Xe5u5vDSt0Z58P4z
"""

from google.colab import drive
drive.mount('/content/drive')

import os
Root = "/content/drive/MyDrive/ML"
os.chdir(Root)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
data = pd.read_csv("/content/drive/MyDrive/ML/survey.csv")
data.head()

data.shape

data.info()

data['Country'].value_counts().plot(kind='bar',figsize=(10,8))

data.drop(['Country','state','Timestamp','comments'],axis=1,inplace=True)

data.isnull().sum()

data['self_employed'].value_counts()

data['self_employed'].fillna('No',inplace=True)

data['work_interfere'].value_counts()

data['work_interfere'].fillna('N/A',inplace=True)

data['Age'].value_counts().plot(kind='bar',figsize=(10,8))

data.drop(data[(data['Age']>60) | (data['Age'] < 18)].index,inplace=True)

data['Gender'].value_counts().plot(kind='bar',figsize=(10,8))

data['Gender'].replace(['Male','male','M','m','Male ','Cis Male','Man','cis male','Mail','Male (CIS)','Male-ish','maile','Cis Man','male','Malr','Mal','Make','msle'],'Male',inplace=True)

data['Gender'].value_counts().plot(kind='bar',figsize=(10,8))

data['Gender'].replace(['Female','female','F','f','Women','Woman','woman','Female ','Female (cis)','cis-female/femme','femail','women','Femake','Cis Female'],'Female',inplace=True)

data['Gender'].value_counts().plot(kind='bar',figsize=(10,8))

data['Gender'].replace(['Female (trans)','Androgyne','queer','Neuter','Trans woman','male leaning androgynous','Guy (-ish) ^_^','Agender','Genderqueer','fluid','Enby','Nah','non-binary','queer/she/they','something kinda male?','Trans-female','ostensibly male, unsure what that really means'],'Non-Binary',inplace=True)

data['Gender'].value_counts().plot(kind='bar',figsize=(10,8))

sb.displot(data["Age"])
plt.title("Distribution - Age")
plt.xlabel("Age")

data.describe(include='all')

data.info()

x = data.drop('treatment',axis = 1)
y = data['treatment']

from sklearn. compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

x = data.drop('treatment',axis = 1)
y = data['treatment']

ct = ColumnTransformer([('oe',OrdinalEncoder(),['Gender','self_employed','family_history','work_interfere','no_employees','remote_work','tech_company','benefits','care_options','wellness_program','seek_help','anonymity','leave','mental_health_consequence','phys_health_consequence','coworkers','supervisor','mental_health_interview','phys_health_interview','mental_vs_physical','obs_consequence'])])

x = ct.fit_transform(x)

le = LabelEncoder()
y = le.fit_transform(y)

import joblib
joblib.dump(ct,'feature_values')

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.3,random_state=49)

X_train.shape,X_test.shape,y_train.shape,y_test.shape

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import accuracy_score,roc_curve, confusion_matrix, classification_report,auc

model_dict = {}

model_dict['Logistic regression'] = LogisticRegression(solver='liblinear',random_state=49)
model_dict['KNN Classifier'] = KNeighborsClassifier()
model_dict['Decision Tree Classifier'] = DecisionTreeClassifier(random_state=49)
model_dict['Random Forest Classifier'] = RandomForestClassifier(random_state=49)
model_dict['AdaBoost Classifier'] = AdaBoostClassifier(random_state=49)
model_dict['Gradient Boosting Classifier'] = GradientBoostingClassifier(random_state=49)
model_dict['XGB Classifier'] = XGBClassifier(random_state=49)

def model_test(X_train,X_test,y_train,y_test,model,model_name):
  model.fit(X_train,y_train)
  y_pred = model.predict(X_test)
  accuracy = accuracy_score(y_test,y_pred)
  print("=============================={}==============================".format(model_name))
  print('score is : {}'.format(accuracy))
  print()

for model_name,model in model_dict.items():
  model_test(X_train,X_test,y_train,y_test,model,model_name)

abc = AdaBoostClassifier(random_state=99)
abc.fit(X_train,y_train)
pred_abc = abc.predict(X_test)
print('Accuracy of AdaBoost=',accuracy_score(y_test,pred_abc))

from sklearn.model_selection import RandomizedSearchCV
params_abc = {'n_estimators': [int(x) for x in np.linspace(start = 1,stop = 50, num =15)],
              'learning_rate':[(0.97 + x / 100) for x in range(0,8)],
              }
abc_random = RandomizedSearchCV(random_state=49,estimator=abc,param_distributions = params_abc,n_iter = 50,cv=5,n_jobs=-1)

params_abc

abc_random.fit(X_train,y_train)

abc_random.best_params_

abc_tuned = AdaBoostClassifier(random_state = 49,n_estimators=11,learning_rate=1.0)
abc_tuned.fit(X_train,y_train)
pred_abc_tuned = abc_tuned.predict(X_test)
print('Accuracy of Adaboost(tuned)=',accuracy_score(y_test,pred_abc_tuned))

cf_matrix = confusion_matrix(y_test,pred_abc)
sb.heatmap(cf_matrix/np.sum(cf_matrix),annot=True,fmt='.2%')
plt.title('Confusion Matrix of AdaBoost Classifier')
plt.xlabel('Predicted')
plt.ylabel('Actual')

from sklearn import metrics
fpr_abc, tpr_abc, thresholds_abc = roc_curve(y_test,pred_abc)
roc_auc_abc = metrics.auc(fpr_abc,tpr_abc)
plt.plot(fpr_abc,tpr_abc,color='orange',label='ROC curve (area = %0.2f)'%roc_auc_abc)
plt.plot([0,1],[0,1],color='blue',linestyle='--')
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.0])
plt.title('ROC_Curve')
plt.xlabel('False Positive Rate (1 - specifity)')
plt.ylabel('True Positive Rate (sensitivity)')
plt.legend(loc="lower right")
plt.show()
roc_curve(y_test,pred_abc)

fpr_abc_tuned, tpr_abc_tuned,thresholds_abc_tuned = roc_curve(y_test,pred_abc_tuned)
roc_auc_abc_tuned = metrics.auc(fpr_abc_tuned,tpr_abc_tuned)
plt.plot(fpr_abc_tuned,tpr_abc_tuned,color='orange',label='ROC curve(area = %0.2f)' % roc_auc_abc_tuned)
plt.plot([0,1],[0,1],color='blue',linestyle='--')
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.0])
plt.title('ROC Curve')
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.legend(loc='lower right')
plt.show()
roc_curve(y_test,pred_abc_tuned)

print(classification_report(y_test,pred_abc))

print(classification_report(y_test,pred_abc_tuned))

import pickle
pickle.dump(abc_tuned,open('model.pkl','wb'))

with open('model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)
print(loaded_model)

user_screening_score = loaded_model.predict_proba(x)[:, 1]
print(f"User Screening Score: {user_screening_score}")