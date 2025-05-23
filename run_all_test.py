import csv
from stress_test_client import stress_test  # pastikan file ini di-import dengan benar
import os

# Konfigurasi kombinasi pengujian
pool_types = ['thread', 'process']
volumes = ['file10MB.bin', 'file50MB.bin', 'file100MB.bin']
client_workers = [5, 10, 20]
# server_workers = [10, 20, 30]  # ← kamu bisa ubah worker server manual sebelum tes

# Output file
csv_filename = "hasil_stresstest.csv"

# Header CSV
header = [
    "Nomor", "Pool Type", "Volume", "Jumlah Client Worker",
    "Jumlah Server Worker", "Waktu Total (s)", "Rata-rata Throughput (MB/s)",
    "Client Sukses", "Client Gagal"
]

rows = []
nomor = 1

# Loop kombinasi
for pool in pool_types:
    for volume in volumes:
        for c_workers in client_workers:
            for s_workers in server_workers:
                print(f"\n▶️ Test #{nomor}: pool={pool}, volume={volume}, client={c_workers}, server={s_workers}")
                
                # Reminder: kamu HARUS ganti jumlah server worker MANUAL sebelum uji kombinasi ini.
                input(f"🚨 Pastikan server worker = {s_workers}. Tekan Enter untuk lanjut...")

                results = stress_test(
                    pool_type=pool,
                    workers=c_workers,
                    file_upload=volume,
                    file_download=volume
                )

                sukses = sum(1 for r in results if r['upload_status'] and r['download_status'])
                gagal = c_workers - sukses
                total_duration = sum(r['duration'] for r in results)
                avg_throughput = sum(r['throughput'] for r in results) / c_workers / (1024 * 1024)

                rows.append([
                    nomor,
                    pool,
                    volume,
                    c_workers,
                    s_workers,
                    round(total_duration, 2),
                    round(avg_throughput, 2),
                    sukses,
                    gagal
                ])
                nomor += 1

# Simpan ke CSV
with open(csv_filename, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"\n✅ Semua hasil sudah disimpan ke '{csv_filename}'")
