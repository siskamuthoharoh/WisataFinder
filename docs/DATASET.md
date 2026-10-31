# Dokumentasi Dataset WisataFinder

## 1. Gambaran Umum Dataset

WisataFinder menggunakan data destinasi wisata sebagai sumber informasi
utama dalam proses pencarian dan rekomendasi destinasi.

Dalam pengembangannya, proyek ini menggunakan dua dataset pada tahap
yang berbeda. Dataset awal digunakan pada pengembangan versi pertama,
sedangkan dataset nasional digunakan sebagai dataset utama untuk
pengembangan sistem berikutnya.

Kedua dataset tidak langsung digabungkan karena memiliki sumber,
struktur, dan cakupan data yang berbeda.

## 2. Dataset Awal

Dataset awal berasal dari file:

`data/raw/tourism_with_id.csv`

Karakteristik dataset awal:
- Jumlah data: 437 destinasi.
- Jumlah kolom: 13.
- Dataset hasil preprocessing: `data/processed/destinations_clean.csv`.
- Jumlah kolom setelah preprocessing: 14.

Dataset ini digunakan dalam pengembangan awal aplikasi WisataFinder
dan menjadi dasar pembuatan mesin pencari berbasis TF-IDF
dan Cosine Similarity.

Dataset awal tetap dipertahankan sebagai bagian dari riwayat
pengembangan proyek dan pembanding.

## 3. Dataset Nasional

Dataset nasional diperoleh dari Kaggle:

https://www.kaggle.com/datasets/sagitasantia/indonesia-tourism

File sumber:

`data/raw/wisata_indonesia_new.csv`

Karakteristik dataset sumber:
- Jumlah data: 1.025 destinasi.
- Jumlah kolom: 11.

Setelah proses pengolahan, dataset disimpan sebagai:

`data/processed/destinations_nasional.csv`

Dataset hasil pengolahan memiliki:
- Jumlah data: 1.025 destinasi.
- Jumlah kolom: 23.
- Cakupan label provinsi: 37 provinsi.

Dataset nasional digunakan sebagai dataset utama untuk
pengembangan aplikasi WisataFinder versi nasional.

Jumlah provinsi tersebut menunjukkan cakupan data yang tersedia,
bukan klaim bahwa seluruh destinasi wisata Indonesia telah tercakup.

## 4. Struktur Kolom Dataset Nasional

Dataset hasil pengolahan terdiri dari 23 kolom.

| Kolom | Keterangan |
|---|---|
| Place_Id | Identitas destinasi |
| Place_Name | Nama destinasi wisata |
| Description | Deskripsi destinasi |
| Category | Kategori wisata |
| City | Informasi kota atau kabupaten |
| Province | Informasi provinsi |
| Address | Alamat destinasi |
| Price | Informasi harga |
| Rating | Penilaian destinasi |
| Time_Minutes | Perkiraan durasi kunjungan |
| Lat | Koordinat lintang |
| Long | Koordinat bujur |
| Image_URL | Alamat gambar destinasi |
| Location_Label | Label lokasi untuk kebutuhan aplikasi |
| Location_Verification | Status pemeriksaan lokasi |
| Description_Quality | Informasi kualitas deskripsi |
| City_Verification | Informasi pemeriksaan kota |
| Province_Verification | Informasi pemeriksaan provinsi |
| Coordinate_Verification | Informasi pemeriksaan koordinat |
| Source | Informasi sumber data |
| Original_Name | Nama asli dari sumber |
| Original_Image_Path | Referensi lokasi gambar asli |
| search_text | Gabungan teks yang digunakan untuk pencarian |

## 5. Proses Pengolahan Dataset

Dataset nasional melalui proses pemeriksaan dan pengolahan sebelum
digunakan dalam sistem.

Tahapan yang dilakukan meliputi:

1. Memeriksa struktur, jumlah baris, dan jumlah kolom dataset.
2. Memeriksa nilai kosong pada setiap kolom.
3. Memeriksa nama destinasi yang berulang.
4. Memeriksa kelengkapan alamat dan koordinat.
5. Memeriksa kualitas deskripsi destinasi.
6. Memeriksa URL gambar.
7. Memeriksa konsistensi informasi kota dan provinsi.
8. Melakukan koreksi metadata provinsi berdasarkan informasi alamat
   pada data yang diperiksa.
9. Menambahkan informasi pendukung untuk pemeriksaan lokasi.
10. Menyusun kolom search_text untuk mendukung proses pencarian teks.

Nilai yang tidak tersedia tetap dipertahankan sebagai nilai kosong.
Informasi yang tidak memiliki sumber yang dapat dipastikan tidak
dibuat atau diperkirakan secara sembarangan.

## 6. Hasil Audit Kualitas Dataset Nasional

Berdasarkan hasil audit, diperoleh ringkasan berikut:

| Aspek Pemeriksaan | Hasil |
|---|---:|
| Jumlah destinasi | 1.025 |
| Jumlah kolom awal | 11 |
| Nama wisata duplikat | 0 |
| Alamat kosong | 0 |
| Latitude kosong | 0 |
| Longitude kosong | 0 |
| Koordinat di luar rentang | 0 |
| Koordinat unik | 861 |
| Data dengan koordinat berulang | 164 |
| Kota kosong | 18 |
| Deskripsi kosong | 27 |
| Deskripsi tidak informatif | 177 |
| Deskripsi informatif | 821 |
| URL gambar kosong | 0 |
| URL gambar duplikat | 36 |
| URL berformat HTTP/HTTPS | 1.025 |
| Provinsi dikoreksi berdasarkan alamat | 89 |
| Provinsi perlu verifikasi | 1 |

Hasil audit memperlihatkan bahwa dataset sudah memiliki informasi
dasar yang cukup untuk mendukung pengembangan mesin pencari.
Namun, masih terdapat beberapa keterbatasan yang perlu diperhatikan.

## 7. Keterbatasan Dataset

Beberapa keterbatasan yang ditemukan adalah:

1. Sebanyak 18 data belum memiliki informasi kota.
2. Sebanyak 27 data memiliki deskripsi kosong.
3. Sebanyak 177 deskripsi dinilai tidak informatif.
4. Terdapat 164 baris dalam kelompok koordinat yang berulang.
5. Terdapat 36 URL gambar yang berulang.
6. Satu data provinsi masih memerlukan verifikasi lebih lanjut.
7. Kolom Price, Rating, dan Time_Minutes belum memiliki nilai terisi
   dalam dataset nasional yang diperiksa.
8. Jumlah destinasi pada setiap provinsi tidak merata.

Keterbatasan tersebut perlu diperhatikan saat sistem menghasilkan
pencarian dan rekomendasi.

Hasil pencarian akan bergantung pada informasi yang benar-benar tersedia
dalam dataset.

## 8. Penggunaan Dataset dalam Aplikasi

Dataset nasional `destinations_nasional.csv` direncanakan menjadi
sumber data utama untuk:

- Mesin pencari destinasi WisataFinder.
- Penyaringan berdasarkan provinsi.
- Penyaringan berdasarkan kota atau kabupaten.
- Penyaringan berdasarkan kategori wisata.
- Pengembangan rekomendasi melalui WisataBot.

Penggunaan satu dataset utama bertujuan menjaga konsistensi informasi
antara fitur pencarian dan fitur rekomendasi.

Dataset awal tetap disimpan untuk mempertahankan riwayat pengembangan
dan memungkinkan perbandingan dengan versi sebelumnya.

## 9. Lisensi dan Sumber Data

Dataset nasional bersumber dari Kaggle.

Ketentuan lisensi dan izin redistribusi dataset perlu diperiksa
sebelum file mentah maupun hasil pengolahannya dipublikasikan
dalam repository GitHub publik.

Informasi atribusi dan lisensi akan dilengkapi berdasarkan
ketentuan resmi dari pemilik dataset.

## 10. Kesimpulan

Dataset nasional berisi 1.025 destinasi wisata dengan 23 kolom
setelah proses pengolahan.

Dataset ini menjadi dasar pengembangan WisataFinder versi nasional
karena memiliki cakupan wilayah lebih luas dibandingkan dataset awal.

Meskipun demikian, hasil audit menunjukkan masih terdapat data kosong,
deskripsi yang tidak informatif, koordinat berulang, dan metadata
yang perlu diverifikasi.

Oleh karena itu, pemeriksaan kualitas data tetap menjadi bagian
penting dalam pengembangan sistem agar hasil pencarian yang diberikan
kepada pengguna lebih konsisten dan dapat dipertanggungjawabkan.

---

Dokumen pendukung:
- `data/processed/destinations_nasional.csv`
- `data/processed/ringkasan_audit_final.csv`
- `notebooks/pengembangan_dan_evaluasi_algoritma_nasional.ipynb`
