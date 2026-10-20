
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw" / "tourism_with_id.csv"

df = pd.read_csv(DATA)

print("=== NILAI UNIK KOLOM TAMBAHAN ===")

for col in ["Unnamed: 11", "Unnamed: 12", "Time_Minutes"]:
    if col in df.columns:
        print(f"\nKolom: {col}")
        print("Jumlah nilai kosong:", df[col].isna().sum())
        print("Jumlah nilai unik:", df[col].nunique(dropna=True))
        print("Contoh nilai:", df[col].dropna().unique()[:10])

print("\n=== JUMLAH DESTINASI PER KOTA ===")
print(df["City"].value_counts().to_string())

print("\n=== KATEGORI WISATA ===")
print(df["Category"].value_counts().to_string())

print("\n=== DISTRIBUSI RATING ===")
print(df["Rating"].describe().to_string())
