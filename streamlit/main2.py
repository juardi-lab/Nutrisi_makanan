import streamlit as st
from streamlit_option_menu import option_menu

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Klaster Banjir Bogor",
    page_icon="🌧",
    layout="wide"
)

# Navbar horizontal
selected = option_menu(
    menu_title=None,  # Tidak menampilkan judul
    options=["Home", "Visualisasi", "Klastering", "Kesimpulan"],
    icons=["house", "bar-chart", "diagram-3", "clipboard-check"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

# Isi halaman berdasarkan menu yang dipilih
if selected == "Home":
    st.title("📊 ANALISIS KLASTER TERHADAP HUBUNGAN CURAH HUJAN DENGAN KEJADIAN BANJIR DI KOTA BOGOR")
    st.subheader("Menggunakan Algoritma K-Means")
    st.markdown("""
    Selamat datang di aplikasi analisis data banjir Kota Bogor.  
    Proyek ini bertujuan untuk mengeksplorasi hubungan antara curah hujan dan kejadian banjir menggunakan algoritma K-Means Clustering.
    """)
    st.image("https://cdn.pixabay.com/photo/2015/11/07/11/39/flood-1032090_960_720.jpg", caption="Ilustrasi Banjir", use_column_width=True)

elif selected == "Visualisasi":
    st.header("📈 Visualisasi Data")
    st.markdown("Tampilkan grafik curah hujan dan kejadian banjir di sini...")

elif selected == "Klastering":
    st.header("📊 Hasil Klastering")
    st.markdown("Tampilkan hasil algoritma K-Means di sini...")

elif selected == "Kesimpulan":
    st.header("📝 Kesimpulan")
    st.markdown("Berisi ringkasan dan insight dari hasil analisis.")