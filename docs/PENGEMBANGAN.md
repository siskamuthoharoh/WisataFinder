# Riwayat Pengembangan WisataFinder

## 1. Pendahuluan

WisataFinder merupakan aplikasi mesin pencari destinasi wisata
berbasis web yang dikembangkan menggunakan Python dan Streamlit.

Proyek ini dikembangkan secara bertahap, mulai dari aplikasi
pencarian dengan dataset awal hingga pengembangan sistem pencarian
nasional menggunakan TF-IDF dan Cosine Similarity.

Pengembangan dilakukan dengan memperhatikan kualitas data,
kemampuan pencarian, kesesuaian lokasi, evaluasi hasil,
dan kemudahan penggunaan aplikasi.

## 2. Tahap Pengembangan Awal

Pada tahap awal, WisataFinder menggunakan dataset pariwisata
dengan 437 destinasi.

Aplikasi dikembangkan menggunakan:
- Python.
- Streamlit.
- Pandas.
- Scikit-learn.
- TF-IDF.
- Cosine Similarity.

Fitur awal aplikasi meliputi:
- Pencarian destinasi berdasarkan kata kunci.
- Filter lokasi.
- Filter kategori.
- Penampilan informasi destinasi.
- Pengurutan hasil berdasarkan kemiripan teks.

Pada tahap ini, tujuan utama adalah membangun produk awal
yang dapat digunakan untuk mencari informasi destinasi wisata.

## 3. Pengembangan Dataset Nasional

Untuk memperluas cakupan pencarian, dilakukan pengembangan
menggunakan dataset nasional dari Kaggle.

Dataset sumber memiliki 1.025 destinasi dengan 11 kolom.

Setelah proses pengolahan, disusun dataset nasional
dengan 1.025 destinasi dan 23 kolom.

Dataset nasional mencakup 37 provinsi berdasarkan
label provinsi yang tersedia.

Pengembangan ini bertujuan agar pengguna dapat mencari
destinasi wisata dari lebih banyak wilayah di Indonesia.

Dataset lama tetap dipertahankan sebagai bagian dari
riwayat pengembangan. Kedua dataset tidak langsung
digabungkan karena memiliki sumber dan struktur yang berbeda.

## 4. Audit dan Pengolahan Data

Setelah dataset nasional disiapkan, dilakukan pemeriksaan
kualitas data.

Pemeriksaan mencakup:
- Nilai kosong.
- Data duplikat.
- Kelengkapan alamat.
- Koordinat geografis.
- Kualitas deskripsi.
- URL gambar.
- Konsistensi kota dan provinsi.

Hasil audit menunjukkan beberapa data memerlukan
perhatian lebih lanjut, khususnya deskripsi yang tidak
informatif, kota yang belum tersedia, koordinat yang
berulang, dan metadata lokasi yang perlu diverifikasi.

Informasi yang tidak tersedia tidak dibuat secara
sembarangan. Nilai kosong tetap dipertahankan agar
sistem tidak menyajikan informasi yang tidak memiliki dasar.

## 5. Eksperimen Pengembangan Algoritma

Eksperimen dilakukan secara bertahap melalui tujuh versi
pengembangan, yaitu V2 sampai V7, dengan V2 sebagai
pengembangan setelah baseline pencarian awal.

### V2 – Penambahan skor kecocokan

Menambahkan skor tambahan untuk kecocokan kategori
dan lokasi agar destinasi yang sesuai memperoleh
prioritas lebih tinggi.

### V3 – Penyaringan kategori dan lokasi

Mengembangkan penyaringan berdasarkan kategori
dan lokasi destinasi.

### V4 – Pencocokan nama destinasi

Memperluas pencarian dengan mempertimbangkan
nama destinasi sebagai bagian dari pencocokan.

### V5 – Deteksi kota otomatis

Mengembangkan kemampuan sistem untuk mengenali
nama kota yang disebutkan dalam kata kunci pengguna.

### V6 – Deteksi provinsi dan kota

Memperluas pengenalan lokasi menggunakan data
provinsi dan kota yang tersedia pada dataset nasional.

### V7 – Validasi lokasi pencarian

Menambahkan validasi lokasi agar sistem tidak
mengembalikan destinasi dari wilayah lain ketika
lokasi yang diminta tidak dikenali atau tidak tersedia.

Eksperimen tersebut didokumentasikan dalam notebook:

`notebooks/pengembangan_dan_evaluasi_algoritma_nasional.ipynb`

## 6. Evaluasi Algoritma

Pengujian dilakukan untuk membandingkan kemampuan
versi algoritma V2 sampai V7.

Skenario pengujian mencakup:
- Pencarian museum di Bandung.
- Pencarian wisata di Papua Barat.
- Pencarian lokasi yang tidak dikenal seperti Atlantis.
- Pencarian Kepulauan Riau.

Selain perbandingan algoritma, dilakukan evaluasi
relevansi manual pada delapan kueri dengan total
56 hasil pencarian yang dinilai.

Hasil evaluasi V7:
- Rata-rata Precision@10: 70%.
- Hasil yang ditemukan dan dinilai relevan: 56 dari 56.
- Pengujian penyaringan provinsi: 37 provinsi.
- Total hasil pada pengujian provinsi: 289.
- Hasil yang sesuai dengan metadata provinsi: 289.

Angka tersebut berlaku pada skenario dan data pengujian
yang telah dilakukan, bukan merupakan klaim akurasi umum
untuk seluruh pertanyaan pengguna.

Hasil lengkap disimpan dalam file evaluasi CSV
dan dijelaskan pada `docs/EVALUASI.md`.

## 7. Pengembangan Aplikasi Nasional

Agar aplikasi awal tetap aman, dibuat salinan aplikasi
untuk pengembangan dataset nasional.

File aplikasi:
- `app.py`: aplikasi awal.
- `app_nasional_v7.py`: salinan aplikasi untuk pengembangan
  menggunakan dataset nasional.

Aplikasi nasional diarahkan untuk menggunakan:

`data/processed/destinations_nasional.csv`

Pada salinan aplikasi dilakukan pengembangan filter:
- Provinsi.
- Kota atau kabupaten.
- Kategori wisata.

Selain itu, dilakukan perbaikan deteksi nama lokasi
agar sistem dapat mengenali nama pendek seperti
Semarang dan Bandung serta nama administratif lengkap
seperti Kabupaten Semarang dan Kota Bandung.

Pemeriksaan sintaks Python terhadap perubahan tersebut
telah berhasil. Aplikasi Streamlit juga telah berhasil
dijalankan pada tahap pengujian sebelumnya.

Pengujian ulang terhadap seluruh perubahan terakhir
masih perlu diselesaikan sebelum aplikasi nasional
ditetapkan sebagai versi utama.

## 8. Pengelolaan Repository GitHub

Proyek menggunakan repository:

https://github.com/siskamuthoharoh/WisataFinder

Pengembangan nasional dilanjutkan pada repository
yang sama untuk mempertahankan riwayat proyek.

Beberapa commit pengembangan sebelumnya meliputi:
- `1e9d522`: preprocessing data wisata.
- `874edad`: dokumentasi eksplorasi dataset.
- `c7e33ef`: penambahan dataset mentah.
- `ef31a72`: dokumentasi hasil evaluasi query expansion.
- `a0071ff`: implementasi aplikasi pencarian WisataFinder.

Pengembangan dataset nasional selanjutnya akan disimpan
melalui commit terpisah sesuai kelompok pekerjaan,
misalnya dataset, dokumentasi, aplikasi, dan evaluasi.

File sementara, file cadangan, serta hasil eksperimen
yang tidak digunakan sebagai artefak akhir tidak
direncanakan untuk dimasukkan ke repository publik.

## 9. Rencana Pengembangan Berikutnya

Tahap pengembangan berikutnya meliputi:

1. Menyelesaikan pengujian filter provinsi, kota,
   kabupaten, dan kategori.
2. Memastikan algoritma V7 terintegrasi dengan benar
   pada aplikasi nasional.
3. Melakukan pengujian fungsional pada berbagai
   variasi kata kunci.
4. Menyelesaikan seleksi file yang akan dimasukkan
   ke repository GitHub.
5. Memeriksa lisensi dataset sebelum publikasi.
6. Memperbarui README dan dokumentasi proyek.
7. Melakukan commit dan push pengembangan nasional
   secara bertahap.
8. Mengembangkan fitur chatbot WisataBot.

## 10. Rencana Pengembangan WisataBot

WisataBot direncanakan sebagai asisten pencarian
dan rekomendasi destinasi melalui percakapan.

Versi awal direncanakan menggunakan dataset nasional
yang sama dengan WisataFinder agar hasil rekomendasi
konsisten dengan informasi yang tersedia dalam aplikasi.

Fitur yang direncanakan:
- Pencarian destinasi melalui percakapan.
- Rekomendasi berdasarkan kategori wisata.
- Pencarian berdasarkan provinsi dan kota.
- Penyajian informasi destinasi dari dataset.
- Alternatif rekomendasi ketika hasil tidak ditemukan.

Fitur ini masih dalam tahap perencanaan
dan belum menjadi bagian dari aplikasi aktif.

## 11. Kesimpulan

Pengembangan WisataFinder telah berkembang dari aplikasi
pencarian awal dengan 437 destinasi menjadi pengembangan
mesin pencari nasional dengan dataset berisi 1.025 destinasi.

Proses pengembangan mencakup pengolahan dataset,
audit kualitas data, eksperimen algoritma V2 sampai V7,
evaluasi relevansi, pengujian lokasi, serta pengembangan
fitur aplikasi.

Fokus pengembangan saat ini adalah menyelesaikan
integrasi dan pengujian aplikasi nasional serta
menata dokumentasi dan repository GitHub.

WisataBot direncanakan sebagai fitur tambahan
untuk memperluas kemampuan WisataFinder dalam
memberikan rekomendasi destinasi melalui percakapan.
