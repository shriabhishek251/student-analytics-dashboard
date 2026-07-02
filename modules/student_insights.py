# modules/student_insights.py

import pandas as pd


def get_toppers(summary, n=3):
    """
    Returns the top N students by percentage.
    summary: the student summary DataFrame from compute_metrics()
    n: number of toppers to return (default 3)
    """
    toppers = summary.nlargest(n, "percentage").copy()
    toppers = toppers.reset_index(drop=True)
    toppers.index += 1  # Start rank display from 1 not 0
    return toppers


def get_at_risk_students(summary, df_clean, marks_cols, threshold=50):
    """
    Identifies at-risk students using two signals:
    1. Overall percentage below threshold
    2. Failed 2 or more individual subjects (mark < 40)

    Returns a DataFrame of at-risk students with a reason column.
    """
    at_risk_records = []

    for _, row in summary.iterrows():
        reasons = []

        # ── Signal 1: Overall percentage below threshold ───────────────────
        if row["percentage"] < threshold:
            reasons.append(f"Overall {row['percentage']}% (below {threshold}%)")

        # ── Signal 2: Failed 2 or more subjects individually ──────────────
        student_row = df_clean[df_clean.index == row.name]

        if not student_row.empty:
            subject_marks = student_row[marks_cols].iloc[0]
            failed_subjects = [
                subj.replace("_", " ").title()
                for subj in marks_cols
                if subject_marks[subj] < 40
            ]
            if len(failed_subjects) >= 2:
                reasons.append(
                    f"Failed {len(failed_subjects)} subjects: "
                    f"{', '.join(failed_subjects)}"
                )

        # ── Add to list only if at least one signal triggered ─────────────
        if reasons:
            at_risk_records.append({
                "name":       row.get("name", f"Student {row.name}"),
                "percentage": row["percentage"],
                "grade":      row["grade"],
                "status":     row["status"],
                "rank":       row["rank"],
                "reason":     " | ".join(reasons)
            })

    if not at_risk_records:
        return pd.DataFrame()  # Empty DataFrame — no at-risk students

    at_risk_df = pd.DataFrame(at_risk_records)
    at_risk_df = at_risk_df.sort_values("percentage").reset_index(drop=True)
    return at_risk_df