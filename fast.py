# Bring in lightweight dependencies
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import tensorflow as tf
app = FastAPI()

class ScoringItem(BaseModel): 
    Age: float
    Gender: str
    Location: str
    Subscription_Length_Months: float
    Monthly_Bill: float
    Total_Charges: float #/ 1, // Float value 
    Total_Usage_GB: float #0.01, // Float value 
    Years: int
    Month: int 
    random: int#4.0 // Ordinal 1,2,3,4,5

with open('model.pkl', 'rb') as f: 
    model = pickle.load(f)

@app.post('/')
async def scoring_endpoint(item:ScoringItem):
    df = pd.DataFrame([item.dict().values()], columns=item.dict().keys())
    le=LabelEncoder()
    x=df.values
    x[:,1]=le.fit_transform(x[:,1])
    ct=ColumnTransformer(transformers=[('encoder',OneHotEncoder(),[1])],remainder='passthrough')
    x=np.array(ct.fit_transform(x))
    x[:,2]=le.fit_transform(x[:,2])
    print(x)
    x= np.asarray(x).astype(np.float32)
    tens=tf.convert_to_tensor(x, dtype=None)
    yhat = model.predict(x)
    return {"prediction":int(yhat)}