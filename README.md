
## 1. Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis pola penggunaan layanan bike-sharing dengan menggunakan dataset harian dan per jam dari sistem bike-sharing. 
Analisis dilakukan untuk memberikan wawasan terkait pola penggunaan sepeda, tren musiman, dan preferensi pengguna berdasarkan waktu dan kondisi cuaca.

### Tujuan Proyek:
1. Menganalisis pengaruh musim terhadap penggunaan sepeda harian.
2. Mengidentifikasi tren penggunaan sepeda berdasarkan waktu dan musim.

## 2. Pertanyaan Bisnis yang Akan Dijawab
1. Bagaimana tren penggunaan sepeda pada musim panas dibandingkan musim dingin?
2. Jam berapa penggunaan sepeda mencapai puncaknya pada hari kerja dibandingkan akhir pekan selama bulan liburan?

## 3. File yang Disertakan
- `notebook.ipynb`: Berisi keseluruhan proses analisis data yang terstruktur menggunakan template Dicoding.
- `dashboard.py`: Script untuk membuat dashboard interaktif menggunakan Streamlit.
- `day.csv` dan `hour.csv`: Dataset harian dan per jam yang digunakan untuk analisis.
- `requirements.txt`: Berisi library yang dibutuhkan untuk menjalankan proyek.
- `revised_notebook.ipynb`: Versi revisi dari notebook dengan tambahan penjelasan setiap langkah analisis.

## 4. Cara Menjalankan Dashboard
1. Pastikan Anda sudah menginstal library yang dibutuhkan dengan menjalankan:
```
pip install -r requirements.txt
```
2. Menjalankan dashboard dengan perintah:
```
streamlit run dashboard/dashboard.py
```
3. Jika dashboard sudah dideploy, tautan akan tersedia di sini: [Link Streamlit Dashboard](#)

## 5. Kesimpulan
Proyek ini memberikan wawasan tentang pola penggunaan sepeda berdasarkan musim dan waktu dalam sehari. Penggunaan sepeda cenderung lebih tinggi pada musim panas dan mencapai puncaknya pada jam-jam tertentu selama akhir pekan. Analisis ini dapat membantu operator layanan bike-sharing dalam mengoptimalkan penawaran layanan berdasarkan tren musiman.
