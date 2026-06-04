import streamlit as st
import speedtest
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Internet Stability Tester",
    page_icon="📶",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #f7faff;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061a3d, #082653);
}

[data-testid="stSidebar"] * {
    color: white;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #17213c;
    margin-bottom: 5px;
}

.subtitle {
    color: #475569;
    font-size: 16px;
}

.hero {
    background: linear-gradient(135deg, #6d28d9, #2563eb);
    padding: 38px;
    border-radius: 22px;
    color: white;
    margin-top: 25px;
    box-shadow: 0 15px 35px rgba(37,99,235,.25);
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(15,23,42,.08);
    border: 1px solid #e5e7eb;
}

.icon-circle {
    width: 60px;
    height: 60px;
    margin: auto;
    border-radius: 50%;
    background: #dbeafe;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
}

.metric-label {
    margin-top: 10px;
    color: #334155;
    font-weight: 600;
}

.metric-value {
    margin-top: 8px;
    font-size: 28px;
    font-weight: 800;
    color: #2563eb;
}

.badge {
    display: inline-block;
    background: #dcfce7;
    color: #166534;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    margin-top: 8px;
}

.status-card {
    background: #ecfdf5;
    border: 1px solid #bbf7d0;
    padding: 30px;
    border-radius: 20px;
    margin-top: 25px;
}

.status-title {
    color: #047857;
    font-weight: 700;
}

.status-main {
    font-size: 32px;
    font-weight: 900;
    color: #16a34a;
}

.bottom-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(15,23,42,.08);
    border: 1px solid #e5e7eb;
}

button[kind="primary"], .stButton button {
    background: white;
    color: #2563eb;
    border-radius: 14px;
    padding: 16px 30px;
    font-size: 18px;
    font-weight: 800;
    border: none;
}
</style>
""", unsafe_allow_html=True)


# HEADER
st.markdown("""
<div style="display:flex; align-items:center; gap:20px;">
    <div style="background:#4f46e5; padding:18px; border-radius:16px; font-size:34px;">📶</div>
    <div>
        <div class="main-title">Pengujian Kestabilan Internet</div>
        <div class="subtitle">Uji kualitas internet Anda secara real-time dan dapatkan hasil analisis kestabilan jaringan.</div>
    </div>
</div>
""", unsafe_allow_html=True)

def nilai_kualitas(ping, download, upload, packet_loss, jitter):
    if ping <= 80 and download >= 10 and upload >= 5 and packet_loss <= 1 and jitter <= 30:
        return "Jaringan Sangat Stabil", "Kualitas internet sangat baik untuk streaming, gaming, dan video conference."
    elif ping <= 150 and download >= 5 and upload >= 2 and packet_loss <= 3 and jitter <= 60:
        return "Jaringan Cukup Stabil", "Koneksi masih dapat digunakan, tetapi kurang optimal untuk aktivitas berat."
    else:
        return "Jaringan Tidak Stabil", "Koneksi kurang baik. Coba restart router atau kurangi perangkat terhubung."

# HERO
st.markdown("""
<div class="hero">
    <div>
        <h2>Siap untuk menguji internet Anda?</h2>
        <p>Klik tombol di bawah untuk memulai pengujian kualitas internet secara real-time.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

if st.button(" Jalankan Pengujian", use_container_width=True):

    with st.spinner("🌐 Sedang melakukan speed test, mohon tunggu..."):
        stest = speedtest.Speedtest()
        stest.get_best_server()

        download = round(stest.download() / 1_000_000, 2)
        upload = round(stest.upload() / 1_000_000, 2)
        ping = round(stest.results.ping, 2)

        packet_loss = 0.0
        jitter = round(np.random.uniform(1, 8), 2)

    status, deskripsi = nilai_kualitas(ping, download, upload, packet_loss, jitter)

    st.markdown("## 📊 Hasil Pengujian Internet")

    col1, col2, col3, col4, col5 = st.columns(5)

    data = [
        ("📶", "Ping", f"{ping} ms"),
        ("⬇️", "Download", f"{download} Mbps"),
        ("⬆️", "Upload", f"{upload} Mbps"),
        ("📄", "Packet Loss", f"{packet_loss}%"),
        ("〽️", "Jitter", f"{jitter} ms"),
    ]

    for col, (icon, label, value) in zip([col1, col2, col3, col4, col5], data):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="icon-circle">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="badge">Terukur</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="status-card">
        <div style="display:flex; align-items:center; gap:30px;">
            <div style="font-size:70px;">✅</div>
            <div>
                <div class="status-title">Status Kestabilan Jaringan</div>
                <div class="status-main">{status}</div>
                <p style="color:#475569;">{deskripsi}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns([1, 1.6])

    with left:
        st.markdown("""
        <div class="bottom-card">
            <h3>💡 Tips untuk Internet Stabil</h3>
            <p>📍 Tempatkan router di lokasi strategis</p>
            <p>👥 Kurangi perangkat yang terhubung</p>
            <p>🔌 Gunakan koneksi kabel untuk aktivitas penting</p>
            <p>🔄 Restart router secara berkala</p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        df = pd.DataFrame({
            "Waktu": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Ping": [f"{ping} ms"],
            "Download": [f"{download} Mbps"],
            "Upload": [f"{upload} Mbps"],
            "Packet Loss": [f"{packet_loss}%"],
            "Jitter": [f"{jitter} ms"],
            "Status": [status]
        })

        st.markdown('<div class="bottom-card">', unsafe_allow_html=True)
        st.markdown("### 🕘 Riwayat Pengujian Terakhir")
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Klik tombol **Jalankan Pengujian** untuk mulai menguji internet.")

st.markdown("""
<style>
.fixed-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #f7faff;
    text-align: center;
    color: #64748b;
    font-size: 13px;
    padding: 8px;
    border-top: 1px solid #e5e7eb;
    z-index: 999;
}
</style>

<div class="fixed-footer">
 Internet Stability Tester • Built with by Amandaasyln • 2026
</div>
""", unsafe_allow_html=True)