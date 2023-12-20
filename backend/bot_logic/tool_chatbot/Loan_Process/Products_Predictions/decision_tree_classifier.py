#!/usr/bin/env python
# coding: utf-8

# In[19]:

import json
import os

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

# In[20]:


products = pd.read_csv(
    r"C:\Users\adina\Desktop\תקיית_עבודות\chatbot-shira-fe-fixes\backend\bot_logic\CL-programs.csv",
    sep=',')
# Lower The inputs
products['Employee_Status'] = products['Employee_Status'].str.lower()

# In[21]:

# data preprocessing 

X = products.iloc[:, 1:]
y = products.iloc[:, 0:1].values

# In[22]:


X = X.drop(columns=['APY Rate', 'Notes'])


# In[23]:


def convert_to_duration_numeric(value):
    value = value.split(' ')
    return int(value[0])


def convert_to_loan_amount_numeric(value):
    value = value.split('$')[1].split(',')
    return int(''.join(value))


# In[24]:


X['Duration'] = X['Duration'].apply(convert_to_duration_numeric)
X['Loan Amount'] = X['Loan Amount'].apply(convert_to_loan_amount_numeric)

# In[25]:


ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), ['Employee_Status'])],
                       remainder='passthrough')

# In[26]:


import numpy as np

X_transformed = np.array(ct.fit_transform(X))

# In[27]:


X_transformed

# In[28]:


new_df = pd.DataFrame(X_transformed, columns=['', 'Employee_Status', 'Duration', 'Loan Amount',
                                              'Down_payment', 'Annual_income'])

# In[30]:


new_df = new_df.drop(columns=[''])

# In[32]:


# Feature scaling
sc = StandardScaler()
new_df.iloc[:, 1:] = sc.fit_transform(new_df.iloc[:, 1:])

# In[33]:


new_df

# In[36]:


X = new_df.values

# In[34]:


from sklearn.tree import DecisionTreeClassifier

# In[35]:


classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)

# In[37]:


classifier.fit(X, y)

# In[39]:


# Prediction 
prediction = {
    'Employee_Status': 'Employed',
    'Duration': 20,
    'Loan Amount': 12000,
    'Down_payment': 1500,
    'Annual_income': 45000
}

prediction_df = pd.DataFrame([prediction])
prediction_df['Employee_Status'] = prediction_df['Employee_Status'].str.lower()
# data preprocess
prediction_after_ct = ct.transform(prediction_df)
prediction_after_ct = prediction_after_ct[:, 1:]
prediction = pd.DataFrame(prediction_after_ct,
                          columns=['Employee_Status', 'Duration', 'Loan Amount', 'Down_payment', 'Annual_income'])
prediction.iloc[:, 1:] = sc.transform(prediction.iloc[:, 1:])

# In[40]:


prediction

# In[41]:


y_prediction = np.array(prediction)

# In[42]:


prediction_from_model = classifier.predict(y_prediction)

# In[43]:


print(prediction_from_model)

# In[ ]:
joblib.dump(classifier, 'decision_tree_classifier.joblib')
joblib.dump(sc, 'sc.pkl')
joblib.dump(ct, 'ct.pkl')

current_directory = os.path.abspath(os.getcwd())

classifier_path = os.path.join(current_directory, 'decision_tree_classifier.joblib')
sc_path = os.path.join(current_directory, 'sc.pkl')
ct_path = os.path.join(current_directory, 'ct.pkl')

print("Classifier path:", classifier_path)
print("Scaler path:", sc_path)
print("ColumnTransformer path:", ct_path)

print('Model saved successfully.')
