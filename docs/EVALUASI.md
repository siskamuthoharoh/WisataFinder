# Evaluasi Sistem WisataFinder

## 1. Tujuan Evaluasi

Evaluasi dilakukan untuk mengetahui kemampuan algoritma pencarian WisataFinder
dalam menghasilkan destinasi yang relevan berdasarkan kata kunci, kategori,
dan lokasi yang diminta pengguna.

Evaluasi juga dilakukan untuk mengukur konsistensi penyaringan lokasi dan
memeriksa kualitas dataset nasional yang digunakan oleh sistem.

## 2. Evaluasi Relevansi Pencarian V7

Pengujian relevansi dilakukan menggunakan delapan kueri pencarian.
Sebanyak 56 hasil pencarian dinilai secara manual berdasarkan kesesuaiannya
dengan kebutuhan pencarian.

Hasil evaluasi:

| Kueri | Jumlah Hasil | Jumlah Relevan | Precision@10 |
|---|---:|---:|---:|
| Gunung dan wisata alam | 10 | 10 | 100% |
| Kebun binatang di Jakarta | 1 | 1 | 10% |
| Museum | 10 | 10 | 100% |
| Museum di Bandung | 4 | 4 | 40% |
| Museum di Semarang | 1 | 1 | 10% |
| Pantai di Bali | 10 | 10 | 100% |
| Tempat wisata di Bali | 10 | 10 | 100% |
| Wisata budaya di Jawa Tengah | 10 | 10 | 100% |
| **Rata-rata** | | | **70%** |

### Interpretasi

Rata-rata Precision@10 sebesar 70% diperoleh dari delapan kueri pengujian.

Perhitungan menggunakan pembagi tetap 10, termasuk ketika jumlah hasil
yang ditemukan kurang dari 10.

Selain itu, seluruh 56 hasil yang benar-benar dikembalikan oleh sistem
dinilai relevan berdasarkan penilaian manual pada sampel pengujian ini.
Dengan demikian, relevansi di antara hasil yang ditemukan adalah 100%.

Kedua nilai tersebut memiliki definisi pengukuran yang berbeda dan tidak
boleh dianggap sebagai ukuran akurasi umum seluruh sistem.

### Verifikasi label manual

Proses pemeriksaan ulang menemukan satu perubahan label pada destinasi
Candi Cetho untuk kueri "Wisata budaya di Jawa Tengah".

Label awal bernilai 0 dan setelah pemeriksaan ulang diubah menjadi 1
karena destinasi tersebut relevan terhadap kueri. Catatan juga diberikan
mengenai ketidaksesuaian metadata kota pada dataset.

File label yang digunakan sebagai acuan evaluasi akhir adalah:

`data/processed/label_relevansi_manual_v7_terverifikasi.csv`

## 3. Pengujian Penyaringan Provinsi

Pengujian dilakukan terhadap seluruh 37 nama provinsi yang tersedia
dalam dataset nasional.

Hasil pengujian menunjukkan bahwa seluruh provinsi menghasilkan
kecocokan metadata lokasi sebesar 100%.

Terdapat 289 kemunculan hasil dari seluruh pengujian provinsi,
dan seluruh hasil yang dikembalikan memiliki nilai Province yang
sesuai dengan provinsi yang diminta.

Hasil ini menunjukkan konsistensi penyaringan berdasarkan metadata
provinsi pada skenario pengujian.

Nilai tersebut bukan jaminan bahwa seluruh metadata geografis dalam
dataset telah benar secara faktual. Verifikasi lokasi destinasi
tetap diperlukan.

Rincian pengujian tersedia pada:

`data/processed/evaluasi_provinsi_v7.csv`

## 4. Audit Kualitas Dataset Nasional

Dataset nasional diperiksa menggunakan beberapa aspek kualitas data.

| Pemeriksaan | Hasil |
|---|---:|
| Jumlah destinasi | 1.025 |
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
| URL gambar berformat HTTP/HTTPS | 1.025 |
| Provinsi dikoreksi berdasarkan alamat | 89 |
| Provinsi perlu verifikasi | 1 |

Pemeriksaan menunjukkan bahwa dataset masih memiliki beberapa keterbatasan,
khususnya deskripsi yang tidak informatif, informasi kota yang kosong,
koordinat yang berulang, serta satu data provinsi yang masih memerlukan
verifikasi.

Informasi yang tidak tersedia tidak dibuat secara sembarangan.
Nilai kosong tetap dipertahankan agar sistem tidak menyajikan
informasi yang tidak memiliki dasar.

Ringkasan audit tersedia pada:

`data/processed/ringkasan_audit_final.csv`

## 5. Keterbatasan Evaluasi

Evaluasi yang dilakukan masih memiliki beberapa keterbatasan:

1. Pengujian relevansi baru menggunakan delapan kueri.
2. Label relevansi dibuat melalui penilaian manual pada sampel hasil.
3. Hasil pengujian 37 provinsi mengukur kesesuaian metadata,
   bukan verifikasi geografis menyeluruh.
4. Kualitas informasi destinasi masih dipengaruhi kelengkapan dataset.
5. Kinerja algoritma pada variasi bahasa dan pertanyaan yang lebih luas
   masih memerlukan pengujian lanjutan.

## 6. Kesimpulan

Berdasarkan pengujian yang dilakukan, algoritma V7 menunjukkan kemampuan
menyaring lokasi secara konsisten pada skenario pengujian yang digunakan.

Rata-rata Precision@10 pada delapan kueri mencapai 70%, sedangkan seluruh
hasil yang ditemukan pada sampel tersebut dinilai relevan secara manual.

Pengujian provinsi menunjukkan kecocokan metadata sebesar 100% pada
37 provinsi.

Hasil ini menjadi dasar untuk pengembangan dan pengujian lebih lanjut
terhadap aplikasi WisataFinder berbasis dataset nasional.

---

**Artefak evaluasi:**
- `evaluasi_precision_v7.csv`
- `evaluasi_provinsi_v7.csv`
- `ringkasan_audit_final.csv`
- `label_relevansi_manual_v7_terverifikasi.csv`
- `perbandingan_akhir_v2_v7.csv`
