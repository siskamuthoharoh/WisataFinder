# Metodologi Sistem WisataFinder

## 1. Pendekatan Pengembangan

WisataFinder dikembangkan sebagai mesin pencari destinasi wisata
berbasis teks menggunakan Python dan Streamlit.

Sistem menggunakan metode Information Retrieval (IR), yaitu
pendekatan untuk menemukan dokumen atau informasi yang paling
sesuai dengan kebutuhan pencarian pengguna.

Dalam proyek ini, setiap destinasi wisata diperlakukan sebagai
dokumen teks yang berisi informasi nama destinasi, kategori,
dan deskripsi.

Dataset nasional digunakan sebagai sumber data utama dalam
pengembangan sistem pencarian versi nasional.

## 2. Alur Kerja Sistem

Secara umum, proses pencarian WisataFinder terdiri dari beberapa tahap:

1. Memuat dataset destinasi wisata.
2. Melakukan persiapan teks untuk kebutuhan pencarian.
3. Mengubah teks destinasi menjadi representasi numerik menggunakan TF-IDF.
4. Menerima kata kunci dari pengguna.
5. Mengubah kata kunci menjadi representasi TF-IDF.
6. Menghitung kemiripan antara kata kunci dan dokumen destinasi
   menggunakan Cosine Similarity.
7. Menerapkan penyaringan kategori dan lokasi.
8. Mengurutkan hasil berdasarkan tingkat kemiripan.
9. Menampilkan destinasi yang sesuai kepada pengguna.

## 3. Persiapan Data Teks

Sistem menggunakan informasi teks destinasi untuk membangun indeks pencarian.

Informasi yang dimanfaatkan meliputi:

- Nama destinasi (Place_Name).
- Kategori wisata (Category).
- Deskripsi destinasi (Description).

Pada dataset nasional juga disiapkan kolom `search_text`
untuk mendukung proses pencarian.

Persiapan teks bertujuan agar informasi destinasi dapat
direpresentasikan dalam bentuk yang bisa diproses oleh algoritma.

Nilai teks yang kosong ditangani agar tidak menyebabkan
kesalahan pada proses pemuatan dan pengindeksan data.

## 4. Metode TF-IDF

TF-IDF merupakan singkatan dari Term Frequency-Inverse Document Frequency.

Metode ini digunakan untuk memberikan bobot pada kata berdasarkan
frekuensi kemunculannya dalam suatu dokumen dan tingkat kelangkaannya
dalam keseluruhan kumpulan dokumen.

### 4.1. Term Frequency (TF)

Term Frequency menunjukkan seberapa sering suatu kata muncul
dalam sebuah dokumen.

Secara sederhana:

TF(t,d) = jumlah kemunculan kata t dalam dokumen d

### 4.2. Inverse Document Frequency (IDF)

Inverse Document Frequency menunjukkan tingkat kepentingan suatu
kata berdasarkan jumlah dokumen yang memuat kata tersebut.

Secara umum:

IDF(t) = log(N / df(t))

Keterangan:

- N adalah jumlah seluruh dokumen.
- df(t) adalah jumlah dokumen yang mengandung kata t.

### 4.3. Bobot TF-IDF

Bobot TF-IDF diperoleh dari kombinasi TF dan IDF.

TF-IDF(t,d) = TF(t,d) × IDF(t)

Kata yang sering muncul pada dokumen tertentu tetapi relatif jarang
pada dokumen lain dapat memperoleh bobot yang lebih tinggi.

Dalam implementasi eksperimen nasional, digunakan
`TfidfVectorizer` dari library Scikit-learn.

Konfigurasi eksperimen dasar menggunakan pengaturan default
`TfidfVectorizer()` pada dataset yang telah memiliki kolom `search_text`.

## 5. Metode Cosine Similarity

Cosine Similarity digunakan untuk menghitung kemiripan antara
vektor kata kunci pencarian dan vektor dokumen destinasi.

Rumus Cosine Similarity:

similarity(A,B) = (A · B) / (||A|| × ||B||)

Keterangan:

- A adalah vektor kata kunci pengguna.
- B adalah vektor dokumen destinasi.
- A · B adalah hasil perkalian titik kedua vektor.
- ||A|| dan ||B|| adalah panjang masing-masing vektor.

Nilai kemiripan yang lebih tinggi menunjukkan bahwa teks dokumen
memiliki kemiripan yang lebih besar terhadap kata kunci pencarian.

Dalam implementasi, penghitungan dilakukan menggunakan
`cosine_similarity` dari Scikit-learn.

Hasil kemudian diurutkan berdasarkan skor kemiripan.

## 6. Pengembangan Algoritma V2 sampai V7

Pengembangan algoritma dilakukan secara bertahap.
Setiap versi memperbaiki keterbatasan yang ditemukan pada versi
sebelumnya.

### 6.1. V2 – Penambahan Bobot Kategori dan Lokasi

Pada V2 ditambahkan skor tambahan ketika kueri cocok dengan
kategori atau lokasi destinasi.

Tujuannya adalah meningkatkan prioritas destinasi yang memiliki
kesesuaian dengan maksud pencarian pengguna.

Pada eksperimen ini, kecocokan kategori dan lokasi masing-masing
diberikan tambahan skor sebesar 0,30.

Versi ini masih menggunakan pendekatan penambahan skor sehingga
hasil yang tidak sesuai lokasi masih dapat muncul.

### 6.2. V3 – Penyaringan Kategori dan Lokasi

V3 mengembangkan pendekatan penyaringan berdasarkan kategori
dan lokasi.

Sistem mulai menggunakan kondisi kecocokan untuk membatasi
kandidat destinasi.

Pada versi awal, ketika tidak ditemukan hasil yang cocok,
sistem masih dapat kembali menampilkan seluruh dataset.

Perilaku tersebut menjadi salah satu kelemahan yang perlu diperbaiki.

### 6.3. V4 – Pencocokan Nama Destinasi

V4 memperluas pencocokan kata kunci dengan mempertimbangkan
nama destinasi.

Pendekatan ini membantu menemukan tempat berdasarkan identitas
namanya meskipun kategori dataset tidak selalu menggunakan
istilah yang sama dengan kueri pengguna.

Contohnya adalah pencarian kebun binatang di Jakarta,
yang dapat menemukan Kebun Binatang Ragunan meskipun
kategori datanya tidak secara eksplisit bernama kebun binatang.

Pada versi ini, mekanisme fallback dari versi sebelumnya
masih menjadi keterbatasan.

### 6.4. V5 – Deteksi Kota Otomatis

V5 mengembangkan kemampuan sistem dalam mendeteksi kota
yang disebutkan langsung oleh pengguna.

Dengan demikian, sistem tidak selalu bergantung pada pilihan
kota melalui filter.

Pengujian menunjukkan peningkatan pada kueri museum di Bandung.
Versi ini menghasilkan empat hasil yang sesuai dengan Kota Bandung.

Namun, pencarian masih memiliki keterbatasan pada cakupan
pengenalan lokasi dan penanganan wilayah yang belum dikenali.

### 6.5. V6 – Deteksi Provinsi dan Kota

V6 memperluas deteksi lokasi dengan menggunakan informasi
kota dan provinsi yang tersedia pada dataset.

Pengenalan lokasi dilakukan berdasarkan daftar lokasi
yang berasal dari dataset, termasuk nama provinsi
yang telah disusun untuk kebutuhan pencarian.

Peningkatan ini membantu sistem membedakan pencarian
berdasarkan kota dan provinsi.

Pada pengujian Papua Barat, V6 menghasilkan tiga destinasi
yang seluruhnya sesuai dengan metadata provinsi.

Namun, sistem masih memerlukan validasi tambahan untuk
menangani lokasi yang tidak dikenal.

### 6.6. V7 – Validasi Lokasi Pencarian

V7 menambahkan lapisan validasi terhadap lokasi yang
disebutkan oleh pengguna.

Tujuannya adalah mencegah sistem menampilkan destinasi
dari lokasi lain ketika lokasi yang diminta tidak dikenali.

Contohnya:

- `museum di Semarang` harus mengarah pada lokasi Semarang.
- `pantai di Bali` harus mengarah pada provinsi Bali.
- `tempat wisata di Atlantis` harus menghasilkan pencarian kosong
  karena Atlantis tidak tersedia sebagai lokasi yang dikenali.
- `tempat wisata di Kepulauan Riau` tidak menghasilkan destinasi
  apabila lokasi tersebut belum mempunyai data pada dataset.

V7 juga dikembangkan agar tidak menggunakan fallback ke seluruh
dataset ketika lokasi yang disebutkan tidak cocok.

Dengan pendekatan tersebut, sistem lebih menjaga kesesuaian
antara maksud pencarian dan lokasi hasil.

## 7. Penggunaan Alias Kategori dan Lokasi

Pengguna dapat menggunakan istilah yang berbeda untuk
menyatakan kebutuhan pencarian yang sama.

Oleh karena itu, pada eksperimen tertentu digunakan
pemetaan alias kategori dan lokasi.

Contoh alias kategori:

| Istilah pengguna | Kelompok pencarian |
|---|---|
| Laut | Pantai atau bahari |
| Pendakian | Gunung |
| Zoo | Kebun binatang |
| Curug | Air terjun |
| Mal | Mall atau pusat perbelanjaan |

Contoh alias lokasi:

| Istilah pengguna | Lokasi yang dikenali |
|---|---|
| Jateng | Jawa Tengah |
| Jabar | Jawa Barat |
| Jatim | Jawa Timur |
| Jogja | Daerah Istimewa Yogyakarta |
| NTB | Nusa Tenggara Barat |

Pemetaan alias membantu menjembatani perbedaan istilah
antara kata kunci pengguna dan informasi yang tersimpan
dalam dataset.

Penggunaan alias disesuaikan dengan versi eksperimen
yang sedang diuji.

## 8. Penyaringan Hasil

Setelah skor kemiripan diperoleh, sistem menerapkan
penyaringan tambahan.

Penyaringan dapat menggunakan:

- Provinsi.
- Kota atau kabupaten.
- Kategori wisata.
- Kesesuaian identitas destinasi untuk kueri tertentu.
- Status verifikasi lokasi.

Filter lokasi dan kategori bertujuan membatasi hasil
agar sesuai dengan kebutuhan pengguna.

Pencarian tanpa lokasi tetap dapat menampilkan destinasi
dari berbagai wilayah selama hasilnya sesuai dengan
kata kunci dan filter yang digunakan.

## 9. Perbandingan dan Evaluasi Algoritma

Pengembangan V2 sampai V7 diuji dengan beberapa skenario,
antara lain:

- Museum di Bandung.
- Wisata di Papua Barat.
- Lokasi Atlantis.
- Kepulauan Riau.

Pengujian digunakan untuk melihat kemampuan setiap versi
dalam menemukan hasil yang sesuai dan menolak lokasi
yang tidak tersedia.

Selain itu, dilakukan penilaian relevansi secara manual
terhadap delapan kueri untuk mengevaluasi hasil pencarian V7.

Hasil lengkap tersedia pada:

- `data/processed/perbandingan_akhir_v2_v7.csv`
- `data/processed/evaluasi_precision_v7.csv`
- `data/processed/evaluasi_provinsi_v7.csv`

## 10. Batasan Metodologi

Metode TF-IDF dan Cosine Similarity memiliki beberapa keterbatasan.

1. Sistem terutama mengandalkan kemiripan kata dan teks.
2. Sinonim dan istilah yang tidak tercakup dalam alias
   dapat menghasilkan pencarian yang kurang tepat.
3. Kualitas hasil pencarian dipengaruhi kelengkapan
   dan kualitas deskripsi destinasi.
4. Metadata lokasi yang salah dapat menyebabkan hasil
   yang secara geografis tidak tepat.
5. Eksperimen dan evaluasi yang dilakukan belum mencakup
   seluruh kemungkinan kueri pengguna.
6. Pemetaan alias masih perlu diperluas berdasarkan
   variasi bahasa dan kebutuhan pengguna.

Oleh karena itu, pengembangan berikutnya dapat mencakup
perbaikan kualitas data, perluasan variasi kueri,
serta pengujian yang lebih luas.

## 11. Kesimpulan

WisataFinder menggunakan TF-IDF dan Cosine Similarity
sebagai dasar pencarian destinasi wisata.

Pengembangan V2 sampai V7 dilakukan untuk meningkatkan
kemampuan sistem dalam memahami kategori, mengenali lokasi,
menyaring hasil, serta menangani lokasi yang tidak dikenal.

Berdasarkan skenario pengujian yang dilakukan, V7 menunjukkan
perbaikan dalam penyaringan lokasi dibandingkan versi awal.

Algoritma ini menjadi dasar pengembangan aplikasi nasional
WisataFinder dan rencana fitur rekomendasi melalui WisataBot.

---

Dokumen ini menjelaskan metodologi eksperimen algoritma.
Implementasi dan hasil evaluasi aktual tetap perlu dilihat
pada notebook dan file aplikasi yang sesuai.
