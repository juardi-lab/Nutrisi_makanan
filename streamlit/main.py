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

# ========== AMBIL PARAMETER ==========
selected = st.query_params.get("page", ["Beranda"])[0]

# Daftar halaman yang valid
valid_pages = ["Beranda", "Tabel Data", "Kesimpulan"]

# Kalau selected tidak valid, pakai default
if selected not in valid_pages:
    selected = "Beranda"

# ========== NAVIGASI ==========
selected = option_menu(
    menu_title=None,
    options=valid_pages,
    icons=["house", "table", "check-circle"],
    menu_icon="cast",
    default_index=default_index,
    orientation="horizontal"
)
# ========== AMBIL DATA ==========
file_id = "1pR1b8GTF4tshPdKfZyaPyflGg_bRmZSt"
download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
response = requests.get(download_url)
df = pd.read_csv(io.StringIO(response.text))

# Mapping cluster
cluster_labels = {
    0: "Tinggi Protein & Lemak",
    1: "Rendah Kalori & Nutrisi Berat",
    2: "Tinggi Karbohidrat & Kalori"
}

# ========== HALAMAN BERANDA ==========
if selected == "Beranda":
    st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🍽️ Dashboard Data Makanan</h1>", unsafe_allow_html=True)

    img_url = "https://drive.google.com/uc?export=download&id=1M52cM5GXWl6SbIDsAN9F7niqvcICLxOL"
    img_response = requests.get(img_url)
    image = Image.open(io.BytesIO(img_response.content))

    st.image(image, caption="Makanan", use_container_width=True)
    st.markdown("<p style='text-align:center;'>Selamat datang! Website ini menampilkan data makanan berdasarkan kandungan nutrisinya dan gambarnya.</p>", unsafe_allow_html=True)

# ========== HALAMAN TABEL DATA ==========
elif selected == "Tabel Data":
    st.markdown("<h2 style='color:#4CAF50;'>📊 Tabel Data Makanan</h2>", unsafe_allow_html=True)

    search = st.text_input("Cari nama makanan")
    filtered_df = df[df['name'].str.contains(search, case=False)] if search else df.copy()

    if filtered_df.empty:
        st.warning("⚠️ Data tidak ditemukan.")
    else:
        sort_col = st.selectbox("Urutkan berdasarkan", ["name", "calories", "proteins", "fat", "carbohydrate", "Cluster"])
        sort_order = st.radio("Urutan", ["Naik", "Turun"], horizontal=True)
        filtered_df = filtered_df.sort_values(by=sort_col, ascending=(sort_order == "Naik"))

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
                    st.image(row["image"], width=130)

                with col_nutrisi:
                    st.markdown(f"<h4 style='margin-bottom: 5px;'>{row['name']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div style='font-size: 14px; line-height: 1.8; color: black !important;'>
                        <b>Kalori:</b> {row['calories']} kcal<br>
                        <b>Karbohidrat:</b> {row['carbohydrate']} g<br>
                        <b>Protein:</b> {row['proteins']} g<br>
                        <b>Lemak:</b> {row['fat']} g
                        </div>
                    """, unsafe_allow_html=True)

                with col_cluster:
                    cluster_value = int(row["Cluster"])
                    cluster_name = cluster_labels.get(cluster_value, "Tidak Diketahui")
                    st.markdown(f"""
                        <a href='?page=Kesimpulan' style='text-decoration: none;'>
                            <div style='text-align: center; cursor: pointer;'>
                                <div style='font-size: 22px; font-weight: bold; color: black;'>{cluster_value}</div>
                                <div style='font-size: 12px; color: #555;'>{cluster_name}</div>
                            </div>
                        </a>
                    """, unsafe_allow_html=True)

            st.markdown("<hr style='border:0.5px solid #ccc;'>", unsafe_allow_html=True)

# ========== HALAMAN KESIMPULAN ==========
elif selected == "Kesimpulan":
    st.markdown("<h2 style='color:#4CAF50;'>📌 Kesimpulan</h2>", unsafe_allow_html=True)

    st.markdown("""### 🟢 Cluster 0 – Tinggi Protein & Lemak
• Jumlah Data: 196 item  
• Rata-rata Nutrisi: 334,3 kkal | 23,8 g protein | 20,9 g lemak | 13,5 g karbohidrat  
Kelompok ini cocok untuk atlet, pemulihan, dan penderita malnutrisi.
""")

    st.markdown("""### 🟡 Cluster 1 – Rendah Kalori & Nutrisi Berat
• Jumlah Data: 794 item  
• Rata-rata Nutrisi: 91,9 kkal | 5,8 g protein | 2,3 g lemak | 12,4 g karbohidrat  
Cocok untuk diet rendah kalori, diabetes tipe 2, hipertensi, dan ginjal kronis.
""")

    st.markdown("""### 🔴 Cluster 2 – Tinggi Karbohidrat & Kalori
• Jumlah Data: 296 item  
• Rata-rata Gizi: 346,9 kkal | 7,3 g protein | 6,2 g lemak | 67,4 g karbohidrat  
Cocok untuk anak-anak, remaja aktif, pekerja fisik, dan atlet.
""")

    st.info("Aplikasi ini menyajikan hasil pengelompokan makanan berdasarkan kandungan nutrisi.")

# ========== FOOTER ==========
st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem;">
    <div style='text-align: center; color: black; font-size: 16px;'>
        © 2025 Muhammad Ilham Juardi - Dashboard Data Makanan
    </div>
""", unsafe_allow_html=True)
