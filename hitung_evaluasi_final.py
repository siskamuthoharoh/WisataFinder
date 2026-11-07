
import pandas as pd
from pathlib import Path

# File kandidat asli, tidak akan diubah
source = Path("data/processed/kandidat_evaluasi_nasional_v1.csv")

df = pd.read_csv(
    source,
    sep=None,
    engine="python",
    encoding="utf-8-sig"
)

df.columns = df.columns.str.strip()
df["Rank"] = pd.to_numeric(df["Rank"], errors="coerce")
df["_query"] = df["Query"].astype(str).str.strip().str.casefold()

# Label berdasarkan penilaian yang telah kita sepakati
aturan = {
    "museum di jakarta": ["1"] * 10,
    "pantai di bali": ["1"] * 10,
    "wisata alam di jawa tengah": ["1"] * 10,
    "taman di jawa barat": ["1", "1", "1", "0", "1", "1", "0", "1"],
    "candi di daerah istimewa yogyakarta": ["1"] * 10,
    "wisata keluarga di jakarta": [
        "1", "1", "1", "1", "1", "1", "1", "U", "0", "1"
    ],
    "wisata sejarah di banten": ["1", "1", "U", "0", "0", "0", "0"],
    "wisata murah di jawa tengah": ["U"] * 10
}

# Pasangkan label berdasarkan query dan rank
label_map = {}

for query, labels in aturan.items():
    subset = df[df["_query"] == query].sort_values("Rank")

    expected_ranks = list(range(1, len(labels) + 1))
    actual_ranks = subset["Rank"].tolist()

    if actual_ranks != expected_ranks:
        raise ValueError(
            f"Rank untuk query '{query}' tidak sesuai. "
            f"Ditemukan: {actual_ranks}"
        )

    for rank, label in enumerate(labels, start=1):
        label_map[(query, rank)] = label

df["Relevan"] = [
    label_map.get((q, int(r)), "")
    for q, r in zip(df["_query"], df["Rank"])
]

if (df["Relevan"] == "").any():
    raise ValueError("Ada kandidat yang belum mendapatkan label.")

# Hitung evaluasi per query
hasil = []

for query, grup in df.groupby("Query", sort=False):
    grup = grup.sort_values("Rank")

    baris = {
        "Query": query,
        "Jumlah_1": (grup["Relevan"] == "1").sum(),
        "Jumlah_0": (grup["Relevan"] == "0").sum(),
        "Jumlah_U": (grup["Relevan"] == "U").sum()
    }

    for k in [5, 10]:
        top = grup.head(k)
        dinilai = top[top["Relevan"].isin(["1", "0"])]

        jumlah_relevan = (dinilai["Relevan"] == "1").sum()

        precision = (
            jumlah_relevan / len(dinilai)
            if len(dinilai) > 0
            else float("nan")
        )

        baris[f"Precision@{k}"] = precision

    hasil.append(baris)

ringkasan = pd.DataFrame(hasil)

# Ringkasan keseluruhan
print("\n===== DISTRIBUSI LABEL =====")
print(df["Relevan"].value_counts().to_string())

print("\n===== HASIL PER QUERY =====")
print(ringkasan.to_string(index=False))

for k in [5, 10]:
    rata = ringkasan[f"Precision@{k}"].mean()
    print(f"\nRata-rata Precision@{k}: {rata * 100:.2f}%")

# Simpan dua file hasil
folder = Path("data/processed")
df.drop(columns=["_query"]).to_csv(
    folder / "kandidat_evaluasi_nasional_final_berlabel.csv",
    index=False,
    encoding="utf-8-sig"
)

ringkasan.to_csv(
    folder / "hasil_evaluasi_precision_final.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nFile final berhasil dibuat.")
