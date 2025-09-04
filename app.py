import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA
import numpy as np

# ============================
# 🎨 Config Streamlit
# ============================
st.set_page_config(page_title="Clustering Diabetes Jawa Barat", layout="wide")
st.title("Clustering Penderita Diabetes di Jawa Barat")

st.markdown("""
Aplikasi ini melakukan **Clustering (K-Means)** pada data penderita Diabetes di Jawa Barat  
berdasarkan jumlah penderita DM, peserta BPJS, dan jumlah puskesmas.
""")

# ============================
# 📂 Upload Dataset
# ============================
uploaded_file = st.file_uploader("Upload Dataset Excel", type=["xlsx"])

if uploaded_file:
    # Baca data
    df = pd.read_excel(uploaded_file, sheet_name="Sheet1")

    # Atur header yang benar
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    # Pilih kolom penting
    df_selected = df[['nama_kabupaten_kota', 'jumlah_penderita_dm',
                      'jumlah_ warga_terdaftar_bpjs', 'jumlah_puskesmas', 'tahun']].copy()
    df_selected.columns = ['kabupaten_kota', 'penderita_dm', 'bpjs', 'puskesmas', 'tahun']

    # Cleaning
    for col in ['penderita_dm', 'bpjs', 'puskesmas']:
        df_selected[col] = pd.to_numeric(df_selected[col], errors='coerce')

    df_clean = df_selected.dropna().reset_index(drop=True)

    # Normalisasi
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean[['penderita_dm', 'bpjs', 'puskesmas']])

    # ============================
    # ⚙️ Clustering
    # ============================
    k = st.slider("Jumlah cluster (k)", 2, 10, 3)
    kmeans = KMeans(n_clusters=k, random_state=42)
    df_clean['cluster'] = kmeans.fit_predict(X_scaled)

    # Evaluasi
    sil_score = silhouette_score(X_scaled, df_clean['cluster'])
    dbi_score = davies_bouldin_score(X_scaled, df_clean['cluster'])

    col1, col2 = st.columns(2)
    col1.metric("Silhouette Score", f"{sil_score:.4f}")
    col2.metric("Davies-Bouldin Index", f"{dbi_score:.4f}")

    # ============================
    # 📊 PCA Visualisasi
    # ============================
    st.subheader("Visualisasi Cluster (PCA 2D)")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    df_clean['pca1'] = X_pca[:, 0]
    df_clean['pca2'] = X_pca[:, 1]

    fig, ax = plt.subplots(figsize=(6, 4))
    scatter = ax.scatter(df_clean['pca1'], df_clean['pca2'], c=df_clean['cluster'], cmap='Set1', s=60, alpha=0.8)
    legend1 = ax.legend(*scatter.legend_elements(), title="Cluster")
    ax.add_artist(legend1)
    ax.set_xlabel("PCA 1")
    ax.set_ylabel("PCA 2")
    ax.set_title("Pemetaan Cluster (PCA 2D)", fontsize=12)
    st.pyplot(fig)

    # ============================
    # 📅 Visualisasi Per Tahun
    # ============================
    st.subheader("Distribusi Penderita Diabetes per Tahun")

    # Generate dynamic colors for all possible clusters
    colors = plt.cm.Set1(np.linspace(0, 1, k))
    color_map = {i: colors[i] for i in range(k)}

    tahun_list = sorted(df_clean['tahun'].unique())
    for tahun in tahun_list:
        df_tahun = df_clean[df_clean['tahun'] == tahun]
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create colors list based on cluster labels
        bar_colors = [color_map[cluster] for cluster in df_tahun['cluster']]
        
        bars = ax.bar(
            range(len(df_tahun)),  # Use indices instead of labels for x-axis
            df_tahun['penderita_dm'],
            color=bar_colors
        )
        
        # Set x-axis labels
        ax.set_xticks(range(len(df_tahun)))
        ax.set_xticklabels(df_tahun['kabupaten_kota'], rotation=45, ha='right', fontsize=8)
        ax.set_title(f"Tahun {tahun} - Jumlah Penderita DM per Cluster", fontsize=12)
        ax.set_ylabel("Jumlah Penderita DM")
        
        # Add legend for clusters
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color_map[i], label=f'Cluster {i}') for i in range(k)]
        ax.legend(handles=legend_elements, title="Cluster", bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        st.pyplot(fig)

    # ============================
    # 📋 Tabel Rekap
    # ============================
    st.subheader("Ringkasan Cluster")
    tabel_cluster = df_clean.groupby(['cluster']).agg(
        jumlah_daerah=('kabupaten_kota', 'count'),
        total_penderita_dm=('penderita_dm', 'sum'),
        rata_rata_penderita_dm=('penderita_dm', 'mean'),
        total_bpjs=('bpjs', 'sum'),
        total_puskesmas=('puskesmas', 'sum')
    ).reset_index()
    
    # Format numbers for better readability
    tabel_cluster['total_penderita_dm'] = tabel_cluster['total_penderita_dm'].apply(lambda x: f"{x:,.0f}")
    tabel_cluster['rata_rata_penderita_dm'] = tabel_cluster['rata_rata_penderita_dm'].apply(lambda x: f"{x:,.1f}")
    tabel_cluster['total_bpjs'] = tabel_cluster['total_bpjs'].apply(lambda x: f"{x:,.0f}")
    tabel_cluster['total_puskesmas'] = tabel_cluster['total_puskesmas'].apply(lambda x: f"{x:,.0f}")
    
    st.dataframe(tabel_cluster, use_container_width=True)

    # ============================
    # 📊 Analisis Cluster
    # ============================
    st.subheader("Analisis Karakteristik Cluster")
    
    # Create comparison chart for each cluster
    cluster_stats = df_clean.groupby('cluster').agg({
        'penderita_dm': 'mean',
        'bpjs': 'mean', 
        'puskesmas': 'mean'
    }).reset_index()
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot rata-rata penderita DM per cluster
    axes[0].bar(cluster_stats['cluster'], cluster_stats['penderita_dm'], 
                color=[color_map[i] for i in cluster_stats['cluster']])
    axes[0].set_title('Rata-rata Penderita DM per Cluster')
    axes[0].set_xlabel('Cluster')
    axes[0].set_ylabel('Rata-rata Penderita DM')
    
    # Plot rata-rata BPJS per cluster  
    axes[1].bar(cluster_stats['cluster'], cluster_stats['bpjs'],
                color=[color_map[i] for i in cluster_stats['cluster']])
    axes[1].set_title('Rata-rata Peserta BPJS per Cluster')
    axes[1].set_xlabel('Cluster')
    axes[1].set_ylabel('Rata-rata Peserta BPJS')
    
    # Plot rata-rata puskesmas per cluster
    axes[2].bar(cluster_stats['cluster'], cluster_stats['puskesmas'],
                color=[color_map[i] for i in cluster_stats['cluster']])
    axes[2].set_title('Rata-rata Jumlah Puskesmas per Cluster')
    axes[2].set_xlabel('Cluster')
    axes[2].set_ylabel('Rata-rata Jumlah Puskesmas')
    
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Data dengan Label Cluster")
    # Add cluster information to display
    display_df = df_clean.copy()
    display_df['penderita_dm'] = display_df['penderita_dm'].apply(lambda x: f"{x:,.0f}")
    display_df['bpjs'] = display_df['bpjs'].apply(lambda x: f"{x:,.0f}")
    st.dataframe(display_df, use_container_width=True)
    
else:
    st.info("Silakan upload file Excel terlebih dahulu.")