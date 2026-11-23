
from pydriller import Repository
from datetime import datetime
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Repository path
repo_path = Path(__file__).resolve().parent.parent

# Analysis period
since = datetime(2021, 1, 1)
to = datetime(2024, 12, 31, 23, 59, 59)

# File selected from Task 2
target_file = "src/flask/app.py"

observations = []

print(f"Analyzing LOC for {target_file}...")

for commit in Repository(
    str(repo_path),
    since=since,
    to=to
).traverse_commits():

    # PyDriller does not report modifications for merge commits
    # in its default merge handling.
    if len(commit.parents) > 1:
        continue

    for modified_file in commit.modified_files:

        if modified_file.new_path == target_file:
            if modified_file.nloc is not None:
                observations.append({
                    "date": commit.committer_date,
                    "nloc": modified_file.nloc,
                    "commit": commit.hash
                })

# Create DataFrame
df = pd.DataFrame(observations)

if df.empty:
    print("No observations found.")
    raise SystemExit

# Extract year and month
df["month"] = pd.to_datetime(df["date"], utc=True).dt.tz_localize(None).dt.to_period("M")

# Calculate average LOC for each month
monthly_avg = (
    df.groupby("month")
    .agg(
        average_loc=("nloc", "mean"),
        modifications=("nloc", "count")
    )
    .reset_index()
)

# Display results
print("\nMONTHLY AVERAGE LOC")
print(monthly_avg.to_string(index=False))

# Save monthly results
monthly_avg.to_csv(
    repo_path / "analysis" / "monthly_loc.csv",
    index=False
)

# Plot only months with modifications
plt.figure(figsize=(15, 7))

plt.bar(
    monthly_avg["month"].astype(str),
    monthly_avg["average_loc"],
    color="steelblue"
)

plt.xlabel("Month")
plt.ylabel("Average number of lines of code (nloc)")
plt.title("Monthly Average LOC of src/flask/app.py (2021–2024)")

plt.xticks(rotation=90)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    repo_path / "analysis" / "monthly_loc.png",
    dpi=300
)

plt.show()

print("\nNumber of observations:", len(df))
print("Results saved to analysis/monthly_loc.csv")
print("Plot saved to analysis/monthly_loc.png")
