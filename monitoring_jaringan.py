import speedtest
import pandas as pd
from ping3 import ping
from datetime import datetime
import os
import time
import subprocess

# NAMA FILE DATASET
file_name = "monitoring.csv"

# CEK FILE CSV
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=[
        "Waktu",
        "Ping(ms)",
        "Download(Mbps)",
        "Upload(Mbps)",
        "PacketLoss(%)",
        "Jitter(ms)",
        "Status"
    ])

    df.to_csv(file_name, index=False)

print("====================================")
print(" MONITORING JARINGAN DIMULAI ")
print(" Data diambil setiap 5 menit ")
print("====================================\n")


# LOOP MONITORING

while True:

    try:
      
        # WAKTU
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

 
        # PING
        ping_result = ping("8.8.8.8")

        if ping_result is None:
            ping_ms = 0
        else:
            ping_ms = ping_result * 1000


        # JITTER
        ping_list = []

        for i in range(5):

            p = ping("8.8.8.8")

            if p is not None:
                ping_list.append(p * 1000)

            time.sleep(1)

        if len(ping_list) > 1:
            jitter = max(ping_list) - min(ping_list)
        else:
            jitter = 0

        # PACKET LOSS
        packet_loss = 0

        try:
            response = subprocess.run(
                ["ping", "-n", "5", "8.8.8.8"],
                capture_output=True,
                text=True
            )

            output = response.stdout

            for line in output.split("\n"):

                if "Lost =" in line:

                    loss_text = line.split("(")[1].split("%")[0]
                    packet_loss = float(loss_text)

        except:
            packet_loss = 0

        # SPEEDTEST
        try:
            st = speedtest.Speedtest()

            st.get_best_server()

            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000

        except:
            print("Speedtest gagal...")

            download = 0
            upload = 0

        # STATUS JARINGAN
        if ping_ms < 100 and packet_loss < 5:
            status = "Stabil"
        else:
            status = "Tidak Stabil"

        # SIMPAN DATA
        data = {
            "Waktu": waktu,
            "Ping(ms)": round(ping_ms, 2),
            "Download(Mbps)": round(download, 2),
            "Upload(Mbps)": round(upload, 2),
            "PacketLoss(%)": packet_loss,
            "Jitter(ms)": round(jitter, 2),
            "Status": status
        }

        df = pd.DataFrame([data])

        df.to_csv(
            file_name,
            mode='a',
            header=False,
            index=False
        )

        print(f"""
==================================
Waktu          : {waktu}
Ping           : {round(ping_ms,2)} ms
Download       : {round(download,2)} Mbp
Upload         : {round(upload,2)} Mbps
Packet Loss    : {packet_loss} %
Jitter         : {round(jitter,2)} ms
Status         : {status}
==================================
""")

    except Exception as e:
        print("Terjadi error:", e)

    time.sleep(300)










    