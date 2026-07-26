"""
grade-evaluator.py is a file that will be used to:
Read grades.csv, validate the data, calculate the GPA, determine the status (PASSED/FAILED), and finally suggest formative assignments to resubmit.

I will work according to the expected CSV format:
Assignment,Category,Weight,Score
Quiz1,Formative,10,85
"""

import csv
import os
import sys

CSV_FILE = "grades.csv"


def read_grades(filename):
    """Let's open and parse the CSV file. Handles missing/empty file cases."""
    if not os.path.exists(filename):
        print(f"Error: file '{filename}' was not found.")
        sys.exit(1)

    records = []
    try:
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    except Exception as e:
        print(f"Error while reading '{filename}': {e}")
        sys.exit(1)

    if not records:
        print(f"Error: file '{filename}' is empty. No grades to process.")
        sys.exit(1)

    return records


def validate_and_clean(records):
    """
    Checks each row (required fields present, numeric values, score
    within 0-100, known category). Returns (clean_rows, error_list).
    Invalid rows are skipped instead of crashing the program.
    """
    clean = []
    errors = []

    for i, row in enumerate(records, start=1):
        name = (row.get("Assignment") or "").strip()
        category = (row.get("Category") or "").strip()
        weight_raw = (row.get("Weight") or "").strip()
        score_raw = (row.get("Score") or "").strip()

        if not name or not category or not weight_raw or not score_raw:
            errors.append(f"Row {i}: missing field(s), row skipped.")
            continue

        try:
            weight = float(weight_raw)
            score = float(score_raw)
        except ValueError:
            errors.append(f"Row {i} ({name}): Weight/Score is not numeric, row skipped.")
            continue

        if category not in ("Formative", "Summative"):
            errors.append(f"Row {i} ({name}): unknown category '{category}', row skipped.")
            continue

        if not (0 <= score <= 100):
            errors.append(f"Row {i} ({name}): score {score} out of range 0-100, row skipped.")
            continue

        clean.append({
            "name": name,
            "category": category,
            "weight": weight,
            "score": score,
        })

    return clean, errors


def validate_weights(clean):
    """Checks that Formative=60, Summative=40, Total=100."""
    formative_total = sum(r["weight"] for r in clean if r["category"] == "Formative")
    summative_total = sum(r["weight"] for r in clean if r["category"] == "Summative")
    total = formative_total + summative_total

    ok = True
    if round(total, 2) != 100:
        print(f"Weight error: total weight is {total}, expected 100.")
        ok = False
    if round(formative_total, 2) != 60:
        print(f"Weight error: Formative total is {formative_total}, expected 60.")
        ok = False
    if round(summative_total, 2) != 40:
        print(f"Weight error: Summative total is {summative_total}, expected 40.")
        ok = False

    return ok, formative_total, summative_total


def compute_category_percentage(clean, category):
    """
    Percentage score obtained in a given category (0-100), independent
    of that category's overall weight in the final grade.
    """
    total_weight = sum(r["weight"] for r in clean if r["category"] == category)
    if total_weight == 0:
        return 0.0
    earned = sum(r["score"] * r["weight"] for r in clean if r["category"] == category)
    return earned / total_weight


def compute_total_grade(clean):
    """Total weighted grade out of 100 (sum of score * weight / 100)."""
    return sum(r["score"] * r["weight"] / 100 for r in clean)


def find_resubmission_candidates(clean):
    failed_formatives = [r for r in clean if r["category"] == "Formative" and r["score"] < 50]
    if not failed_formatives:
        return []

    max_weight = max(r["weight"] for r in failed_formatives)
    return [r for r in failed_formatives if r["weight"] == max_weight]


def main():
    records = read_grades(CSV_FILE)
    clean, errors = validate_and_clean(records)

    if errors:
        print("=== Data issues found ===")
        for e in errors:
            print(" -", e)
        print()

    if not clean:
        print("No valid rows to evaluate. Exiting.")
        sys.exit(1)

    weights_ok, formative_total, summative_total = validate_weights(clean)
    if not weights_ok:
        print("Cannot compute a reliable GPA: weight distribution is invalid.")
        sys.exit(1)

    total_grade = compute_total_grade(clean)
    gpa = (total_grade / 100) * 5.0

    formative_pct = compute_category_percentage(clean, "Formative")
    summative_pct = compute_category_percentage(clean, "Summative")

    status = "PASSED" if formative_pct >= 50 and summative_pct >= 50 else "FAILED"

    print("=== Grade Report ===")
    print(f"Formative score: {formative_pct:.2f}% (total weight {formative_total})")
    print(f"Summative score: {summative_pct:.2f}% (total weight {summative_total})")
    print(f"Total weighted grade: {total_grade:.2f}/100")
    print(f"GPA: {gpa:.2f}/5.0")
    print(f"Final status: {status}")

    if status == "FAILED":
        candidates = find_resubmission_candidates(clean)
        if candidates:
            print("\nFormative assignment(s) eligible for resubmission (highest weight among failures):")
            for c in candidates:
                print(f" - {c['name']} (weight {c['weight']}, score {c['score']})")
        else:
            print("\nNo individual Formative assignment failed, but the overall status is FAILED"
                  " (likely due to the Summative category).")


if __name__ == "__main__":
    main()
