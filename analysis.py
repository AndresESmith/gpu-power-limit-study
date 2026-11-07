import os
import pandas as pd
import matplotlib.pyplot as plt

# The degree sign is: "\u00b0"
# Any names endind in .1 are the integrated gpu

script_dir = os.path.dirname(os.path.abspath(__file__))
def target_path(path):
    return os.path.join(script_dir, path)

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

results = pd.read_csv(target_path("data/results.csv"))
rows = []

for i, row in results.iterrows():
    pl = int(row["power_limit"])
    trial = int(row["trial"])
    
    if pl == 0:
        tag = "pl0"
    else:
        tag = f"pl{pl:+d}" # Gives a positive number a plus sign, otherwise +10 would just be 10

    run = summarize_run(target_path(f"data/raw/{tag}_trial{trial}.csv"))
    run["power_limit"] = pl
    run["trial"] = trial
    run["score"] = row["score"]
    run["start_temp_c"] = row["start_temp_c"]
    rows.append(run)

runs = pd.DataFrame(rows)
runs["ppw"] = runs["score"] / runs["avg_power_w"] # Get performance per watt (ppw)
print(len(runs))
print(runs)

cols = ["score", "avg_power_w", "ppw", "peak_temp_c", "avg_clock_mhz"]
means = runs.groupby("power_limit")[cols].mean()
stds = runs.groupby("power_limit")[cols].std()
pct_change = (means - means.loc[0]) / means.loc[0] * 100
print(means.round(2))
print(stds.round(2))
print(pct_change.round(2))
means.round(3).to_csv(target_path("data/summary_means.csv"))
stds.round(3).to_csv(target_path("data/summary_stds.csv"))
pct_change.round(3).to_csv(target_path("data/summary_pct_change.csv"))