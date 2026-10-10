
import pandas as pd


def calculate_adherence(
    df: pd.DataFrame,
    patient_id=None,
    selected_date=None,
) -> dict:
    """Calculate overall or patient-specific medication adherence."""

    required_columns = {
        "patient_id",
        "scheduled_date",
        "status",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    data = df.copy()
    data["status"] = (
        data["status"].fillna("").astype(str).str.strip().str.lower()
    )
    data["scheduled_date"] = pd.to_datetime(
        data["scheduled_date"], errors="coerce"
    ).dt.date

    # Filter for one patient, if requested.
    if patient_id is not None:
        data = data[
            data["patient_id"].astype(str) == str(patient_id)
        ]

    # Filter for one scheduled date, if requested.
    if selected_date is not None:
        selected_date = pd.to_datetime(selected_date).date()
        data = data[data["scheduled_date"] == selected_date]

    taken = int((data["status"] == "taken").sum())
    missed = int((data["status"] == "missed").sum())
    pending = int((data["status"] == "pending").sum())

    # Pending doses aren't included until their status is resolved.
    doses_due = taken + missed
    percentage = (
        round(taken / doses_due * 100, 2)
        if doses_due > 0 else 0.0
    )

    return {
        "patient_id": patient_id,
        "selected_date": str(selected_date) if selected_date else "all dates",
        "total_records": len(data),
        "taken": taken,
        "missed": missed,
        "pending": pending,
        "doses_due": doses_due,
        "adherence_percentage": percentage,
    }