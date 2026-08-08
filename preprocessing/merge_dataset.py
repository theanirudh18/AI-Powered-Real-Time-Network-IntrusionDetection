from pathlib import Path
import pandas as pd

RAW_DIR = Path("dataset/raw")
OUTPUT_DIR = Path("dataset/interim")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

csv_files = sorted(RAW_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV files found in dataset/raw")

print(f"Found {len(csv_files)} CSV files\n")

dfs = []

for file in csv_files:
    print(f"Reading: {file.name}")
    df = pd.read_csv(file, low_memory=False)
    print(f"Shape: {df.shape}\n")
    dfs.append(df)

merged_df = pd.concat(dfs, ignore_index=True)

output_file = OUTPUT_DIR / "merged_dataset.csv"
merged_df.to_csv(output_file, index=False)

print("=" * 50)
print("Merge Completed Successfully")
print("=" * 50)
print(f"Final Shape: {merged_df.shape}")
print(f"Saved to: {output_file}")

if "Label" in merged_df.columns:
    print("\nClass Distribution:\n")
    print(merged_df["Label"].value_counts())