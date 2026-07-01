# modules/subject_analysis.py

import pandas as pd


def assign_subject_status(average):
    """Classifies a subject's health based on class average."""
    if average >= 75:
        return "🟢 Good"
    elif average >= 55:
        return "🟡 Average"
    else:
        return "🔴 Needs Attention"


def analyse_subjects(df, marks_cols):
    """
    Accepts the clean DataFrame and marks column names.
    Returns a tuple: (subject summary DataFrame, insights dict)
    """

    rows = []

    for subject in marks_cols:
        col = df[subject]

        average     = round(col.mean(), 2)
        highest     = int(col.max())
        lowest      = int(col.min())
        pass_count  = int((col >= 40).sum())
        fail_count  = int((col < 40).sum())
        pass_rate   = round((pass_count / len(col)) * 100, 2)
        status      = assign_subject_status(average)

        rows.append({
            "subject":     subject.replace("_", " ").title(),
            "average":     average,
            "highest":     highest,
            "lowest":      lowest,
            "pass_count":  pass_count,
            "fail_count":  fail_count,
            "pass_rate":   pass_rate,
            "status":      status
        })

    subject_df = pd.DataFrame(rows).sort_values("average", ascending=False)
    subject_df = subject_df.reset_index(drop=True)

    # ── Insights ──────────────────────────────────────────────────────────────
    best_subject  = subject_df.loc[subject_df["average"].idxmax(), "subject"]
    worst_subject = subject_df.loc[subject_df["average"].idxmin(), "subject"]
    best_avg      = subject_df["average"].max()
    worst_avg     = subject_df["average"].min()

    insights = {
        "best_subject":  best_subject,
        "worst_subject": worst_subject,
        "best_avg":      best_avg,
        "worst_avg":     worst_avg,
        "needs_attention": list(
            subject_df[subject_df["pass_rate"] < 50]["subject"]
        )
    }

    return subject_df, insights