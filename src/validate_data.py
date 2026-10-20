
from pathlib import Path

import pandas as pd


# Lokasi proyek dan dataset
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "tourism_with_id.csv"


def main():
    print("=" * 60)
    print("WISATAFINDER - VALIDASI DATASET")
    print("=" * 60)

    # Memastikan file tersedia
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {DATA_PATH}"
        )

    # Membaca dataset asli
    df = pd.read_csv(DATA_PATH)

    print(f"\nLokasi dataset : {DATA_PATH}")
    print(f"Jumlah baris   : {df.shape[0]}")
    print(f"Jumlah kolom   : {df.shape[1]}")

    print("\n--- DAFTAR KOLOM ---")
    print(df.columns.tolist())

    print("\n--- TIPE DATA ---")
    print(df.dtypes.to_string())

    print("\n--- DATA KOSONG PER KOLOM ---")
    print(df.isna().sum().to_string())

    print("\n--- JUMLAH BARIS DUPLIKAT ---")
    print(df.duplicated().sum())

    # Pemeriksaan kolom penting
    required_columns = [
        "Place_Name",
        "Description",
        "Category",
        "City",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    print("\n--- PEMERIKSAAN KOLOM WAJIB ---")
    if missing_columns:
        print(f"Kolom tidak ditemukan: {missing_columns}")
    else:
        print("Semua kolom wajib tersedia.")

    # Memeriksa nama destinasi kosong
    if "Place_Name" in df.columns:
        empty_names = (
            df["Place_Name"]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )
        print(f"Nama destinasi kosong: {empty_names}")

    # Memeriksa deskripsi kosong
    if "Description" in df.columns:
        empty_descriptions = (
            df["Description"]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )
        print(f"Deskripsi kosong: {empty_descriptions}")

    # Melihat beberapa contoh data
    print("\n--- 5 DATA PERTAMA ---")
    print(df.head().to_string(index=False))

    # Menyimpan laporan validasi
    report_dir = PROJECT_ROOT / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / "validasi_dataset.txt"

    with report_path.open("w", encoding="utf-8") as file:
        file.write("WISATAFINDER - LAPORAN VALIDASI DATASET\n")
        file.write("=" * 50 + "\n")
        file.write(f"Jumlah baris: {df.shape[0]}\n")
        file.write(f"Jumlah kolom: {df.shape[1]}\n")
        file.write(f"Baris duplikat: {df.duplicated().sum()}\n")
        file.write(
            f"Kolom kosong:\n{df.isna().sum().to_string()}\n"
        )
        file.write(
            f"\nKolom dataset:\n{df.columns.tolist()}\n"
        )

    print(f"\nLaporan tersimpan di: {report_path}")
    print("\nValidasi selesai.")


if __name__ == "__main__":
    main()
