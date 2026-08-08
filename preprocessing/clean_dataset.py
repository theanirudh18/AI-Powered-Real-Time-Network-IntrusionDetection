import numpy as np
import pandas as pd
from pathlib import Path

INPUT_FILE = Path("dataset/interim/merged_dataset.csv")
OUTPUT_FILE = Path("dataset/interim/clean_dataset.csv")

print("Loading dataset...")
df = pd.read_csv(INPUT_FILE, low_memory=False)

print(f"\nOriginal Shape : {df.shape}")

# Remove spaces from column names
df.columns = df.columns.str.strip()

# Remove duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# Replace Infinity values
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Remove rows containing NaN
missing_before = df.isna().sum().sum()
df.dropna(inplace=True)

print("\nCleaning Summary")
print("-" * 40)
print(f"Duplicates Removed : {duplicates}")
print(f"Missing Values     : {missing_before}")
print(f"Final Shape        : {df.shape}")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nClean dataset saved to:\n{OUTPUT_FILE}")