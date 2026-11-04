import pandas as pd
import matplotlib.pyplot as plt

path = "C:/Code/gpu-power-limit-study/data/raw/test.csv"
df = pd.read_csv(path, encoding="latin-1")
print(df.shape)

for c in df.columns:
    if c.startswith(("GPU Temperature", "GPU Clock [", "GPU Utilization", "Total Board Power (TBP) [W]")): # GPU Clock has a bracker so it doesn't read 
        print(c, "|", df[c].iloc[-1])