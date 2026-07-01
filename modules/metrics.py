# modules/metrics.py

import pandas as pd


def assign_grade(percentage):
    """Maps a percentage to a letter grade."""
    if percentage >= 90:
        return "A"
    elif percentage >= 75:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


def compute_metrics(df, marks_cols):
    """
    Accepts the clean DataFrame and list of marks column names.
    Returns a tuple: (summary DataFrame, class stats dict)
    """

    # ── Step 1: Build the summary DataFrame ──────────────────────────────────
    # Start fresh — don't modify the clean df
    summary = df.copy()

    # ── Step 2: Total marks per student ──────────────────────────────────────
    summary["total"] = summary[marks_cols].sum(axis=1)

    # ── Step 3: Maximum possible marks ───────────────────────────────────────
    max_possible = len(marks_cols) * 100

    # ── Step 4: Percentage ────────────────────────────────────────────────────
    summary["percentage"] = (summary["total"] / max_possible * 100).round(2)

    # ── Step 5: Grade ─────────────────────────────────────────────────────────
    summary["grade"] = summary["percentage"].apply(assign_grade)

    # ── Step 6: Pass / Fail ───────────────────────────────────────────────────
    summary["status"] = summary["percentage"].apply(
        lambda p: "Pass" if p >= 40 else "Fail"
    )

    # ── Step 7: Rank (1 = highest percentage) ────────────────────────────────
    summary["rank"] = summary["percentage"].rank(
        ascending=False, method="min"
    ).astype(int)

    # ── Step 8: Sort by rank ──────────────────────────────────────────────────
    summary = summary.sort_values("rank").reset_index(drop=True)

    # ── Step 9: Class-level stats ─────────────────────────────────────────────
    total_students = len(summary)
    passed = (summary["status"] == "Pass").sum()
    failed = total_students - passed

    class_stats = {
        "total_students": total_students,
        "class_average": round(summary["percentage"].mean(), 2),
        "highest_score": summary["percentage"].max(),
        "lowest_score": summary["percentage"].min(),
        "passed": int(passed),
        "failed": int(failed),
        "pass_rate": round((passed / total_students) * 100, 2),
        "grade_distribution": summary["grade"].value_counts().to_dict()
    }

    return summary, class_stats