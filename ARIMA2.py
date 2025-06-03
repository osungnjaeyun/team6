#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import pmdarima as pm
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import (mean_absolute_error,
                             mean_squared_error,
                             mean_absolute_percentage_error)


# In[2]:


df = pd.read_csv("C:/Users/USER/Desktop/종설/firebase_log.csv", parse_dates=["Time"])
df = (df.dropna())

df['Temperature'] = df["Temperature"].interpolate()
df.loc[df['Temperature'] < 25,'Temperature'] = 25
df.loc[df['Temperature'] > 32,'Temperature'] = 32
df['moving_average'] = df['Temperature'].rolling(window=1000).mean()
temp = df['moving_average'][1000:].copy()

# ➋ Train/Test (뒤 30 %)
split = int(len(temp)*0.7)
train, test = temp.iloc[:split], temp.iloc[split:]

model = pm.auto_arima (train, start_p=5,  max_p=5, d = 1, seasonal = False, trace = True)
model.fit(train)

temp_predict = model.predict(n_periods=len(test)) 

# 그래프
fig, axes = plt.subplots(1, 1, figsize=(12, 4))
plt.plot(train, label='Train')        # 훈련 데이터
plt.plot(test, label='Test')          # 테스트 데이터
plt.plot(temp_predict, label='Prediction')  # 예측 데이터
plt.legend()
plt.show()


# In[3]:


df = pd.read_csv("C:/Users/USER/Desktop/종설/firebase_log.csv", parse_dates=["Time"])
df = (df.dropna())

df['Temperature'] = df["Temperature"].interpolate()
df.loc[df['Temperature'] < 25,'Temperature'] = 25
df.loc[df['Temperature'] > 32,'Temperature'] = 32
df['moving_average'] = df['Temperature'].rolling(window=1000).mean()
temp = df['moving_average'][1000:].copy()

# ➋ Train/Test (뒤 30 %)
split = int(len(temp)*0.7)
train, test = temp.iloc[:split], temp.iloc[split:]

model = ARIMA(train, order=(5,1,2))
model_fit = model.fit()

n_test = len(test)
temp_predict = model_fit.forecast(steps=n_test)

# 그래프
fig, axes = plt.subplots(1, 1, figsize=(12, 4))
plt.plot(train, label='Train')        # 훈련 데이터
plt.plot(test, label='Test')          # 테스트 데이터
plt.plot(temp_predict, label='Prediction')  # 예측 데이터
plt.legend()
plt.show()


# In[ ]:




