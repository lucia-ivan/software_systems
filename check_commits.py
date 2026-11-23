import pandas as pd

df = pd.read_csv("analysis/commit_statistics.csv")

print("Distribution of modified files:")
print(df["modified_files"].value_counts().sort_index())

print("\nSample non-merge commits:")

non_merge = df[
    ~df["message"].str.startswith("Merge", na=False)
]

print(
    non_merge[
        ["hash", "message", "modified_files"]
    ].head(10).to_string(index=False)
)
