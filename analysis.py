import os
import pandas as pd
import matplotlib.pyplot as plt

# The degree sign is: "\u00b0"
# Any names endind in .1 are the integrated gpu

path = "C:/Code/gpu-power-limit-study/data/raw/pl0_trial1.csv"

COLS = {
    "GPU Temperature [\u00b0C]": "temp_c",
    "GPU Clock [MHz]": "clock_mhz",
    "Total Board Power (TBP) [W]": "power_w",
    "GPU Utilization [%]": "util_pct",
}

def summarize_run(path):
    df = pd.read_csv(path, encoding="latin-1")
    small = df[list(COLS.keys())].rename(columns=COLS)
    for name in small.columns:
        small[name] = pd.to_numeric(small[name], errors="coerce")
    small = small.dropna()
    busy = small[small["util_pct"] > 90]
    return {
        "avg_power_w": busy["power_w"].mean(),
        "peak_temp_c": small["temp_c"].max(),
        "avg_clock_mhz": busy["clock_mhz"].mean(),
        "busy_rows": len(busy),
    }

print(summarize_run(path))