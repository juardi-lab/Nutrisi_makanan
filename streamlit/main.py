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
    options=["Beranda", "Tabel Data", "Kesimpulan"],
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

        # 🔸 Tambahkan mapping keterangan cluster
        cluster_labels = {
            0: "Tinggi Protein & Lemak",
            1: "Rendah Kalori & Nutrisi Berat",
            2: "Tinggi Karbohidrat & Kalori"
        }
        filtered_df["keterangan_cluster"] = filtered_df["Cluster"].map(cluster_labels)

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
                        <div style='font-size: 12px; text-align: center; color: grey;'>
                        {row['keterangan_cluster']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            st.markdown("<hr style='border:0.5px solid #ccc;'>", unsafe_allow_html=True)
            
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
