# Lab 1: Grade Evaluator & Archiver

## Description
My Lab 1 contains two tools:

1. **grade-evaluator.py**: reads a `grades.csv` file, validates grades

and weights, calculates the final GPA, determines the PASSED/FAILED status

and indicates which formative assignment(s) to resubmit in case of failure.

2. **organizer.sh**: archives the current `grades.csv` file with a timestamp,

moves it to an `archive/` folder, recreates an empty `grades.csv` file, and

logs the operation in `organizer.log`.

## Format of the grades.csv file

```
Assignment,Category,Weight,Score
Quiz1,Formative,10,85
```

- `Category` must be either `Formative` or `Summative`.

- The `Formative` weights must total **60**.

- The `Summative` weights must total **40**.

- The grand total of all weights must be **100**.

- `Score` must be between **0 and 100**.

## How to run the Python script

Prerequisites: Python 3 installed.

```bash
python3 grade-evaluator.py
```

The script automatically reads `grades.csv` from the current folder and
displays:

- the score obtained per category (Formative / Summative)
- the total weighted grade out of 100
- the GPA (out of 5.0)
- the final status (PASSED or FAILED)
- if FAILED: the formative assignment(s) to resubmit (the highest weighting among the failures, with ties handled)

## How to run the Bash script

Prerequisites: a Bash terminal (Linux, macOS, or Git Bash / WSL on
Windows).

```bash
chmod +x organizer.sh # make the script executable (only once)
./organizer.sh
```

This script will:
1. Create the `archive/` folder if it doesn't already exist.

2. Rename `grades.csv` with a timestamp (e.g., `grades_20260726-193913.csv`).

3. Move this renamed file to `archive/`.

4. Create a new, empty `grades.csv` file, ready for the next batch of grades.

5. Add a line to `organizer.log` with the timestamp and the names of the files involved.

## Author
Rosanne Masugue Ngangoumoun