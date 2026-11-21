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

all_runs = runs[["power_limit", "trial", "score", "start_temp_c", "avg_power_w", "peak_temp_c", "avg_clock_mhz", "ppw", "busy_rows"]]
all_runs = all_runs.sort_values(["power_limit", "trial"])
all_runs.round(3).to_csv(target_path("data/summary.csv"), index=False)
print(all_runs.round(3))
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

def make_plot(column, title, ylabel, filename):
    plt.figure(figsize=(7, 4.5))
    plt.errorbar(means.index, means[column], yerr=stds[column], fmt="o-", capsize=4)
    plt.title(title)
    plt.xlabel("Power limit (% of stock)")
    plt.ylabel(ylabel)
    plt.xticks(means.index)
    plt.grid(alpha=0.3) # 30% opacity grid lines
    plt.savefig(f"{target_path('plots')}\\{filename}", dpi=200, bbox_inches="tight") # dpi=200 isets the image resolution, bbox_inches="tight" is to cut off unnessesary space arounds the graph
    plt.close()

make_plot("score", "Steel Nomad score vs. GPU power limit", "Steel Nomad score (points)", "score_vs_power_limit.png")
make_plot("ppw", "Performance per watt vs. GPU power limit", "Performance per watt (points / W)", "ppw_vs_power_limit.png")
make_plot("peak_temp_c", "Peak GPU temperature vs. GPU power limit (fan fixed at 100%)", "Peak GPU temperature (\u00b0C)", "peak_temp_vs_power_limit.png")