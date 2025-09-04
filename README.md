# Clustering Penderita Diabetes di Jawa Barat

Aplikasi web interaktif untuk melakukan analisis clustering pada data penderita diabetes di Jawa Barat menggunakan algoritma K-Means. Aplikasi ini dibangun dengan Streamlit dan menyediakan visualisasi yang informatif untuk memahami pola distribusi penderita diabetes berdasarkan kabupaten/kota.

## 🎯 Fitur Utama

- **Upload Dataset**: Mendukung file Excel (.xlsx) dengan format data yang sudah ditentukan
- **Clustering K-Means**: Implementasi algoritma K-Means dengan jumlah cluster yang dapat disesuaikan (2-10)
- **Evaluasi Cluster**: Perhitungan Silhouette Score dan Davies-Bouldin Index untuk menilai kualitas clustering
- **Visualisasi PCA 2D**: Pemetaan cluster dalam ruang 2 dimensi menggunakan Principal Component Analysis
- **Analisis per Tahun**: Visualisasi distribusi penderita diabetes per kabupaten/kota untuk setiap tahun
- **Ringkasan Statistik**: Tabel ringkasan karakteristik setiap cluster
- **Analisis Komparatif**: Grafik perbandingan rata-rata variabel antar cluster

## 🛠️ Teknologi yang Digunakan

- **Streamlit**: Framework untuk membangun aplikasi web interaktif
- **pandas**: Manipulasi dan analisis data
- **scikit-learn**: Machine learning library untuk clustering dan preprocessing
- **matplotlib**: Visualisasi data dan grafik
- **numpy**: Komputasi numerik

## 📋 Prerequisites

Pastikan Anda telah menginstal Python 3.7+ di sistem Anda.

## 🚀 Instalasi dan Menjalankan Aplikasi

### 1. Clone Repository

```bash
git clone https://github.com/username/clustering-diabetes-jabar.git
cd clustering-diabetes-jabar
```

### 2. Buat Virtual Environment (Opsional tapi Direkomendasikan)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada alamat `http://localhost:8501`

## 📁 Format Dataset

Dataset harus berupa file Excel (.xlsx) dengan format sebagai berikut:

| nama_kabupaten_kota | jumlah_penderita_dm | jumlah_ warga_terdaftar_bpjs | jumlah_puskesmas | tahun |
|---------------------|---------------------|------------------------------|------------------|-------|
| Bandung             | 1500                | 250000                       | 45               | 2020  |
| Bogor               | 1200                | 180000                       | 38               | 2020  |
| ...                 | ...                 | ...                          | ...              | ...   |

**Catatan Penting**:
- Header harus berada di baris pertama
- Kolom `jumlah_ warga_terdaftar_bpjs` memiliki spasi setelah underscore
- Data numerik harus dalam format angka, bukan string
- Sheet name harus "Sheet1"

## 📊 Cara Menggunakan Aplikasi

### 1. Upload Dataset
- Klik tombol "Upload Dataset Excel"
- Pilih file Excel yang sesuai dengan format yang ditentukan
- Data akan otomatis diproses dan dibersihkan

### 2. Atur Parameter Clustering
- Gunakan slider untuk menentukan jumlah cluster (k) dari 2-10
- Aplikasi akan menghitung clustering secara real-time

### 3. Analisis Hasil
- **Metrics**: Lihat Silhouette Score dan Davies-Bouldin Index untuk menilai kualitas cluster
  - Silhouette Score: Semakin tinggi semakin baik (range -1 hingga 1)
  - Davies-Bouldin Index: Semakin rendah semakin baik
- **Visualisasi PCA**: Lihat sebaran cluster dalam ruang 2D
- **Grafik per Tahun**: Analisis distribusi penderita diabetes per tahun
- **Tabel Ringkasan**: Lihat karakteristik setiap cluster
- **Analisis Komparatif**: Bandingkan rata-rata variabel antar cluster

## 🔍 Interpretasi Hasil

### Evaluasi Cluster
- **Silhouette Score > 0.5**: Clustering baik
- **Silhouette Score 0.25-0.5**: Clustering cukup
- **Silhouette Score < 0.25**: Clustering kurang baik

### Analisis Cluster
Setiap cluster menggambarkan karakteristik wilayah yang berbeda:
- **Cluster Rendah**: Daerah dengan jumlah penderita diabetes, peserta BPJS, dan puskesmas yang relatif sedikit
- **Cluster Sedang**: Daerah dengan nilai-nilai menengah
- **Cluster Tinggi**: Daerah dengan nilai-nilai tinggi (biasanya kota besar)

## 📦 Dependencies

```text
streamlit>=1.28.0
pandas>=1.5.0
matplotlib>=3.6.0
scikit-learn>=1.3.0
numpy>=1.21.0
openpyxl>=3.0.0
```

## 🐛 Troubleshooting

### Error: "ValueError" pada Bar Chart
- Pastikan dataset memiliki data yang valid untuk semua kolom numerik
- Periksa apakah ada nilai NaN atau missing values yang tidak tertangani

### Error: File Upload
- Pastikan file Excel memiliki sheet bernama "Sheet1"
- Periksa format header sesuai dengan yang ditentukan
- Pastikan file tidak corrupt atau terlindungi password

### Performance Issues
- Untuk dataset besar (>1000 baris), proses clustering mungkin membutuhkan waktu lebih lama
- Pertimbangkan untuk menggunakan sample data jika dataset terlalu besar

## 🤝 Kontribusi

1. Fork repository ini
2. Buat branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- Data diabetes Jawa Barat dari [sumber data]
- Terima kasih kepada komunitas Streamlit dan scikit-learn
- Inspirasi dari berbagai proyek clustering yang ada
