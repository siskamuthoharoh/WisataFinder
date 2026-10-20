
from pathlib import Path
import pandas as pd

# Menentukan lokasi folder proyek
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "tourism_with_id.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "destinations_clean.csv"


def preprocess_data():
    """Membersihkan dataset destinasi wisata."""

    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {RAW_PATH}"
        )

    df = pd.read_csv(RAW_PATH)

    print("Ukuran data awal:", df.shape)

    # Menghapus kolom tambahan yang tidak diperlukan
    extra_columns = [
        col for col in df.columns
        if col.startswith("Unnamed:")
    ]
    df = df.drop(columns=extra_columns, errors="ignore")

    # Memastikan kolom penting tersedia
    required_columns = [
        "Place_Id",
        "Place_Name",
        "Description",
        "Category",
        "City",
        "Price",
        "Rating",
        "Time_Minutes",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Kolom wajib tidak ditemukan: {missing_columns}"
        )

    # Menghapus baris yang kehilangan informasi utama
    text_columns = [
        "Place_Name",
        "Description",
        "Category",
        "City",
    ]

    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()

    df = df.dropna(subset=required_columns[:5])

    for col in text_columns:
        df = df[df[col].ne("")]

    # Menghapus ID duplikat jika ada
    df = df.drop_duplicates(subset=["Place_Id"])

    # Membentuk teks gabungan untuk mesin pencari
    df["search_text"] = (
        df["Place_Name"] + " "
        + df["Category"] + " "
        + df["City"] + " "
        + df["Description"]
    )

    # Menyimpan hasil yang telah dibersihkan
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nPreprocessing berhasil!")
    print("Ukuran data akhir:", df.shape)
    print("Kolom yang dihapus:", extra_columns)
    print("Jumlah Time_Minutes kosong:", df["Time_Minutes"].isna().sum())
    print("Jumlah ID duplikat:", df["Place_Id"].duplicated().sum())
    print("Lokasi hasil:", OUTPUT_PATH)

    return df


if __name__ == "__main__":
    preprocess_data()
