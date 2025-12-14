import pandas as pd
import numpy as np

df = pd.read_csv("data/v0/transactions_2022.csv")

def poison(p):
    poisoned = df.copy()
    idx = poisoned[poisoned["Class"] == 0].sample(frac=p, random_state=42).index
    poisoned.loc[idx, "Class"] = 1
    poisoned.to_csv(f"data/v0/poisoned_{int(p*100)}.csv", index=False)

for p in [0.02, 0.08, 0.20]:
    poison(p)
