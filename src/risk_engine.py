
import pandas as pd


def calculate_risk(df, patient_id, as_of_date=None):
    """
    Calculate a transparent, rule-based adherence risk summary for one patient.

    Rules:
    - Analyze the seven calendar days ending on as_of_date.
    - 'taken' and 'delayed' count as completed doses.
    - 'missed' counts as a missed dose.
    - 'pending' is excluded from the resolved-dose denominator.
    - Generate an alert when more than one dose is missed on a day.

    This is a demo adherence indicator, not a clinical prediction.
    """

    required_columns = {"patient_id", "scheduled_date", "status"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    # Normalize IDs and statuses to avoid case-sensitive mismatches.
    data = df.copy()
    data["patient_id"] = data["patient_id"].astype(str).str.strip().str.lower()
    data["status"] = data["status"].astype(str).str.strip().str.lower()
    data["scheduled_date"] = pd.to_datetime(
        data["scheduled_date"], errors="coerce"
    ).dt.normalize()

    patient_id = str(patient_id).strip().lower()
    data = data[data["patient_id"] == patient_id].copy()
    data = data.dropna(subset=["scheduled_date"])

    if data.empty:
        raise ValueError(f"No valid dose records found for patient {patient_id!r}.")

    # Default to the latest date in this patient's dataset, which makes
    # historical/demo datasets testable without depending on today's date.
    if as_of_date is None:
        end_date = data["scheduled_date"].max()
    else:
        end_date = pd.to_datetime(as_of_date, errors="raise").normalize()

    start_date = end_date - pd.Timedelta(days=6)

    period = data[
        data["scheduled_date"].between(start_date, end_date, inclusive="both")
    ].copy()

    if period.empty:
        return {
            "patient_id": patient_id,
            "period_start": start_date.strftime("%Y-%m-%d"),
            "period_end": end_date.strftime("%Y-%m-%d"),
            "score": 0,
            "level": "insufficient data",
            "taken": 0,
            "delayed": 0,
            "missed": 0,
            "pending": 0,
            "doses_due": 0,
            "missed_rate": 0.0,
            "daily_missed_counts": {},
            "alerts": ["No dose records found in the selected seven-day period."],
            "reasons": ["Insufficient data to calculate an adherence indicator."],
        }

    counts = period["status"].value_counts()

    taken = int(counts.get("taken", 0))
    delayed = int(counts.get("delayed", 0))
    missed = int(counts.get("missed", 0))
    pending = int(counts.get("pending", 0))

    # Resolved doses exclude pending records.
    doses_due = taken + delayed + missed
    missed_rate = missed / doses_due if doses_due else 0.0

    # Rule-based score: missed-dose rate plus repeated misses in one day.
    score = round(missed_rate * 100)

    daily_missed = (
        period.loc[period["status"] == "missed"]
        .groupby("scheduled_date")
        .size()
    )

    daily_missed_counts = {
        date.strftime("%Y-%m-%d"): int(count)
        for date, count in daily_missed.items()
    }

    multiple_miss_days = {
        date: count
        for date, count in daily_missed_counts.items()
        if count > 1
    }

    # Add a transparent penalty for days with multiple missed doses.
    # Keep score bounded from 0 to 100.
    score = min(100, score + 15 * len(multiple_miss_days))

    if doses_due == 0:
        level = "insufficient data"
    elif score >= 75:
        level = "very high"
    elif score >= 50:
        level = "high"
    elif score >= 25:
        level = "moderate"
    else:
        level = "low"

    alerts = []
    for date, count in sorted(multiple_miss_days.items()):
        alerts.append(
            f"Multiple-missed-dose alert: {count} doses marked missed on {date}."
        )

    if missed > 0:
        alerts.append(
            f"{missed} missed dose(s) recorded in the seven-day period."
        )

    if not alerts:
        alerts.append("No missed-dose alerts triggered in this period.")

    reasons = [
        f"{missed} missed dose(s) out of {doses_due} resolved dose(s) "
        "in the last seven days.",
        f"Missed-dose rate: {missed_rate * 100:.1f}%.",
        f"{delayed} delayed dose(s) counted as completed.",
        f"{pending} pending dose(s) excluded from the resolved-dose rate.",
        (
            f"{len(multiple_miss_days)} day(s) had more than one missed dose."
        ),
    ]

    return {
        "patient_id": patient_id,
        "period_start": start_date.strftime("%Y-%m-%d"),
        "period_end": end_date.strftime("%Y-%m-%d"),
        "score": score,
        "level": level,
        "taken": taken,
        "delayed": delayed,
        "missed": missed,
        "pending": pending,
        "doses_due": doses_due,
        "missed_rate": round(missed_rate * 100, 2),
        "daily_missed_counts": daily_missed_counts,
        "alerts": alerts,
        "reasons": reasons,
    }
