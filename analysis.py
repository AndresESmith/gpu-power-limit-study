import os
import pandas as pd
import matplotlib.pyplot as plt
import time

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

results = pd.read_csv("C:/Code/gpu-power-limit-study/data/results.csv")
rows = []

for i, row in results.iterrows():
    pl = int(row["power_limit"])
    trial = int(row["trial"])
    
    if pl == 0:
        tag = "pl0"
    else:
        tag = f"pl{pl:+d}" # Gives a positive number a plus sign, otherwise +10 would just be 10

    run = summarize_run(f"C:/Code/gpu-power-limit-study/data/raw/{tag}_trial{trial}.csv")
    run["power_limit"] = f"{pl:+d}" if pl != 0 else f"{pl:d}"
    run["trial"] = trial
    run["score"] = row["score"]
    run["start_temp_c"] = row["start_temp_c"]
    rows.append(run)

runs = pd.DataFrame(rows)
runs["ppw"] = runs["score"] / runs["avg_power_w"] # Get performance per watt (ppw)
print(len(runs))
print(runs)