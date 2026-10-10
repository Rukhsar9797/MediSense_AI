
import pandas as pd

from src.adherence import calculate_adherence
from src.risk_engine import calculate_risk
from src.ai_advisor import generate_report, get_recommendations

DOSE_FILE = "data/medication_data_with_dates.csv"
PROFILE_FILE = "data/patient_profiles.csv"

print("\n=== 1. Loading datasets ===")

doses_df = pd.read_csv(DOSE_FILE)
profiles_df = pd.read_csv(PROFILE_FILE)

print("Dose records:", len(doses_df))
print("Patient profiles:", len(profiles_df))
print("Sample IDs:", profiles_df["patient_id"].head().tolist())

# Validate columns
required_dose_columns = {
    "patient_id", "medication_name", "dose",
    "prescribed_time", "actual_time", "status", "scheduled_date"
}

assert required_dose_columns.issubset(doses_df.columns), (
    f"Missing dose columns: {required_dose_columns - set(doses_df.columns)}"
)

assert "patient_id" in profiles_df.columns
assert profiles_df["patient_id"].is_unique

dose_ids = set(doses_df["patient_id"].dropna().astype(str))
profile_ids = set(profiles_df["patient_id"].dropna().astype(str))

assert dose_ids == profile_ids, (
    f"IDs only in doses: {dose_ids - profile_ids}\n"
    f"IDs only in profiles: {profile_ids - dose_ids}"
)

print("Dataset columns and patient IDs: PASS")
print("\nStatus counts:")
print(doses_df["status"].value_counts(dropna=False))

print("\n=== 2. Testing adherence ===")

patient_id = "p101"

patient_doses = doses_df[
    doses_df["patient_id"].astype(str) == patient_id
]

assert not patient_doses.empty, f"{patient_id} not found in dose dataset"

stats = calculate_adherence(doses_df, patient_id=patient_id)

print("Patient:", patient_id)
print("Adherence output:", stats)

print("\n=== 3. Testing risk engine ===")

risk = calculate_risk(doses_df, patient_id=patient_id)

print("Risk output:", risk)

print("\n=== 4. Testing AI report ===")

report = generate_report(stats, risk)
print("AI report:")
print(report)

print("\n=== 5. Testing AI recommendations ===")

recommendations = get_recommendations(
    question="Suggest simple ways to build a consistent medication-taking routine.",
    adherence_summary=stats,
)

print("Recommendations:")
print(recommendations)

print("\n=== ALL BACKEND TESTS COMPLETED ===")
