
import pandas as pd
from src.adherence import calculate_adherence

df = pd.read_csv("data/medication_data_with_dates.csv")

patient_id = str(df["patient_id"].dropna().iloc[0])
selected_date = df["scheduled_date"].iloc[0]

# One patient, one date
daily_stats = calculate_adherence(
    df,
    patient_id=patient_id,
    selected_date=selected_date,
)

print("Individual patient daily adherence:")
for key, value in daily_stats.items():
    print(f"{key}: {value}")

# Same patient's complete available history
overall_stats = calculate_adherence(df, patient_id=patient_id)

print("\nIndividual patient overall adherence:")
print(overall_stats["adherence_percentage"], "%")

assert 0 <= daily_stats["adherence_percentage"] <= 100
print("\nAdherence tests passed!")