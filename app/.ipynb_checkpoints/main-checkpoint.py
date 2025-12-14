from fastapi import FastAPI
import joblib
import numpy as np

model = joblib.load("model.joblib")
app = FastAPI()

@app.post("/predict")
def predict(features: dict):
    X = np.array(list(features.values())).reshape(1, -1)
    prob = model.predict_proba(X)[0][1]
    pred = int(prob > 0.5)
    return {"prediction": pred, "probability": prob}
