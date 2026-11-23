
from pydriller import Repository
from pathlib import Path
import pydriller

repo_path = Path(__file__).resolve().parent.parent
target_hash = "52c060f718e0f07e9d982d2d97973ead0f4d55ca"

print("PyDriller version:", pydriller.__version__)
print("Repository:", repo_path)

for commit in Repository(str(repo_path)).traverse_commits():
    if commit.hash == target_hash:
        print("\nCommit found:", commit.hash)
        print("Message:", commit.msg)
        print("Parents:", commit.parents)
        print("Modified files:", len(commit.modified_files))

        for file in commit.modified_files:
            print(file.new_path, file.change_type)

        break
else:
    print("Commit not found.")