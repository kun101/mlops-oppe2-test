import mlflow
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import joblib

mlflow.set_tracking_uri("http://136.116.2.17:5000/")
mlflow.set_experiment("fraud-detection")

df = pd.read_csv("data/v0/transactions_2022.csv")

X = df.drop(columns=["Class"])
y = df["Class"]

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, val_idx = next(split.split(X, y))

X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

model = LogisticRegression(class_weight="balanced", max_iter=1000)

with mlflow.start_run():
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    f1 = f1_score(y_val, preds)

    mlflow.log_metric("f1_score", f1)
    mlflow.sklearn.log_model(model, "model")

    joblib.dump(model, "model.joblib")
