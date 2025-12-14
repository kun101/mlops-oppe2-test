import pandas as pd
from pathlib import Path

df = pd.read_csv("transactions.csv")
df = df.sort_values("Time")

mid = len(df) // 2
v0 = df.iloc[:mid]
v1 = df.iloc[mid:]

Path("data/v0").mkdir(parents=True, exist_ok=True)
Path("data/v1").mkdir(parents=True, exist_ok=True)

v0.to_csv("data/v0/transactions_2022.csv", index=False)
v1.to_csv("data/v1/transactions_2023.csv", index=False)
