\# Dokumentasi Pengujian Aplikasi WisataFinder



\## 1. Tujuan Pengujian



Pengujian dilakukan untuk memastikan fungsi pencarian dan penyaringan destinasi wisata pada aplikasi WisataFinder versi nasional berjalan sesuai kebutuhan pengguna.



Pengujian dilakukan secara manual melalui aplikasi Streamlit dengan memperhatikan hasil pencarian kata kunci, deteksi lokasi, filter provinsi, kota/kabupaten, kategori, dan validasi input.



\## 2. Lingkungan Pengujian



| Komponen | Keterangan |

|---|---|

| Aplikasi | WisataFinder versi nasional |

| File aplikasi | `app\_nasional\_v7.py` |

| Framework | Streamlit |

| Bahasa pemrograman | Python 3.10 |

| Environment | `ds\_siska` |

| Dataset | Dataset wisata nasional |

| Jumlah data | 1.025 destinasi |

| Jumlah provinsi | 37 |

| Metode pencarian | TF-IDF dan Cosine Similarity |

| Jenis pengujian | Pengujian fungsional manual |



\## 3. Skenario Pengujian



Pengujian dilakukan dengan membandingkan input pengguna terhadap hasil yang diharapkan.



| ID | Skenario | Input atau Kondisi | Hasil yang Diharapkan | Hasil |

|---|---|---|---|---|

| TC01 | Pencarian museum di Semarang | Kata kunci `museum di Semarang`, semua filter Semua | Menampilkan museum di Semarang | Berhasil |

| TC02 | Pencarian museum di Bandung | Kata kunci `museum di Bandung`, semua filter Semua | Menampilkan museum di Bandung | Berhasil |

| TC03 | Pencarian pantai di Bali | Kata kunci `pantai di Bali`, semua filter Semua | Menampilkan destinasi pantai di Bali | Berhasil |

| TC04 | Validasi lokasi tidak dikenal | Kata kunci `tempat wisata di Atlantis` | Menampilkan peringatan lokasi tidak ditemukan | Berhasil |

| TC05 | Kombinasi pencarian dan filter | Kata kunci `museum`, Jawa Tengah, Kota Semarang | Menampilkan hasil sesuai lokasi | Berhasil |

| TC06 | Filter provinsi dengan kata kunci | Kata kunci `museum`, Jawa Tengah, kota dan kategori Semua | Menampilkan museum di Jawa Tengah | Berhasil |

| TC07 | Filter kategori dengan kata kunci | Kata kunci `wisata`, pilih satu kategori | Hasil sesuai kategori pilihan | Berhasil |

| TC08 | Filter kota dengan kata kunci | Kata kunci `museum`, Kota Semarang | Menampilkan museum di Kota Semarang | Berhasil |

| TC09 | Provinsi dan kota tidak sesuai | Kata kunci `museum`, Jawa Barat, Kota Semarang | Tidak menampilkan destinasi | Berhasil |

| TC10 | Filter provinsi tanpa kata kunci | Kata kunci kosong, Jawa Tengah | Menampilkan destinasi di Jawa Tengah | Berhasil |

| TC11 | Filter kota tanpa kata kunci | Kata kunci kosong, Kota Semarang | Menampilkan destinasi di Kota Semarang | Berhasil |

| TC12 | Filter kategori tanpa kata kunci | Kata kunci kosong, kategori Pantai | Menampilkan destinasi kategori Pantai | Berhasil |

| TC13 | Kombinasi tiga filter tanpa kata kunci | Kata kunci kosong, Jawa Tengah, Kota Semarang, Museum | Menampilkan destinasi yang memenuhi seluruh filter | Berhasil |

| TC14 | Semua input kosong | Kata kunci kosong dan semua filter Semua | Menampilkan peringatan untuk memasukkan kata kunci atau memilih filter | Berhasil |

| TC15 | Provinsi dan kota tidak sesuai tanpa kata kunci | Kata kunci kosong, Jawa Barat, Kota Semarang | Tidak menampilkan destinasi yang tidak sesuai | Berhasil |



\## 4. Analisis Hasil Pengujian



Berdasarkan 15 skenario pengujian fungsional manual, aplikasi telah menunjukkan perilaku sesuai dengan hasil yang diharapkan.



Hasil pengujian menunjukkan bahwa:



1\. Sistem dapat melakukan pencarian berdasarkan kata kunci menggunakan TF-IDF dan Cosine Similarity.

2\. Sistem dapat mengenali penyebutan kota dan provinsi dalam kata kunci pencarian.

3\. Sistem dapat menerapkan filter provinsi, kota/kabupaten, dan kategori secara terpisah maupun bersamaan.

4\. Sistem mendukung pencarian tanpa kata kunci ketika pengguna memilih minimal satu filter.

5\. Sistem memberikan peringatan ketika kata kunci kosong dan tidak ada filter yang dipilih.

6\. Sistem dapat menangani lokasi yang tidak dikenal dan kombinasi filter lokasi yang tidak sesuai.



\## 5. Batasan Pengujian



Pengujian ini merupakan pengujian fungsional manual berdasarkan skenario yang telah ditentukan. Pengujian belum mencakup seluruh kemungkinan kombinasi input, pengujian beban, performa pada banyak pengguna secara bersamaan, maupun pengujian otomatis seluruh fungsi program.



Hasil pengujian juga bergantung pada kelengkapan dan kualitas informasi lokasi dalam dataset.



\## 6. Kesimpulan



Berdasarkan 15 skenario pengujian yang dilakukan, fungsi utama aplikasi WisataFinder versi nasional telah berjalan sesuai kebutuhan pengujian.



Fitur pencarian dengan kata kunci, pencarian menggunakan filter tanpa kata kunci, kombinasi filter lokasi dan kategori, serta validasi input telah menunjukkan hasil yang sesuai dengan perilaku yang diharapkan.



Pengujian ini menjadi dasar untuk pengembangan dan penyempurnaan aplikasi WisataFinder selanjutnya.
