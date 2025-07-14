import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import requests
import io

# ========== KONFIGURASI HALAMAN ==========
st.set_page_config(
    page_title="Dashboard Makanan",
    page_icon="🍽️",
    layout="centered"
)

# ========== NAVIGASI HORIZONTAL ==========
selected = option_menu(
    menu_title=None,
    options=["Beranda", "Tabel Data", "Visualisasi", "Tentang Metode", "Kesimpulan"],
    icons=["house", "table", "bar-chart-line", "info-circle", "check-circle"],
    orientation="horizontal"
)

# ========== BACA DATA DARI GOOGLE DRIVE ==========
file_id = "1pR1b8GTF4tshPdKfZyaPyflGg_bRmZSt"
download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

response = requests.get(download_url)
df = pd.read_csv(io.StringIO(response.text))

# ========== LOGIKA TIAP HALAMAN ==========
if selected == "Beranda":
    st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🍽️ Dashboard Data Makanan </h1>", unsafe_allow_html=True)

    # Ambil gambar dari Google Drive
    image_url = "https://drive.google.com/uc?export=download&id=1M52cM5GXWl6SbIDsAN9F7niqvcICLxOL"
    response = requests.get(image_url)
    image = Image.open(io.BytesIO(response.content))

    st.image(image, caption="Makanan", use_container_width=True)
    st.write("<p style='text-align:center;'>Selamat datang! Website ini menampilkan data makanan berdasarkan kandungan nutrisinya dan gambarnya.</p>", unsafe_allow_html=True)

elif selected == "Tabel Data":
    st.markdown("<h2 style='color:#4CAF50;'>📊 Tabel Data Makanan</h2>", unsafe_allow_html=True)

    search = st.text_input("Cari nama makanan")
    if search:
        filtered_df = df[df['name'].str.contains(search, case=False)].copy()
    else:
        filtered_df = df.copy()

    if filtered_df.empty:
        st.warning("⚠️ Data tidak ditemukan.")
    else:
        sort_col = st.selectbox("Urutkan berdasarkan", ["name", "calories", "proteins", "fat", "carbohydrate", "Cluster"], index=0)
        sort_order = st.radio("Urutan", ["Naik", "Turun"], horizontal=True)
        filtered_df = filtered_df.sort_values(by=sort_col, ascending=(sort_order == "Naik"))

        rows_per_page = 100
        total_rows = len(filtered_df)
        total_pages = (total_rows - 1) // rows_per_page + 1
        page_number = st.number_input("Halaman", min_value=1, max_value=total_pages, value=1)
        start_idx = (page_number - 1) * rows_per_page
        end_idx = start_idx + rows_per_page
        paginated_df = filtered_df.iloc[start_idx:end_idx]

        for idx, row in paginated_df.iterrows():
            with st.container():
                col_gambar, col_nutrisi, col_cluster = st.columns([1, 2, 1])

                with col_gambar:
                    st.write("")
                    st.image(row["image"], width=130)

                with col_nutrisi:
                    st.markdown(f"<h4 style='margin-bottom: 5px;'>{row['name']}</h4>", unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <div style='font-size: 14px; line-height: 1.8; color: black !important;'>
                        <b>Kalori:</b> {row['calories']} kcal<br>
                        <b>Karbohidrat:</b> {row['carbohydrate']} g<br>
                        <b>Protein:</b> {row['proteins']} g<br>
                        <b>Lemak:</b> {row['fat']} g
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col_cluster:
                    st.markdown("<h5 style='color:black;'>Cluster</h5>", unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <div style='font-size: 20px; text-align: center; font-weight: bold; color: black;'>
                        {row['Cluster']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            st.markdown("<hr style='border:0.5px solid #ccc;'>", unsafe_allow_html=True)

elif selected == "Visualisasi":
    st.markdown("<h2 style='color:#4CAF50;'>📈 Visualisasi Data</h2>", unsafe_allow_html=True)

    st.subheader("🔹 K-Means Clustering")
    st.markdown("**Metode Elbow**")

    elbow_url = "https://drive.google.com/uc?export=download&id=11jpb8FlbT9Gw_3IlMBDScaPeo9mHA_vK"
    response = requests.get(elbow_url)
    elbow_img = Image.open(io.BytesIO(response.content))
    st.image(elbow_img, use_container_width=True)

    st.markdown("""
    Grafik di atas merupakan hasil dari **Metode Elbow** pada algoritma K-Means untuk menentukan jumlah klaster optimal.
    - **Sumbu X (Jumlah Cluster):** menunjukkan jumlah klaster yang diuji, dari 1 hingga 10.
    - **Sumbu Y (WCSS):** total jarak kuadrat antar data dan pusat klaster.
    Titik 'tekukan' menunjukkan jumlah klaster optimal, yaitu **3 cluster**.
    """)

    st.markdown("**Hasil Clustering K-Means**")
    
    scatter_url = "https://drive.google.com/uc?export=download&id=1EyET1hBKMOSQ5MGBXeo8pSsmQRRucXSf"
    response = requests.get(scatter_url)
    scatter_img = Image.open(io.BytesIO(response.content))
    st.image(scatter_img, use_container_width=True)
    
    st.markdown("""
    Plot ini menunjukkan hasil akhir pengelompokan K-Means dengan 3 klaster berdasarkan variabel gizi makanan.
    """)

    st.subheader("🔸 DBSCAN Clustering")
    st.markdown("**K-Distance Plot (Menentukan Epsilon)**")
    kdistance_url = "https://drive.google.com/uc?export=download&id=1AEa0LO-cizuLtu82fTtEdZJoqBXe6oJ6"
    response = requests.get(kdistance_url)
    kdistance_img = Image.open(io.BytesIO(response.content))
    st.image(kdistance_img, use_container_width=True)
    st.markdown("""
    Grafik ini digunakan untuk menentukan nilai **epsilon (ε)** optimal pada DBSCAN.
    """)

    st.markdown("**Hasil Clustering DBSCAN**")
    dbscan_url = "https://drive.google.com/uc?export=download&id=1iKtXvH_znbJeMX7E9O8KwdkjxVR6VfRk"
    response = requests.get(dbscan_url)
    dbscan_img = Image.open(io.BytesIO(response.content))
    st.image(dbscan_img, use_container_width=True)
    st.markdown("""
    Visualisasi ini menunjukkan hasil akhir dari metode DBSCAN.
    """)

elif selected == "Tentang Metode":
    st.markdown("<h2 style='color:#4CAF50;'>🔍 Metode Klastering yang Digunakan</h2>", unsafe_allow_html=True)
    st.markdown("<div style='background-color:#e6fff0;padding:10px;border-left:5px solid #4CAF50;'>"
                "Analisis klaster dilakukan menggunakan dua metode utama: <strong>K-Means Clustering</strong> dan <strong>DBSCAN (Density-Based Spatial Clustering of Applications with Noise)</strong>."
                "</div><br>", unsafe_allow_html=True)

    # ===================== K-MEANS =====================
    with st.container():
        st.markdown("### 📌 K-Means Clustering")
        st.markdown("""
        Metode K-Means digunakan untuk mengelompokkan data ke dalam beberapa klaster berdasarkan kedekatan data terhadap pusat klaster (centroid). 
        Metode ini cocok untuk data yang memiliki bentuk distribusi yang jelas dan terstruktur.
        """)

    with st.container():
        st.markdown("### 🧪 Langkah-langkah Analisis K-Means")
        st.markdown("""
        1. **Preprocessing data**  
        2. **Menentukan jumlah klaster optimal** (menggunakan Elbow Method)  
        3. **Menerapkan algoritma K-Means**  
        4. **Visualisasi dan interpretasi hasil**
        """)

    with st.container():
        st.markdown("### 📊 Evaluasi Model K-Means")
        st.markdown("""
        Model dievaluasi menggunakan **Silhouette Score**, dan **Davies-Bouldin Index**.
        """)

    # ===================== DBSCAN =====================
    with st.container():
        st.markdown("### 📌 DBSCAN Clustering")
        st.markdown("""
        DBSCAN (Density-Based Spatial Clustering of Applications with Noise) adalah algoritma klastering yang berbasis kepadatan data.
        DBSCAN efektif untuk mendeteksi klaster dengan bentuk yang tidak beraturan dan mengidentifikasi outlier atau data yang tidak termasuk dalam klaster mana pun.
        """)

    with st.container():
        st.markdown("### 🧪 Langkah-langkah Analisis DBSCAN")
        st.markdown("""
        1. **Preprocessing data**  
        2. **Menentukan parameter epsilon (ε) dan minimum sampel (minPts)**  
        3. **Menerapkan algoritma DBSCAN**  
        4. **Identifikasi klaster dan outlier**
        """)

    with st.container():
        st.markdown("### 📊 Evaluasi Model DBSCAN")
        st.markdown("""
        DBSCAN dievaluasi menggunakan metrik yang sama seperti K-Means, yaitu:  
        - **Silhouette Score**    
        - **Davies-Bouldin Index**  
        Selain itu, DBSCAN juga dianalisis dari seberapa baik ia mengidentifikasi noise (outlier) di dataset.
        """)

    st.markdown("<div style='background-color:#fff3cd;padding:15px;border-left:5px solid #ffc107;border-radius:8px;'>"
                "<h5>⚠️ Catatan Penting:</h5>"
                "<ul>"
                "<li>📌 K-Means cocok untuk data yang berbentuk bulat dan terdistribusi merata.</li>"
                "<li>🌐 DBSCAN cocok untuk data yang memiliki bentuk klaster tidak beraturan dan mengandung outlier.</li>"
                "<li>🔍 Visualisasi seperti PCA membantu melihat bentuk klaster.</li>"
                "<li>✅ Evaluasi model penting untuk menilai kualitas pengelompokan.</li>"
                "</ul>"
                "</div>", unsafe_allow_html=True)


elif selected == "Kesimpulan":
    st.markdown("<h2 style='color:#4CAF50;'>📌 Kesimpulan</h2>", unsafe_allow_html=True)

    st.markdown("""
    ### 🟢 Cluster 0 – Tinggi Protein & Lemak
    • Jumlah Data: 196 item
    
    • Rata-rata Nutrisi: 334,3 kkal | 23,8 g protein | 20,9 g lemak | 13,5 g karbohidrat
    Kelompok ini terdiri dari makanan tinggi protein dan lemak, Karbohidrat tergolong rendah
    Cocok untuk atlet, individu dalam masa pemulihan, dan penderita malnutrisi.
    """)

    st.markdown("""
    ### 🟡 Cluster 1 – Rendah Kalori & Nutrisi Berat
        • Jumlah Data: 794 item
        • Rata-rata Nutrisi: 91,9 kkal | 5,8 g protein | 2,3 g lemak | 12,4 g karbohidrat
          Kelompok ini berasal dari makanan dengan kalori, protein, dan lemak rendah, Karbohidrat juga cenderung rendah
          Cocok untuk diet rendah kalori, penderita diabetes tipe 2, hipertensi, dan penyakit ginjal kronis.
        💡 Mendukung pola makan sehat berbasis nabati dan pengendalian berat badan..
    """)

    st.markdown("""
    ### 🔴 Cluster 2 – Tinggi Karbohidrat & Kalori
        • Jumlah Data: 296 item
        • Rata-rata Gizi: 346,9 kkal | 7,3 g protein | 6,2 g lemak | 67,4 g karbohidrat
          Kelompok ini berasa dari makanan dengan kandungan karbohidrat tinggi, Kalori juga tinggi, namun protein dan lemak sedang
          Cocok untuk anak-anak, remaja aktif, pekerja fisik, dan atlet.
    """)

    st.info("""
    Aplikasi ini menyajikan hasil pengelompokan makanan berdasarkan kandungan nutrisi.
    """)

# ========== FOOTER ==========
st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem;">
    <div style='text-align: center; color: black; font-size: 16px;'>
        © 2025 Muhammad Ilham Juardi - Dashboard Data Makanan
    </div>
""", unsafe_allow_html=True)
