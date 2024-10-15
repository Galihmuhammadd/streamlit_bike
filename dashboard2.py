import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# seabirn
sns.set(style="whitegrid")

# Load dataset
day_data = pd.read_csv('day.csv')  
hour_data = pd.read_csv('hour.csv')  

# Judul Dashboard
st.title("Dashboard Penggunaan Bike-Sharing")

# Visualisasi 1: Distribusi Penggunaan Sepeda Berdasarkan Musim
st.header("Distribusi Penggunaan Sepeda Berdasarkan Musim")

# Konsistensi palet warna
season_plot = plt.figure(figsize=(8,6))
sns.countplot(x='Musim', data=day_data, palette='Blues_d')  # Menggunakan palet warna seragam
plt.title("Distribusi Penggunaan Sepeda Berdasarkan Musim", fontsize=16)
plt.xlabel("Musim", fontsize=12)
plt.ylabel("Jumlah Pengguna", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()  # Agar label dan elemen grafik tidak terpotong
st.pyplot(season_plot)

# Visualisasi 2: Tren Penggunaan Sepeda Per Jam
st.header("Tren Penggunaan Sepeda Per Jam")

# Menggunakan warna untuk menyoroti puncak tren
hour_plot = plt.figure(figsize=(10,6))
sns.lineplot(x='Jam', y='Jumlah Total', data=hour_data, marker='o', color='darkblue', linewidth=2)
plt.fill_between(hour_data['Jam'], hour_data['Jumlah Total'], color='skyblue', alpha=0.3)  # Highlight area di bawah garis
plt.title("Tren Penggunaan Sepeda Per Jam", fontsize=16)
plt.xlabel("Jam", fontsize=12)
plt.ylabel("Jumlah Total Pengguna", fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
st.pyplot(hour_plot)

# Elemen interaktif (Opsional) - Filter berdasarkan musim
st.sidebar.header("Filter Data Berdasarkan Musim")
season_filter = st.sidebar.selectbox("Pilih Musim", day_data['Musim'].unique())

# Visualisasi setelah filter
st.header(f"Tren Penggunaan Sepeda Berdasarkan {season_filter}")

filtered_data = day_data[day_data['Musim'] == season_filter]
filtered_plot = plt.figure(figsize=(10,6))
sns.boxplot(x='Musim', y='Jumlah Total', data=filtered_data, palette='Blues_d')
plt.title(f"Penggunaan Sepeda pada Musim {season_filter}", fontsize=16)
plt.ylabel("Jumlah Total Pengguna", fontsize=12)
plt.tight_layout()
st.pyplot(filtered_plot)

# ----------------------------------------
# RFM Analysis
# ----------------------------------------

# Copy dataset day_data untuk RFM analysis
rfm_data = day_data.copy()

# Convert 'Tanggal' menjadi format datetime untuk perhitungan Recency
rfm_data['Tanggal'] = pd.to_datetime(rfm_data['Tanggal'])

# Set reference date (misalnya tanggal terbaru dalam dataset)
reference_date = rfm_data['Tanggal'].max()

# Hitung Recency: Selisih hari antara tanggal acuan dan tanggal penggunaan terakhir
rfm_data['Recency'] = (reference_date - rfm_data['Tanggal']).dt.days

# Hitung Frequency: Jumlah total penggunaan per musim
rfm_frequency = rfm_data.groupby('Musim Deskriptif')['Jumlah Total'].count().reset_index()
rfm_frequency.columns = ['Musim Deskriptif', 'Frequency']

# Hitung Monetary: Total penggunaan per musim (asumsi penggunaan sebagai proxy untuk nilai monetari)
rfm_monetary = rfm_data.groupby('Musim Deskriptif')['Jumlah Total'].sum().reset_index()
rfm_monetary.columns = ['Musim Deskriptif', 'Monetary']

# Gabungkan Recency, Frequency, dan Monetary berdasarkan 'Musim Deskriptif'
rfm_summary = rfm_data.groupby('Musim Deskriptif').agg({
    'Recency': 'mean'  # Menggunakan rata-rata Recency per musim
}).reset_index()

# Gabungkan Frequency dan Monetary dengan rfm_summary
rfm_summary = rfm_summary.merge(rfm_frequency, on='Musim Deskriptif').merge(rfm_monetary, on='Musim Deskriptif')


# Visualisasi untuk RFM Analysis
st.header("RFM Analysis")

# Plotting Recency
st.subheader("Recency by Season")
recency_plot = plt.figure(figsize=(8, 6))
plt.bar(rfm_summary['Musim Deskriptif'], rfm_summary['Recency'], color='skyblue')
plt.title('Recency by Season', fontsize=16)
plt.xlabel('Season', fontsize=12)
plt.ylabel('Average Recency (days)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(recency_plot)

# Plotting Frequency
st.subheader("Frequency by Season")
frequency_plot = plt.figure(figsize=(8, 6))
plt.bar(rfm_summary['Musim Deskriptif'], rfm_summary['Frequency'], color='lightgreen')
plt.title('Frequency by Season', fontsize=16)
plt.xlabel('Season', fontsize=12)
plt.ylabel('Total Frequency (number of transactions)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(frequency_plot)

# Plotting Monetary
st.subheader("Monetary by Season")
monetary_plot = plt.figure(figsize=(8, 6))
plt.bar(rfm_summary['Musim Deskriptif'], rfm_summary['Monetary'], color='coral')
plt.title('Monetary by Season', fontsize=16)
plt.xlabel('Season', fontsize=12)
plt.ylabel('Total Monetary Value (users)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(monetary_plot)

# Simulasi data lokasi dengan latitude dan longitude
# Tambahkan satu nilai latitude dan longitude ke semua baris
day_data['latitude'] = [1.35] * len(day_data)
day_data['longitude'] = [103.82] * len(day_data)


# Binning Jumlah Total Penggunaan untuk Clustering Manual
day_data['Usage_Cluster'] = pd.cut(day_data['Jumlah Total'], 
                                   bins=[0, 500, 1000, 1500, 2000], 
                                   labels=['Low', 'Medium', 'High', 'Very High'])

# 1. RFM Analysis Section
st.header("RFM Analysis")
st.write(rfm_summary[['Musim Deskriptif', 'Recency', 'Frequency', 'Monetary']])

# 2. Geoanalysis Section - Peta Penggunaan Berdasarkan Lokasi
st.header("Peta Penggunaan Sepeda Berdasarkan Lokasi")

# Membuat peta interaktif
map_center = [1.35, 103.82]
bike_map = folium.Map(location=map_center, zoom_start=12)

# Menambahkan marker untuk setiap lokasi
for index, row in day_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Penggunaan: {row['Jumlah Total']}"
    ).add_to(bike_map)

# Menampilkan peta di Streamlit
st_folium(bike_map, width=700)

# Heatmap Geoanalysis
st.header("Heatmap Penggunaan Sepeda")
heat_data = [[row['latitude'], row['longitude'], row['Jumlah Total']] for index, row in day_data.iterrows()]
bike_map_heat = folium.Map(location=map_center, zoom_start=12)
HeatMap(heat_data).add_to(bike_map_heat)
st_folium(bike_map_heat, width=700)

# 3. Clustering Section - Manual Clustering
st.header("Clustering Pengguna Berdasarkan Jumlah Penggunaan")
st.write(day_data[['Tanggal', 'Jumlah Total', 'Usage_Cluster']])

# Visualisasi Clustering
cluster_plot = plt.figure(figsize=(8,6))
sns.countplot(x='Usage_Cluster', data=day_data, palette='Set3')
plt.title("Distribusi Pengguna Berdasarkan Cluster Penggunaan", fontsize=16)
plt.xlabel("Usage Cluster", fontsize=12)
plt.ylabel("Jumlah Pengguna", fontsize=12)
plt.tight_layout()
st.pyplot(cluster_plot)
