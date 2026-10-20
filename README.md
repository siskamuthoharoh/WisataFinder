

\# WisataFinder



\*\*Sistem Temu Kembali Informasi Destinasi Wisata Menggunakan TF-IDF dan Cosine Similarity\*\*



\## 1. Deskripsi Proyek



WisataFinder adalah proyek Sistem Temu Kembali Informasi (STKI)

yang bertujuan membantu pengguna menemukan destinasi wisata

berdasarkan kata kunci dan informasi destinasi.



\## 2. Tujuan



\- Menemukan destinasi yang relevan dengan kebutuhan pengguna.

\- Menerapkan preprocessing teks.

\- Menerapkan TF-IDF dan Cosine Similarity.

\- Menyediakan filter kota, kategori, harga, dan rating.

\- Mengevaluasi kualitas hasil pencarian.

\- Menyediakan antarmuka berbasis Streamlit.



\## 3. Dataset



Dataset: Indonesia Tourism Destination  

File: `tourism\_with\_id.csv`  

Jumlah data awal: 437 destinasi



Informasi sumber dan lisensi dataset akan didokumentasikan

di `docs/DATASET.md`.



\## 4. Metode



1\. Validasi dataset

2\. Preprocessing teks

3\. Pembentukan fitur TF-IDF

4\. Perhitungan Cosine Similarity

5\. Pemeringkatan hasil pencarian

6\. Evaluasi relevansi



\## 5. Teknologi



\- Python

\- Pandas

\- Scikit-learn

\- Streamlit

\- Git dan GitHub



\## 6. Struktur Proyek



```text

WisataFinder/

├── .streamlit/

├── data/

│   ├── raw/

│   └── processed/

├── docs/

├── notebooks/

├── reports/

│   └── figures/

├── src/

├── tests/

├── .gitignore

├── README.md

└── requirements.txt

```



\## 7. Status Pengembangan



\- \[x] Struktur folder proyek

\- \[x] Validasi awal dataset

\- \[x] Pemeriksaan kolom dataset

\- \[ ] Preprocessing teks

\- \[ ] Mesin pencari TF-IDF dan Cosine Similarity

\- \[ ] Pengujian unit

\- \[ ] Evaluasi relevansi pencarian

\- \[ ] Aplikasi Streamlit

\- \[ ] Dokumentasi penggunaan

\- \[ ] Pengujian akhir



\## 8. Instalasi dan Penggunaan



Panduan instalasi dan cara menjalankan aplikasi akan dilengkapi

setelah implementasi selesai.



\## 9. Evaluasi



Hasil evaluasi akan dilaporkan berdasarkan query uji,

label relevansi, dan metrik pencarian yang sesuai.



\## 10. Pengembang



Proyek akademik untuk mata kuliah Sistem Temu Kembali Informasi (STKI).



