
import pandas as pd

# Load the medication dataset
df = pd.read_csv("data/medication_data.csv")

# Display basic information
print("Dataset shape:", df.shape)
print("\nFirst 5 records:")
print(df.head())

print("\nStatus counts:")
print(df["status"].value_counts())

print("\nMissing values:")
print(df.isnull().sum())