import pandas as pd
import matplotlib.pyplot as plt

# The degree sign is: "\u00b0"
# Any names endind in .1 are the integrated gpu

path = "C:/Code/gpu-power-limit-study/data/raw/test.csv"
df = pd.read_csv(path, encoding="latin-1")
print(df.shape)

for c in df.columns:
    if c.startswith(("GPU Temperature", "GPU Clock [", "GPU Utilization", "Total Board Power (TBP) [W]")): # GPU Clock has a bracker so it doesn't read 
        print(c, "|", df[c].iloc[-1])

COLS = {
    "GPU Temperature [\u00b0C]": "temp_c",
    "GPU Clock [MHz]": "clock_mhz",
    "Total Board Power (TBP) [W]": "power_w",
    "GPU Utilization [%]": "util_pct",
}
small = df[list(COLS.keys())].copy()
small = small.rename(columns=COLS)
print(small.dtypes)
for name in small.columns:
    small[name] = pd.to_numeric(small[name], errors="coerce")
small = small.dropna()
print(small.dtypes)
print(small.shape)
print(small.describe().round(2))