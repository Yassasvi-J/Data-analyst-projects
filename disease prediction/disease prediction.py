# -*- coding: utf-8 -*-
"""Day 28.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eQaySirLoDLmb1Dn24WHyRGXwX5JTRc9

# **Helllo  its daya 28 today we have  task of Diabetes, Hypertension and Stroke Prediction useing differnt machine learning **
"""

##import libraries 
import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.express as px
import scipy
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import catboost
import xgboost
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,f1_score
import warnings
warnings.filterwarnings('ignore')

##read data  and  drop null values 
d_d=pd.read_csv("diabetes_data.csv").dropna()
s_d=pd.read_csv("stroke_data.csv").dropna()
h_d=pd.read_csv("hypertension_data.csv").dropna()

d_d.info()

s_d.info()

h_d.info()

d_d.describe()

s_d.describe()

h_d.describe()

d_d.hist(figsize=(20,15))
plt.show()

s_d.hist(figsize=(20,15))
plt.show()

h_d.hist(figsize=(20,15))

## cheaking corelation with heatmap 

plt.figure(figsize=(30, 8))

plt.subplot(1, 3, 1)
sns.heatmap(d_d.corr(), annot=True, cmap='Greys')
plt.title('Correlation Plot (Original DS)')

plt.subplot(1, 3, 2)
sns.heatmap(d_d.corr(), annot=True, cmap='Oranges')
plt.title('Correlation Plot (Train DS)')

plt.subplot(1, 3, 3)
sns.heatmap(d_d.corr(), annot=True, cmap='Greens')
plt.title('Correlation Plot (Test DS)')
plt.show()

## define a model 
def model_evaluate(model,model_name,data,p_col):
    x,y=data.drop(columns=[p_col]),data[p_col]
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
    ss=StandardScaler()
    x_train_s=ss.fit(x_train)
    x_test_s=ss.fit(x_test)
    print(f"\n-------------------{model_name}----------------------")
    model.fit(x_train,y_train)
    y_pred=model.predict(x_test)
    print(f"accuracy_score_for {model_name}:{accuracy_score(y_test,y_pred)}",)
    print(f"f1_score_for {model_name}:{f1_score(y_test,y_pred,average='weighted')}",)
    print("----------------------------------------------------------\n")
    return accuracy_score(y_test,y_pred),f1_score(y_test,y_pred,average='weighted')

"""**Useing Diabetes data**"""

##here we find 
models = {
    "RandomForestClassifier": RandomForestClassifier(random_state=42,),
    "DecisionTreeClassifier": DecisionTreeClassifier(random_state=42),
    "SVC": SVC(random_state=42),
    "CatBoostClassifier": catboost.CatBoostClassifier(random_state=42, verbose=False,),
    "KNeighborsClassifier": KNeighborsClassifier(),
    "Logistic_Regression": LogisticRegression(),
    "xgboost":xgboost.XGBClassifier(),
}


result_dict=[]
for model_name,model in models.items():
    score,f1=model_evaluate(model,model_name,d_d,'Diabetes')
    result_dict.append({'model':model_name,'accuracy_score':score,'f1_score':f1,'dataset':'diabetis'})

"""**Useing stroke Data**"""

for model_name,model in models.items():
  score,f1=model_evaluate(model,model_name,s_d,'stroke')
  result_dict.append({'model':model_name,'accuracy_score':score,'f1_score':f1,'dataset':'stroke'})

"""Useing Hypertenson Data"""

for model_name,model in models.items():
  score,f1=model_evaluate(model,model_name,h_d,'target')
  result_dict.append({'model':model_name,'accuracy_score':score,'f1_score':f1,'dataset':'hypertenson'})

"""## **Evaluate Results **"""

result_data=pd.DataFrame(result_dict)
diabetes_data=result_data[result_data['dataset']=='diabetis'].reset_index().drop('index',axis=1)
stroke_results=result_data[result_data['dataset']=='stroke'].reset_index().drop('index',axis=1)
hypertension_result=result_data[result_data['dataset']=='hypertenson'].reset_index().drop('index',axis=1)
display(result_data.sort_values(by='f1_score',ascending=True))

plt.figure(figsize=(15,6))
sns.barplot(data=result_data,x='model',y='accuracy_score',hue='dataset')
plt.show()

plt.figure(figsize=(15,7))
sns.pointplot(data=result_data, x="model", y="f1_score", hue="dataset", dodge=True)
plt.show()

fig = px.line(result_data, x="model", y="accuracy_score", color="dataset")
fig.update_traces(textposition="bottom right")
fig.show()

"""# Thanks for reading till the end ! If you liked the EDA, Model Training, Model Evaluation and Comparison,Predtictions
# pls do Upvote👍 and give some remarks/advice if you feels some things need to be added 
"""