import shap
import pandas as pd
import joblib
import mlflow

df = pd.read_csv("data/v0/transactions_2022.csv")
df["location"] = ["A" if i % 2 == 0 else "B" for i in range(len(df))]

X = df.drop(columns=["Class"])
model = joblib.load("model.joblib")

explainer = shap.Explainer(model, X)
shap_values = explainer(X)

shap.summary_plot(shap_values, X, show=False)
