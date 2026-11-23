
from pydriller import Repository
from datetime import datetime
from pathlib import Path
from collections import Counter
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

# Flask repository directory
repo_path = Path(__file__).resolve().parent.parent

# Analysis period
since = datetime(2021, 1, 1)
to = datetime(2024, 12, 31, 23, 59, 59)

# Count each commit's changes against its first parent.
# This includes merge commits without counting changes against
# multiple parents.
file_counter = Counter()

print("Extracting file changes...")

for commit in Repository(
    str(repo_path),
    since=since,
    to=to
).traverse_commits():

    if not commit.parents:
        continue

    parent = commit.parents[0]

    result = subprocess.check_output(
        [
            "git", "-C", str(repo_path),
            "diff", "--numstat",
            parent, commit.hash
        ],
        text=True
    )

    for line in result.splitlines():
        parts = line.split("\t")

        if len(parts) == 3:
            file_path = parts[2]
            file_counter[file_path] += 1

# Create DataFrame
df = pd.DataFrame(
    file_counter.items(),
    columns=["file", "change_frequency"]
)

df = df.sort_values(
    "change_frequency",
    ascending=False
)

# Save all file frequencies
df.to_csv(
    repo_path / "analysis" / "file_frequencies.csv",
    index=False
)

print("\nTOP 20 MOST FREQUENTLY CHANGED FILES")
print(df.head(20).to_string(index=False))

# Plot top 20 files
top20 = df.head(20).sort_values("change_frequency")

plt.figure(figsize=(12, 9))

plt.barh(
    top20["file"],
    top20["change_frequency"],
    color="steelblue"
)

plt.xlabel("Number of commits changing the file")
plt.ylabel("File")
plt.title("Top 20 Most Frequently Changed Flask Files (2021–2024)")
plt.tight_layout()

plt.savefig(
    repo_path / "analysis" / "file_frequency.png",
    dpi=300
)

plt.show()

# Find most frequently changed production Python files
production = df[
    df["file"].str.startswith("src/flask/", na=False)
    & df["file"].str.endswith(".py", na=False)
].copy()

production = production.sort_values(
    "change_frequency",
    ascending=False
)

print("\nTOP 10 PRODUCTION PYTHON FILES")
print(production.head(10).to_string(index=False))

# Save production file frequencies
production.to_csv(
    repo_path / "analysis" / "production_file_frequencies.csv",
    index=False
)

print("\nMost frequently changed production Python file:")

if not production.empty:
    print(production.iloc[0].to_string())

print("\nAnalysis completed!")
