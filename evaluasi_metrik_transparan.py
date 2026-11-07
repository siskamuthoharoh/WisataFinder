
import pandas as pd
from pathlib import Path

folder = Path("data/processed")

file_kandidat = folder / "kandidat_evaluasi_nasional_final_berlabel.csv"
file_gt = folder / "ground_truth_kandidat_v1_dinilai.csv"

def baca(path):
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    df = pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
    df.columns = df.columns.astype(str).str.strip()
    return df

def norm(x):
    return " ".join(str(x).strip().casefold().split())

kandidat = baca(file_kandidat)
gt = baca(file_gt)

kandidat["Relevan"] = kandidat["Relevan"].astype(str).str.strip().str.upper()
gt["GT_Relevan"] = gt["GT_Relevan"].astype(str).str.strip().str.upper()

kandidat["Rank"] = pd.to_numeric(kandidat["Rank"], errors="raise")

hasil = []

for query, grup in kandidat.groupby("Query", sort=False):
    q = norm(query)

    # Query murah dikecualikan: semua kandidat belum dapat dinilai.
    if q == "wisata murah di jawa tengah":
        continue

    pool = gt[gt["Query_GroundTruth"].apply(norm) == q]
    if pool.empty:
        raise ValueError(f"Ground Truth tidak ditemukan: {query}")

    jumlah_gt = (pool["GT_Relevan"] == "1").sum()
    if jumlah_gt == 0:
        raise ValueError(f"Ground Truth relevan kosong: {query}")

    grup = grup.sort_values("Rank")
    baris = {"Query": query, "GT_relevan": int(jumlah_gt)}

    for k in [5, 10]:
        top = grup.head(k)
        tp = int((top["Relevan"] == "1").sum())
        dinilai = int(top["Relevan"].isin(["1", "0"]).sum())
        jumlah_dikembalikan = len(top)

        # Precision hanya pada hasil yang labelnya 1 atau 0
        p_dinilai = tp / dinilai if dinilai else float("nan")

        # Precision konservatif: pembagi tetap K.
        # Label U dan posisi hasil yang tidak tersedia tidak dihitung relevan.
        p_konservatif = tp / k

        # Recall terhadap kumpulan pooled Ground Truth
        recall = tp / jumlah_gt

        f1_dinilai = (
            2 * p_dinilai * recall / (p_dinilai + recall)
            if pd.notna(p_dinilai) and p_dinilai + recall > 0
            else float("nan")
        )

        f1_konservatif = (
            2 * p_konservatif * recall / (p_konservatif + recall)
            if p_konservatif + recall > 0
            else 0
        )

        baris[f"TP@{k}"] = tp
        baris[f"Hasil_dikembalikan@{k}"] = jumlah_dikembalikan
        baris[f"Hasil_dinilai@{k}"] = dinilai
        baris[f"U@{k}"] = int((top["Relevan"] == "U").sum())
        baris[f"Cakupan_penilaian@{k}"] = (
            dinilai / jumlah_dikembalikan
            if jumlah_dikembalikan else float("nan")
        )
        baris[f"Precision_dinilai@{k}"] = p_dinilai
        baris[f"Precision_konservatif@{k}"] = p_konservatif
        baris[f"Recall_pooled@{k}"] = recall
        baris[f"F1_dinilai@{k}"] = f1_dinilai
        baris[f"F1_konservatif@{k}"] = f1_konservatif

    hasil.append(baris)

per_query = pd.DataFrame(hasil)

print("\n===== HASIL PER QUERY =====")
print(per_query.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

print("\n===== RATA-RATA MACRO =====")
for k in [5, 10]:
    print(f"\n@{k}")
    for nama, kolom in [
        ("Precision pada hasil dinilai", f"Precision_dinilai@{k}"),
        ("Precision konservatif", f"Precision_konservatif@{k}"),
        ("Recall pooled", f"Recall_pooled@{k}"),
        ("F1 pada hasil dinilai", f"F1_dinilai@{k}"),
        ("F1 konservatif", f"F1_konservatif@{k}"),
        ("Cakupan penilaian", f"Cakupan_penilaian@{k}")
    ]:
        print(f"{nama}: {per_query[kolom].mean() * 100:.2f}%")

print("\n===== RINGKASAN MICRO =====")
for k in [5, 10]:
    tp = per_query[f"TP@{k}"].sum()
    dinilai = per_query[f"Hasil_dinilai@{k}"].sum()
    dikembalikan = per_query[f"Hasil_dikembalikan@{k}"].sum()
    jumlah_query = len(per_query)
    total_gt = per_query["GT_relevan"].sum()

    p_dinilai = tp / dinilai if dinilai else float("nan")
    p_konservatif = tp / (k * jumlah_query)
    recall = tp / total_gt

    f1_dinilai = (
        2 * p_dinilai * recall / (p_dinilai + recall)
        if pd.notna(p_dinilai) and p_dinilai + recall > 0
        else float("nan")
    )
    f1_konservatif = (
        2 * p_konservatif * recall / (p_konservatif + recall)
        if p_konservatif + recall > 0
        else 0
    )

    print(f"\n@{k}")
    print(f"Precision pada hasil dinilai: {p_dinilai * 100:.2f}%")
    print(f"Precision konservatif: {p_konservatif * 100:.2f}%")
    print(f"Recall pooled: {recall * 100:.2f}%")
    print(f"F1 pada hasil dinilai: {f1_dinilai * 100:.2f}%")
    print(f"F1 konservatif: {f1_konservatif * 100:.2f}%")
    print(
        "Cakupan penilaian hasil yang dikembalikan:",
        f"{dinilai / dikembalikan * 100:.2f}%"
        if dikembalikan else "Tidak tersedia"
    )

per_query.to_csv(
    folder / "evaluasi_metrik_transparan_per_query.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nFile tersimpan:")
print(folder / "evaluasi_metrik_transparan_per_query.csv")
