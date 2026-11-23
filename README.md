
# Software Evolution I assignment

## Project Description

This project investigates the evolution of the Flask
Python framework using its Git history.

The analysis covers January 1, 2021 to December 31, 2024.

## Analysis Tasks

### Task 1 – Commit Analysis
Script: `commit_analysis.py`

Analyses the number of commits, modified files,
and commits with the fewest modified files.

### Task 2 – File Change Frequency
Script: `file_frequency.py`

Identifies frequently modified files and generates
a visualization of file change frequencies.

### Task 3 – Monthly Lines of Code
Script: `monthly_loc.py`

Investigates the monthly evolution of Lines of Code
for the selected production Python file.

## Requirements

- Python 3
- Git
- Dependencies listed in `requirements.txt`: pydriller, pandas, and matplotlib


## Installation

Clone the Flask repository:

```bash
git clone https://github.com/pallets/flask.git
cd flask
git checkout 49943b5a94413a530761350f04e896f76e8d620e
```

Install the analysis dependencies:

```bash
pip install -r requirements.txt
```

## Running the Analysis

Run the following scripts:

```bash
python3 commit_analysis.py
python3 file_frequency.py
python3 monthly_loc.py
```

## Output

The analysis produces CSV files, text results,
and visualizations for the three tasks.
