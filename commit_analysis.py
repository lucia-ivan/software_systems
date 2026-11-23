
from pydriller import Repository
from datetime import datetime
from pathlib import Path
import pandas as pd

# Path to the Flask repository
repo_path = Path(__file__).resolve().parent.parent

# Define the analysis period
since = datetime(2021, 1, 1)
to = datetime(2024, 12, 31, 23, 59, 59)

# Extract commits
commits = list(
    Repository(
        str(repo_path),
        since=since,
        to=to
    ).traverse_commits()
)

# Count commits
print("TASK 1 - COMMIT ANALYSIS")
print("=" * 50)
print(f"Total commits: {len(commits)}")

# Count modified files per commit
commit_data = []

for commit in commits:
    commit_data.append({
        "hash": commit.hash,
        "date": commit.committer_date,
        "message": commit.msg.splitlines()[0],
        "author": commit.author.name,
        "modified_files": len(commit.modified_files)
    })

df = pd.DataFrame(commit_data)

# Find commits with the fewest modified files
minimum = df["modified_files"].min()
smallest_commits = df[df["modified_files"] == minimum]

print(f"\nFewest modified files in a commit: {minimum}")
print(f"Number of commits with this minimum: {len(smallest_commits)}")

print("\nCommits with the fewest modified files:")
print("-" * 50)

for _, commit in smallest_commits.iterrows():
    print(f"\nHash: {commit['hash']}")
    print(f"Date: {commit['date']}")
    print(f"Author: {commit['author']}")
    print(f"Message: {commit['message']}")
    print(f"Modified files: {commit['modified_files']}")

# Save results
df.to_csv(
    repo_path / "analysis" / "commit_statistics.csv",
    index=False
)

print("\nResults saved to analysis/commit_statistics.csv")
